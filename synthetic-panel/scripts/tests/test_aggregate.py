import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import aggregate  # noqa: E402
from fixtures import panel  # noqa: E402

GROUNDED = [
    {"trait": "age 38", "basis": "grounded", "source": "G1"},
    {"trait": "two kids", "basis": "grounded", "source": "G1"},
    {"trait": "shops weekly", "basis": "assumed"},
]


class TestShares(unittest.TestCase):
    def test_shares_include_none_and_sum_to_one(self):
        r = aggregate.summarise(panel(["A"] * 6 + ["B"] * 3 + ["none"] * 3))
        self.assertAlmostEqual(sum(r["shares"].values()), 1.0)
        self.assertAlmostEqual(r["shares"]["none"], 0.25)
        self.assertEqual(r["n"], 12)

    def test_winner_excludes_decoy(self):
        r = aggregate.summarise(panel(["D"] * 5 + ["B"] * 4 + ["A"] * 3))
        self.assertEqual(r["winner"], "B")

    def test_margin_is_share_gap_to_runner_up(self):
        r = aggregate.summarise(panel(["A"] * 6 + ["B"] * 3 + ["C"] * 3))
        self.assertEqual(r["runner_up"], "B")
        self.assertAlmostEqual(r["margin"], 0.25)

    def test_tie_broken_by_mean_intent(self):
        p = panel(["A"] * 4 + ["B"] * 4 + ["C"] * 4)
        for person in p["personas"]:
            person["response"]["intent"]["C"] = 7
        r = aggregate.summarise(p)
        self.assertEqual(r["winner"], "C")

    def test_mean_intent_per_stimulus(self):
        r = aggregate.summarise(panel(["A"] * 12))
        self.assertAlmostEqual(r["mean_intent"]["A"], 6.0)

    def test_invalid_choice_raises(self):
        with self.assertRaises(ValueError):
            aggregate.summarise(panel(["A"] * 11 + ["Z"]))

    def test_intent_out_of_range_raises(self):
        p = panel(["A"] * 12)
        p["personas"][0]["response"]["intent"]["A"] = 9
        with self.assertRaises(ValueError):
            aggregate.summarise(p)


class TestFlags(unittest.TestCase):
    def test_decoy_above_15_percent_flags_sycophancy(self):
        r = aggregate.summarise(panel(["D"] * 2 + ["A"] * 6 + ["B"] * 4))
        self.assertIn("sycophancy", r["flags"])
        self.assertEqual(r["confidence"], "Low")

    def test_decoy_at_or_below_15_percent_is_fine(self):
        r = aggregate.summarise(panel(["D"] + ["A"] * 7 + ["B"] * 4, traits=GROUNDED))
        self.assertNotIn("sycophancy", r["flags"])

    def test_agreement_above_85_percent_flags_homogeneity(self):
        r = aggregate.summarise(panel(["A"] * 11 + ["B"]))
        self.assertIn("homogeneity", r["flags"])

    def test_position_bias_flag(self):
        ids = ["A", "B", "C", "D"]
        orders = [ids[i % 4:] + ids[:i % 4] for i in range(12)]
        choices = [o[0] if o[0] != "D" else "B" for o in orders]
        r = aggregate.summarise(panel(choices, orders=orders))
        self.assertIn("position_bias", r["flags"])

    def test_grounding_coverage(self):
        r = aggregate.summarise(panel(["A"] * 6 + ["B"] * 6, traits=GROUNDED))
        self.assertAlmostEqual(r["grounding_coverage"], 2 / 3)


class TestConfidence(unittest.TestCase):
    def test_high_when_grounded_clean_and_clear(self):
        r = aggregate.summarise(panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2, traits=GROUNDED))
        self.assertEqual(r["flags"], [])
        self.assertEqual(r["confidence"], "High")

    def test_medium_when_margin_small(self):
        r = aggregate.summarise(panel(["A"] * 5 + ["B"] * 4 + ["C"] * 3, traits=GROUNDED))
        self.assertEqual(r["confidence"], "Medium")

    def test_low_when_ungrounded(self):
        assumed = [{"trait": "age 38", "basis": "assumed"}]
        r = aggregate.summarise(panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2, traits=assumed))
        self.assertEqual(r["confidence"], "Low")

    def test_single_context_caps_at_medium(self):
        r = aggregate.summarise(
            panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2, traits=GROUNDED, single_context=True)
        )
        self.assertIn("single_context", r["flags"])
        self.assertEqual(r["confidence"], "Medium")

    def weak(self, decoy_score):
        p = panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2, traits=GROUNDED)
        for person in p["personas"]:
            person["response"]["intent"]["D"] = decoy_score
        return aggregate.summarise(p)

    def test_decoy_everyone_rejects_flags_weak_decoy(self):
        r = self.weak(1)
        self.assertIn("weak_decoy", r["flags"])
        self.assertEqual(r["confidence"], "Medium")
        self.assertTrue(any("decoy" in x.lower() for x in r["confidence_reasons"]))

    def test_decoy_at_threshold_is_weak(self):
        self.assertIn("weak_decoy", self.weak(aggregate.WEAK_DECOY_MAX)["flags"])

    def test_plausible_decoy_is_not_weak(self):
        r = self.weak(3)
        self.assertNotIn("weak_decoy", r["flags"])
        self.assertEqual(r["confidence"], "High")

    def test_no_decoy_is_not_flagged_weak(self):
        p = panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2, traits=GROUNDED)
        for st in p["stimuli"]:
            st["decoy"] = False
        self.assertNotIn("weak_decoy", aggregate.summarise(p)["flags"])

    def test_confidence_reasons_explain_label(self):
        r = aggregate.summarise(panel(["D"] * 3 + ["A"] * 9))
        self.assertTrue(any("decoy" in reason for reason in r["confidence_reasons"]))


if __name__ == "__main__":
    unittest.main()
