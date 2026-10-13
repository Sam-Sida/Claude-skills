---
name: competitor-intel
description: Builds a one-page competitive landscape report (dark-themed feature comparison matrix of the target vs 8–10 competitors, a "competitive moat" pipeline, and Strengths / Key Threats / Market Gaps columns) for any target company or product, exported as HTML + PDF. Use when the user gives a company name or URL and asks for a competitor analysis, competitive landscape, competitor intel, comparison matrix, or "who are X's competitors and how do they compare".
---

# Competitor Intel

Produces `<slug>_competitors-intel.pdf` (+ `.html` and `.json`): a single tall page with

1. **Header**: `<Product> — Competitive Landscape`, a category subtitle (e.g. "Consumer AI Legal Assistant Comparison"), and a month/year badge.
2. **Comparison matrix**: the subject in the first (highlighted) column, then 8–10 competitors. Feature rows are grouped into 4–6 sections, and each cell is ✓ / ✗ / ◐ or short text, plus an optional small mono note.
3. **Competitive moat**: 3–5 steps showing the combination of capabilities that only the subject has.
4. **Competitive positioning**: three cards (Strengths, Key Threats, Market Gaps / Opportunities) with 5 bullets each.
5. **Footer**: compile date and source types.

`references/schema.md` defines the data format. The examples below come from a consumer legal-AI analysis of LawConnect Chat and show the tone, density and note length to aim for.

## Step 1: Pin down the subject

From the user's company name or URL, fetch the homepage and the main product pages (WebFetch; fall back to the browser if they're blocked). Work out:

- **Which product** to analyse. Companies often have several, and the legal-AI example analysed *LawConnect Chat*, not LawConnect overall. If there are multiple products and the user didn't say which, choose the flagship or the one matching the URL, and state that choice in your final summary.
- **Category**, phrased the way the subtitle needs it: `<Audience> <Category> Comparison`.
- **Target user, markets/regions, pricing, monetization.**
- **The value chain**: the steps a user goes through (e.g. free chat → report → lawyer review → referral). This becomes the moat and drives the middle matrix sections.

## Step 2: Choose 8–10 competitors

Mix these archetypes. The legal-AI example used all of them:

| Archetype | Example (consumer legal AI) |
|---|---|
| Direct, same category, best-known brand | DoNotPay, AI Lawyer |
| Incumbents with a human/service layer that are adding AI | JustAnswer, Rocket Lawyer, LegalZoom |
| Emerging or free challengers in the same niche | Cicerai, FreeLawChat |
| Adjacent player aimed at a different segment (e.g. B2B) | Genie AI |
| General-purpose substitute that eats top-of-funnel demand | ChatGPT |

Find them with WebSearch (e.g. "<category> alternatives", "<subject> vs", "best <category> <year>", G2/Capterra/Product Hunt listings). If the user named competitors, use theirs and fill in the rest. Order the columns from closest rival to most distant substitute.

## Step 3: Design the feature rows

Use 12–16 rows in 4–6 uppercase sections:

- **CORE MODEL** (always first): Pricing (text cell plus a price note), Target User, Markets.
- **2–3 category-specific sections**, derived from the subject's value chain and the competitors' differentiators. The legal-AI example used AI CAPABILITIES, HUMAN LAWYER LAYER and PLATFORM & REACH. Rename these for the category (e.g. for a fintech: PRODUCT, COMPLIANCE & TRUST, INTEGRATIONS).
- **REVENUE MODEL** (always last): Monetization.

Choose rows that make the picture honest:
- At least one row where **only the subject** has ✓. This is what makes the moat visible.
- Several rows where the subject is ✗ or ◐ (e.g. Contract Review, Mobile App and Multilingual). These feed the Threats and Gaps columns.
- Rows that split the competitors, not rows where everyone has ✓.

## Step 4: Research every cell

For each competitor × row, check pricing pages, product/feature pages, app stores (for mobile), help docs and recent reviews. Rules:

- `✓` means the feature is clearly offered. `✗` means it's absent. `◐` means it's partial, limited, add-on-only or beta, and needs a note saying why.
- Keep notes to about 25 characters, written as qualifiers: "Reports only", "Premium plans", "iOS + Android", "$39.99/mo".
- Pricing tone: `good` = Free, `warn` = Freemium or Paid. Use `bad` only for something clearly prohibitive.
- **Never guess.** If something can't be verified, use `◐` with the note "Unverified", or plain text "TBD". Keep a private list of sources so you can answer follow-ups.
- Research the competitors in parallel (several WebSearch/WebFetch calls per turn).

## Step 5: Write the moat and positioning

- **Moat**: `title` is "<Subject>'s Competitive Moat" and `tagline` is a punchy one-line claim (e.g. "The Full Pipeline No One Else Has"). Use 3–5 steps from the value chain, each with an emoji, a 2–3-word title, and a ~6-word description that includes a concrete number where there is one (e.g. "24,000+ lawyers via LEAP network").
- **Strengths** (5): only claims the matrix supports. Lead with the unique combination.
- **Key Threats** (5): name specific competitors and what they're doing. Include the general-purpose substitute, and at least one weakness of the subject's own shown in the matrix.
- **Market Gaps / Opportunities** (5): whitespace nobody owns, plus the subject's ✗ rows reframed as opportunities.
- Each bullet should fit on one line, at most ~75 characters.

## Step 6: Build

1. Write the data to `<cwd>/<slug>_competitors-intel.json`, following `references/schema.md`. `slug` is the lowercase company name (e.g. `lawconnect`).
2. Render it:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>/scripts/build.ps1" -Data <slug>_competitors-intel.json -Out <slug>_competitors-intel.html -Pdf
   ```
   The script injects the JSON into `assets/template.html` and prints a single-page PDF with headless Chrome or Edge, sizing the page to fit the content.
   - **No PowerShell, e.g. macOS/Linux:** copy `assets/template.html`, replace the contents of the `<script type="application/json" id="report-data">` block with the JSON (escape any `</` as `<\/`), then run `chrome --headless=new --no-pdf-header-footer --virtual-time-budget=5000 --print-to-pdf=<out>.pdf file://<abs-path>.html`.
3. **Verify** by reading the PDF. Check that every column has a value in every row, nothing is truncated, and it's all on one page.

## Step 7: Report back

Give the user the PDF path, the product and category you chose, the competitor list with a one-line reason for including each, and any cells marked Unverified. Offer to swap competitors or rows and rebuild. Editing the JSON and rerunning step 6 is enough.
