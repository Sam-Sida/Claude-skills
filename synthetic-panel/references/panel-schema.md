# panel.json schema

```json
{
  "run_id": "2026-11-01-mealkit-headlines",   // date + slug; unique across the calibration log
  "date": "2026-11-01",
  "project": "Meal kit launch",
  "question": "Which headline would busy Sydney parents click?",
  "decision": "Pick the launch headline for the Meta campaign",
  "segment": "Parents of school-age kids in Sydney, dual income",
  "context": "Scrolling Instagram in the evening, about 2 seconds per post",
  "metric": "click-through rate",
  "single_context": false,                     // true only if personas weren't run as separate subagents
  "grounding": [
    {"id": "G1", "source": "2025 customer survey (n=400)", "summary": "68% say weeknight time is the main pain"}
  ],
  "stimuli": [
    {"id": "A", "text": "Dinner sorted in 15 minutes", "decoy": false},
    {"id": "B", "text": "Fresh food, less waste", "decoy": false},
    {"id": "D", "text": "Meal kits for everyone", "decoy": true, "decoy_reason": "Generic, no benefit"}
  ],
  "personas": [
    {
      "id": "P01",
      "name": "Priya",
      "summary": "38, nurse, two kids, shops at Coles on Sundays",
      "traits": [
        {"trait": "Short on weeknight time", "basis": "grounded", "source": "G1"},
        {"trait": "Price-sensitive since 2024", "basis": "assumed"}
      ],
      "order": ["B", "D", "A"],                 // from orders.py
      "response": {
        "choice": "A",                          // a stimulus id or "none"
        "intent": {"A": 6, "B": 4, "D": 2},     // 1-7, one per stimulus
        "objection": "Probably costs more than cooking myself",
        "quote": "Fifteen minutes would actually change my Tuesday."
      }
    }
  ],
  "narrative": {                               // add after aggregate.py, before render.py
    "headline": "Time beats freshness for dual-income parents",
    "findings": [
      {"text": "A wins on speed", "confidence": "Medium", "evidence": "7 of 12 chose A"}
    ],
    "minority_view": "Waste-conscious parents preferred B",
    "objections": ["Price isn't shown", "Sounds like every other kit"],
    "live_test": "Meta A/B of A vs B, 5 days, about A$500 per variant, measuring CTR",
    "caveats": ["Grounding is one 2025 survey"]
  }
}
```

The `//` comments are explanations only. Real JSON can't contain them.

## Confidence rules (applied by aggregate.py)

| Label | Rule |
|---|---|
| **Low** | Decoy share above 15%, or under 30% of traits grounded |
| **Medium** | Any other flag (including a weak decoy, mean intent 1.5/7 or lower, or option wording leaked into persona cards), or under 60% grounded, or winner leads by under 25 points, or under 8 personas |
| **High** | None of the above |
