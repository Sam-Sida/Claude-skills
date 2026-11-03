import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import render  # noqa: E402
from fixtures import panel  # noqa: E402


def with_narrative(p):
    p["narrative"] = {
        "headline": "Speed beats freshness for time-poor parents",
        "findings": [
            {"text": "Headline A wins on <speed>", "confidence": "Medium", "evidence": "7 of 12 chose A"}
        ],
        "minority_view": "Waste-conscious parents prefer B",
        "objections": ["Price is unclear"],
        "live_test": "Run A vs B on Meta for 5 days, US$500 each",
        "caveats": ["Synthetic panel, not a measurement"],
    }
    return p


class TestRender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_writes_markdown_and_html(self):
        p = with_narrative(panel(["D"] * 3 + ["A"] * 6 + ["B"] * 3))
        paths = render.render(p, self.tmp.name, "mealkit")
        self.assertTrue(os.path.exists(paths["md"]))
        self.assertTrue(os.path.exists(paths["html"]))
        self.assertNotIn("pdf", paths)

    def test_markdown_shows_key_facts(self):
        p = with_narrative(panel(["D"] * 3 + ["A"] * 6 + ["B"] * 3))
        md = open(render.render(p, self.tmp.name, "mealkit")["md"], encoding="utf-8").read()
        self.assertIn("Which headline gets the most clicks?", md)
        self.assertIn("Dinner sorted in 15 minutes", md)
        self.assertIn("Low", md)
        self.assertIn("sycophancy", md)
        self.assertIn("Run A vs B on Meta", md)
        self.assertIn("(decoy)", md)

    def test_html_escapes_text(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        html = open(render.render(p, self.tmp.name, "mealkit")["html"], encoding="utf-8").read()
        self.assertIn("&lt;speed&gt;", html)
        self.assertNotIn("<speed>", html)

    def test_missing_narrative_raises(self):
        with self.assertRaises(ValueError):
            render.render(panel(["A"] * 12), self.tmp.name, "x")

    def test_agreement_label_is_clear(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        paths = render.render(p, self.tmp.name, "mealkit")
        for kind in ("md", "html"):
            text = open(paths[kind], encoding="utf-8").read()
            self.assertIn("Largest single answer", text)
            self.assertNotIn("Top-option agreement", text)
            self.assertNotIn("Agreement on top option", text)

    def test_grounding_section_lists_facts_and_trait_basis(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        paths = render.render(p, self.tmp.name, "mealkit")
        for kind in ("md", "html"):
            text = open(paths[kind], encoding="utf-8").read()
            self.assertIn("Grounding", text)
            self.assertIn("G1", text)
            self.assertIn("Parents 30-45", text)
            self.assertIn("1 grounded, 1 assumed", text)

    def test_grounding_section_says_when_there_is_no_data(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5,
                                 traits=[{"trait": "busy", "basis": "assumed"}]))
        p["grounding"] = []
        md = open(render.render(p, self.tmp.name, "mealkit")["md"], encoding="utf-8").read()
        self.assertIn("No grounding data", md)
        self.assertIn("0 grounded, 1 assumed", md)

    def test_objections_render_as_list_without_double_punctuation(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        p["narrative"]["objections"] = ["Too pricey.", "Sounds generic."]
        html = open(render.render(p, self.tmp.name, "mealkit")["html"], encoding="utf-8").read()
        self.assertNotIn(".;", html)
        self.assertIn("<li>Too pricey.</li>", html)

    def test_weak_decoy_shown_in_report(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        for person in p["personas"]:
            person["response"]["intent"]["D"] = 1
        md = open(render.render(p, self.tmp.name, "mealkit")["md"], encoding="utf-8").read()
        self.assertIn("weak_decoy", md)
        self.assertIn("Decoy mean intent: 1.0", md)

    @unittest.skipUnless(render._browser(), "needs Chrome or Edge")
    def test_png_preview(self):
        p = with_narrative(panel(["A"] * 7 + ["B"] * 5))
        paths = render.render(p, self.tmp.name, "mealkit", png=True)
        self.assertTrue(paths["png"].endswith("_synthetic-panel.png"))
        with open(paths["png"], "rb") as f:
            self.assertEqual(f.read(4), bytes([0x89]) + b"PNG")


if __name__ == "__main__":
    unittest.main()
