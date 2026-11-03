"""Calibration log: compare panel predictions with what really happened.

Usage:
  py calibration.py add panel.json [--log path]
  py calibration.py record <run_id> <actual_winner> [--note "CTR 2.1% vs 1.4%"] [--log path]
  py calibration.py score [--log path]
  py calibration.py list [--log path]

--log works before or after the subcommand. The default log is calibration-log.csv in the skill folder, shared across all projects.
"""
import argparse
import csv
import datetime
import json
import os

import aggregate

DEFAULT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calibration-log.csv")
FIELDS = [
    "run_id", "date", "project", "question", "options", "n_options", "predicted_winner",
    "predicted_share", "margin", "confidence", "flags", "actual_winner", "actual_note",
    "hit", "recorded_date",
]
LEVELS = ["High", "Medium", "Low"]


def _read(log):
    if not os.path.exists(log):
        return []
    with open(log, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(log, rows):
    with open(log, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def add(panel, results, log=DEFAULT_LOG):
    rows = _read(log)
    if any(r["run_id"] == panel["run_id"] for r in rows):
        raise ValueError(f"run_id {panel['run_id']!r} is already in the log")
    options = [s["id"] for s in panel["stimuli"] if not s.get("decoy")]
    rows.append({
        "run_id": panel["run_id"],
        "date": panel.get("date", ""),
        "project": panel.get("project", ""),
        "question": panel.get("question", ""),
        "options": "|".join(options),
        "n_options": len(options),
        "predicted_winner": results["winner"],
        "predicted_share": f"{results['shares'][results['winner']]:.3f}",
        "margin": f"{results['margin']:.3f}",
        "confidence": results["confidence"],
        "flags": "|".join(results["flags"]),
        "actual_winner": "", "actual_note": "", "hit": "", "recorded_date": "",
    })
    _write(log, rows)


def record(run_id, actual, note="", log=DEFAULT_LOG, today=None):
    rows = _read(log)
    row = next((r for r in rows if r["run_id"] == run_id), None)
    if row is None:
        raise KeyError(f"run_id {run_id!r} is not in the log")
    if actual not in row["options"].split("|"):
        raise ValueError(f"{actual!r} is not one of the tested options ({row['options']})")
    row["actual_winner"] = actual
    row["actual_note"] = note
    row["hit"] = "1" if actual == row["predicted_winner"] else "0"
    row["recorded_date"] = today or datetime.date.today().isoformat()
    _write(log, rows)
    return row


def score(log=DEFAULT_LOG):
    rows = _read(log)
    done = [r for r in rows if r["hit"] in ("0", "1")]

    def rate(rs):
        return sum(r["hit"] == "1" for r in rs) / len(rs) if rs else None

    by_conf = {}
    for level in LEVELS:
        rs = [r for r in done if r["confidence"] == level]
        by_conf[level] = {"resolved": len(rs), "hits": sum(r["hit"] == "1" for r in rs), "hit_rate": rate(rs)}
    return {
        "resolved": len(done),
        "pending": len(rows) - len(done),
        "hit_rate": rate(done),
        "chance_rate": sum(1 / int(r["n_options"]) for r in done) / len(done) if done else None,
        "by_confidence": by_conf,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=DEFAULT_LOG)
    # SUPPRESS keeps the main parser's value unless --log is also given after the subcommand
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--log", default=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", parents=[common])
    a.add_argument("panel")
    r = sub.add_parser("record", parents=[common])
    r.add_argument("run_id")
    r.add_argument("actual")
    r.add_argument("--note", default="")
    sub.add_parser("score", parents=[common])
    sub.add_parser("list", parents=[common])
    args = ap.parse_args()
    log = os.path.abspath(args.log)

    if args.cmd == "add":
        with open(args.panel, encoding="utf-8") as f:
            panel = json.load(f)
        add(panel, aggregate.summarise(panel), log=log)
        print(f"Logged {panel['run_id']} in {log}")
    elif args.cmd == "record":
        print(json.dumps(record(args.run_id, args.actual, args.note, log=log), indent=2))
    elif args.cmd == "score":
        print(json.dumps(score(log=log), indent=2))
    else:
        print(json.dumps(_read(log), indent=2))


if __name__ == "__main__":
    main()
