import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import aggregate  # noqa: E402
import leakage  # noqa: E402
from fixtures import panel  # noqa: E402

STIMULI = [
    {"id": "A", "text": "Put customer evidence behind your next growth decision."},
    {"id": "C", "text": "Test campaigns in days, not 6-8 weeks."},
]


def card(pid, summary="CMO, ASX 200 bank", traits=("Board wants proof",)):
    return {"id": pid, "summary": summary, "traits": [{"trait": t, "basis": "assumed"} for t in traits]}


class TestLeakage(unittest.TestCase):
    def test_three_word_phrase_from_an_option_is_a_leak(self):
        leaks = leakage.find_leaks(STIMULI, [card("P01", traits=["Wants customer evidence behind decisions"])])
        self.assertEqual(leaks, [{"persona": "P01", "stimulus": "A", "phrase": "customer evidence behind"}])

    def test_two_words_with_a_number_is_a_leak(self):
        leaks = leakage.find_leaks(STIMULI, [card("P03", traits=["Research takes 6-8 weeks per study"])])
        self.assertEqual([(x["persona"], x["stimulus"], x["phrase"]) for x in leaks], [("P03", "C", "6-8 weeks")])

    def test_summary_is_checked_too(self):
        leaks = leakage.find_leaks(STIMULI, [card("P02", summary="Tired of waiting 6-8 weeks for research")])
        self.assertEqual(leaks[0]["persona"], "P02")

    def test_paraphrase_and_common_words_are_not_leaks(self):
        people = [card("P01", traits=["Research cycles take about two months", "Owns the growth budget"])]
        self.assertEqual(leakage.find_leaks(STIMULI, people), [])

    def test_case_and_punctuation_are_ignored(self):
        leaks = leakage.find_leaks(STIMULI, [card("P04", traits=["TEST CAMPAIGNS, in days if possible"])])
        self.assertEqual(leaks[0]["phrase"], "test campaigns in")

    def test_one_leak_per_persona_and_stimulus(self):
        leaks = leakage.find_leaks(STIMULI, [card("P01", traits=["test campaigns in days", "6-8 weeks"])])
        self.assertEqual(len(leaks), 1)

    def test_aggregate_flags_leakage_and_caps_confidence(self):
        p = panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2,
                  traits=[{"trait": "loves dinner sorted in 15 minutes", "basis": "grounded", "source": "G1"}])
        r = aggregate.summarise(p)
        self.assertIn("leakage", r["flags"])
        self.assertEqual(r["confidence"], "Medium")
        self.assertTrue(any("wording" in x for x in r["confidence_reasons"]))
        self.assertEqual(len(r["leaks"]), 12)

    def test_aggregate_no_leakage_on_clean_cards(self):
        p = panel(["A"] * 7 + ["B"] * 3 + ["C"] * 2,
                  traits=[{"trait": "age 38", "basis": "grounded", "source": "G1"}])
        r = aggregate.summarise(p)
        self.assertNotIn("leakage", r["flags"])
        self.assertEqual(r["leaks"], [])


if __name__ == "__main__":
    unittest.main()
