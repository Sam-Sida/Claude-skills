import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import aggregate  # noqa: E402
import calibration  # noqa: E402
from fixtures import panel  # noqa: E402


def results(run_id="run-1", choices=None):
    p = panel(choices or ["A"] * 7 + ["B"] * 3 + ["C"] * 2)
    p["run_id"] = run_id
    return p, aggregate.summarise(p)


class TestCalibration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = os.path.join(self.tmp.name, "calibration-log.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def rows(self):
        with open(self.log, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_add_creates_log_with_prediction(self):
        calibration.add(*results(), log=self.log)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "run-1")
        self.assertEqual(rows[0]["predicted_winner"], "A")
        self.assertEqual(rows[0]["n_options"], "3")
        self.assertEqual(rows[0]["actual_winner"], "")

    def test_add_duplicate_run_id_raises(self):
        calibration.add(*results(), log=self.log)
        with self.assertRaises(ValueError):
            calibration.add(*results(), log=self.log)

    def test_record_marks_hit(self):
        calibration.add(*results(), log=self.log)
        calibration.record("run-1", "A", note="CTR 2.1% vs 1.4%", log=self.log, today="2026-11-08")
        row = self.rows()[0]
        self.assertEqual(row["actual_winner"], "A")
        self.assertEqual(row["hit"], "1")
        self.assertEqual(row["actual_note"], "CTR 2.1% vs 1.4%")
        self.assertEqual(row["recorded_date"], "2026-11-08")

    def test_record_marks_miss(self):
        calibration.add(*results(), log=self.log)
        calibration.record("run-1", "B", log=self.log)
        self.assertEqual(self.rows()[0]["hit"], "0")

    def test_record_unknown_run_raises(self):
        calibration.add(*results(), log=self.log)
        with self.assertRaises(KeyError):
            calibration.record("nope", "A", log=self.log)

    def test_record_rejects_unknown_option(self):
        calibration.add(*results(), log=self.log)
        with self.assertRaises(ValueError):
            calibration.record("run-1", "Z", log=self.log)

    def test_score_hit_rate_chance_and_pending(self):
        for i in range(3):
            calibration.add(*results(run_id=f"run-{i}"), log=self.log)
        calibration.record("run-0", "A", log=self.log)
        calibration.record("run-1", "B", log=self.log)
        s = calibration.score(log=self.log)
        self.assertEqual(s["resolved"], 2)
        self.assertEqual(s["pending"], 1)
        self.assertAlmostEqual(s["hit_rate"], 0.5)
        self.assertAlmostEqual(s["chance_rate"], 1 / 3)
        self.assertIn("High", s["by_confidence"])

    def test_score_empty_log(self):
        s = calibration.score(log=self.log)
        self.assertEqual(s["resolved"], 0)
        self.assertIsNone(s["hit_rate"])

    def cli(self, *args):
        script = os.path.join(os.path.dirname(__file__), "..", "calibration.py")
        return subprocess.run([sys.executable, script, *args], capture_output=True, text=True)

    def write_panel(self):
        p, _ = results()
        path = os.path.join(self.tmp.name, "panel.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(p, f)
        return path

    def test_cli_accepts_log_after_subcommand(self):
        out = self.cli("add", self.write_panel(), "--log", self.log)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(self.rows()[0]["run_id"], "run-1")

    def test_cli_accepts_log_before_subcommand(self):
        out = self.cli("--log", self.log, "add", self.write_panel())
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(len(self.rows()), 1)

    def test_cli_record_and_score_with_log_after(self):
        self.cli("add", self.write_panel(), "--log", self.log)
        rec = self.cli("record", "run-1", "A", "--note", "won", "--log", self.log)
        self.assertEqual(rec.returncode, 0, rec.stderr)
        sc = self.cli("score", "--log", self.log)
        self.assertEqual(sc.returncode, 0, sc.stderr)
        self.assertEqual(json.loads(sc.stdout)["resolved"], 1)


if __name__ == "__main__":
    unittest.main()
