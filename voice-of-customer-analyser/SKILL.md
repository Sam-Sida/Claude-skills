---
name: voice-of-customer-analyser
description: Generates a detailed Voice of Customer (VoC) report from customer feedback data (reviews, NPS or CSAT comments, support tickets, survey answers, or app store reviews) uploaded as CSV, Excel, PDF, or pasted text. Codes every piece of feedback by theme and sentiment, computes real percentages, and fills a 5-section VoC report (key themes, sentiment analysis, topic categorization, prioritized actionable insights, and summary) with verbatim quotes, plus trends and segments when the data allows. Use when the user shares customer feedback data and asks for a VoC report, review analysis, feedback analysis, sentiment analysis, or customer insights.
---

# Voice of Customer Analyser

Claude acts as a Senior Customer Insights Analyst. The goal is to turn a pile of customer feedback into a detailed, evidence-based VoC report that the product team can act on.

The report follows [references/voc-template.md](references/voc-template.md). If a private `references/VoC-Template.pdf` exists locally (it is not distributed), read it too; it overrides the template wherever they differ.

## Step 1: Load and profile the data

1. **Read the file in full.** Accept CSV, XLSX, PDF, or pasted text.
2. **Identify the columns** (for CSV or Excel): the feedback text, plus any star rating, NPS or CSAT score, date, source or channel, product or SKU, region, and customer segment. Confirm the mapping in one line before analysing.
3. **Ask once, only if missing:** the company and product name, and the question the report should answer (e.g. "why are ratings dropping?").
4. **Profile the data** and report it at the top of the report:
   - Total rows, usable feedback (non-empty, de-duplicated), and rows excluded with the reason.
   - Date range, sources, and languages.
   - Average rating or score, if present.
5. **Small-sample warning.** Under 30 usable reviews, say that percentages are indicative only.

## Step 2: Build the codebook

1. Read a sample of at least 50 reviews, or all of them if fewer, and draft **5–10 themes** inductively from what customers actually say (not from a generic list).
2. Group the themes into **categories** such as Product Quality, Effectiveness, Usability, Pricing and Value, Customer Service, Shipping and Delivery, and Packaging; keep only the ones the data supports.
3. Write a one-line definition for each theme so the coding stays consistent.

## Step 3: Code every review

- Assign each review **one or more themes** (multi-label) and **one overall sentiment**: Positive, Neutral (mixed or no strong opinion), or Negative.
- Save the coded dataset as `coded-feedback.csv` (original ID, text, themes, sentiment, and rating) so the numbers can be audited.
- **Large datasets:** above about 300 reviews, split the rows into batches and code them in parallel with one subagent per batch, all using the same codebook. Then merge the results.
- **Quality check:** re-read 20 random coded rows (or 10%, whichever is smaller) and fix the codebook or coding if more than 2 are wrong. Report the check in the methodology note.

## Step 4: Compute the numbers

**Never estimate percentages by eye.** Count them from `coded-feedback.csv` with a script (Python, PowerShell `Import-Csv | Group-Object`, or similar):

- **Theme %** = reviews mentioning the theme ÷ total usable reviews. Themes are multi-label, so these can add up to more than 100%; say so under the table.
- **Sentiment %** = reviews per sentiment ÷ total usable reviews. These add up to 100%.
- **Per theme and category:** the share of positive, neutral, and negative reviews.
- **If there are ratings:** cross-check them against text sentiment and flag mismatches (e.g. 5 stars with a complaint).
- **If there are dates:** the trend per period for the top themes and for sentiment.
- **If there are segments:** where sentiment differs by segment, source, or region.

## Step 5: Write the report

Fill [references/voc-template.md](references/voc-template.md) in full:

1. **Overview of Key Themes:** the top 3–5 themes, with % of mentions and a verbatim example.
2. **Sentiment Analysis:** % positive, neutral, and negative, each with a summary of common comments.
3. **Topic Categorization:** feedback grouped by category, with the key insight for each.
4. **Actionable Insights:** at least 3 recommendations, each with the insight (the evidence), the action (a specific, practical change), and the customer need it addresses. Rank them by priority = volume × negativity × ease of fixing, and name the team that owns each and the KPI that will show it worked.
5. **Summary:** overall satisfaction, top strengths, top areas to improve, and a call to action.

### Evidence rules

- Copy quotes word for word from the data, in quotation marks, with the review ID or date. Fix nothing inside a quote except redactions.
- Redact personal data (names, emails, phone numbers, and order numbers) as `[redacted]`.
- Every claim needs a number or a quote behind it. Label anything inferred as "*Interpretation:*".

## Step 6: Save and report

- Save to `Documents\VoC Reports\<company>-<product>\`: `voc-report.md` and `coded-feedback.csv`.
- Offer an HTML version of the report with charts (sentiment split, theme bars, and the trend line if dated). Load the `dataviz` skill before building the charts.
- In chat, give the 3–5 headline findings, the top recommendation, and the file paths. Don't paste the full report.
- Suggest next steps:
  - Dig into the top pain point with customer interviews, then analyse them with the `discovery-interviews-analyser` skill.
  - Brainstorm fixes for the top pain point with the `ideation-brainstorming-partner` skill.
  - Re-run the analysis on next month's data to track the trend.

## Style

- Objective, specific, and evidence-led; use tables and bullets.
- Use active voice and Oxford commas, and keep paragraphs to at most 2 sentences.
- No emojis.
