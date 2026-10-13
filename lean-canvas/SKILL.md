---
name: lean-canvas
description: Researches a company on the public internet and produces a filled one-page Lean Canvas PDF (Problem, Solution, UVP, Unfair Advantage, Customer Segments, Existing Alternatives, Key Metrics, High-Level Concept, Channels, Early Adopters, Cost Structure, Revenue Streams) using the bundled lean-canvas template, plus a sources page. Use when the user names a company, startup, product or URL and asks for a lean canvas, lean canvas PDF, or a one-page business model breakdown of it.
---

# Lean Canvas generator

Turn a company name (or URL) into a filled Lean Canvas PDF, built on
`assets/lean-canvas-template.pdf`, with every box backed by public information
or clearly-marked inference.

## Inputs

- **Company** (required): name and/or website. If ambiguous (several companies
  share the name), ask which one before researching.
- **Designed by** (optional): default to the user's name if known, else "Claude (AI research)".
- **Output folder** (optional): default to the current working directory.

## Workflow

### 1. Deep research

Do real research, not recall. Run several searches in parallel, then fetch the
most useful pages. Cover at least:

| Need | Where to look |
|---|---|
| What they sell, for whom, positioning/tagline | Company homepage, product & pricing pages, "About" |
| Problem & pain points | Product marketing copy, launch posts, founder interviews, customer case studies |
| Pricing / revenue model | Pricing page, investor relations, S-1/10-K/annual report (public cos.) |
| Revenue, growth, users, margins | Earnings releases, annual reports, press, Crunchbase/Tracxn/PitchBook snippets, credible news |
| Funding, investors, team size | Crunchbase, press releases, LinkedIn summaries |
| Competitors / alternatives | "X alternatives", "X vs Y", G2/Capterra, analyst coverage |
| Channels & go-to-market | Marketing site, app stores, partner programs, sales job postings |
| Moat | Patents, network effects, data, brand, regulatory licenses, exclusive partnerships |
| Costs | Annual report expense breakdown, job postings (headcount mix), infrastructure hints |

Prefer primary sources (company site, filings) and recent data — note the year
of any figure. Keep a running list of source titles + URLs for the sources page.

### 2. Draft each box

Write tight, scannable bullets — the canvas is small. Guidance per section:

- **problem**: top 3 customer problems (not company problems).
- **existing_alternatives**: how customers solved it before/without them; name real competitors.
- **solution**: top 3 features mapped to the 3 problems.
- **unique_value_prop**: ONE sentence, ideally their actual positioning; optionally a second line for the "why different".
- **high_level_concept**: an "X for Y" analogy (e.g. "Airbnb = eBay for spare rooms").
- **unfair_advantage**: things that can't easily be copied or bought. Be honest — if it's weak, say so.
- **customer_segments**: who pays / who uses; include segment sizes if public.
- **early_adopters**: characteristics of the first users who adopted it (historical, if known).
- **key_metrics**: the few numbers that matter, with latest public values where available (e.g. "**MAU** 100M (2025)").
- **channels**: concrete paths to customers (SEO, app stores, direct sales, partners, PLG/virality…).
- **cost_structure**: main fixed and variable costs; include reported figures if public.
- **revenue_streams**: model, pricing tiers, revenue figure, gross margin, LTV hints.

Rules:
- **Mark inference.** Prefix any item that is your inference rather than a
  reported fact with `[i] ` — it renders in italics, and the legend explains it.
- Use `**text**` for a short bold lead-in where it helps scanning.
- Length budget: 3–5 bullets per upper box, ~8–25 words each; cost/revenue
  boxes can take 5–7 bullets. The script auto-shrinks text but stays readable
  only if you respect this budget (it warns on stderr when it had to squeeze).
- Use real numbers with years; never invent figures. If a figure is an
  estimate, say "est." and mark it `[i]`.

### 3. Write the content JSON

Save to the scratchpad (or the output folder) as `<company>-lean-canvas.json`:

```json
{
  "designed_for": "Company Name",
  "designed_by": "Claude (AI research)",
  "date": "DD/MM/YYYY",
  "version": "1.0",
  "sections": {
    "problem": ["...", "...", "..."],
    "existing_alternatives": ["..."],
    "solution": ["..."],
    "key_metrics": ["..."],
    "unique_value_prop": ["..."],
    "high_level_concept": ["..."],
    "unfair_advantage": ["..."],
    "channels": ["..."],
    "customer_segments": ["..."],
    "early_adopters": ["..."],
    "cost_structure": ["..."],
    "revenue_streams": ["..."]
  },
  "notes": ["Research date, scope, key assumptions, data gaps."],
  "sources": [{"title": "Company 2025 Annual Report", "url": "https://..."}]
}
```

Date is today's date in DD/MM/YYYY. `notes` and `sources` go on page 2.

### 4. Generate the PDF

Find a Python 3 with `pypdf` and `reportlab` (plus `pypdfium2` for previews).
Try `python`, then `py`, then LibreOffice's bundled interpreter
(`C:\Program Files\LibreOffice\program\python.exe` on Windows). If the
packages are missing: `<python> -m pip install --user pypdf reportlab pypdfium2`.

```bash
<python> scripts/fill_canvas.py <content.json> "<output-folder>/<Company> Lean Canvas.pdf"
```

(Paths relative to this skill's directory.)

### 5. Verify visually

```bash
<python> scripts/render_preview.py "<output.pdf>" <scratchpad>/preview.png
```

Read the PNG. Check that no box overflows, text is legible (if a box was
squeezed, shorten that box's bullets and regenerate), and the header fields
are filled. Iterate until clean.

### 6. Deliver

Give the user the PDF path and a 3–5 line summary: the UVP, the biggest
insight, and any significant data gaps (e.g. private company, revenue unknown).
