# Report data schema

```jsonc
{
  "title": "LawConnect Chat — Competitive Landscape",   // H1
  "subtitle": "Consumer AI Legal Assistant Comparison", // next to the date badge
  "date": "April 2026",                                 // badge (rendered uppercase)
  "subjectLabel": "Subject",                            // tag under the first column: "★ SUBJECT"
  "columns": ["LawConnect", "DoNotPay", "..."],         // columns[0] is the subject (highlighted)
  "sections": [
    {
      "name": "Core Model",                              // section divider (rendered uppercase)
      "rows": [
        { "feature": "Pricing", "cells": [ /* exactly one cell per column, in column order */ ] }
      ]
    }
  ],
  "moat": {                                              // optional; omit to hide the panel
    "title": "LawConnect's Competitive Moat",
    "tagline": "The Full Pipeline No One Else Has",
    "steps": [ { "icon": "💬", "title": "Free AI Chat", "text": "Zero-cost entry point lowers barrier to users" } ]
  },
  "positioning": {
    "strengths": ["..."],   // card title is "<columns[0]> Strengths"
    "threats":   ["..."],
    "gaps":      ["..."]
  },
  "footer": "Compiled April 2026 · Sources: Company websites, product pages, and public reviews"
}
```

## Cells

| Form | Renders as |
|---|---|
| `"yes"` / `"no"` / `"partial"` | green ✓ / red ✗ / yellow ◐ |
| `"Any other string"` | plain text |
| `{ "s": "yes", "note": "iOS + Android" }` | symbol with a small mono note underneath |
| `{ "text": "Paid", "tone": "warn", "note": "$39.99/mo" }` | coloured text with a note. `tone` is `good` (green), `warn` (orange) or `bad` (red); leave it out for neutral text |

Keep notes to about 25 characters or less. With 10 competitor columns, each one is only about 115px wide.
