---
name: synthetic-panel
description: Runs a synthetic customer panel — a set of grounded AI personas who each react independently to 2–6 stimuli (headlines, ad scripts, value propositions, pricing, concepts, landing pages, or messages) — with a hidden decoy to catch sycophancy, shuffled order to catch position bias, an agreement check to catch homogenized answers, a confidence label on every finding, and a global calibration log that scores past predictions against real outcomes. Exports Markdown, HTML, and PDF. Use whenever the user wants to know how customers, buyers, or a segment would react to, choose between, or object to something before testing it for real — "test these headlines with personas", "which ad would CMOs click", "simulate a focus group", "concept test this pricing", "synthetic users", "what would our customers think of this", "role-play my target customer" — even if they don't say "panel". Also use when the user reports a real A/B or campaign result for an earlier panel ("headline B actually won", "log the result") or asks how accurate past panels were.
---

# Synthetic panel

A synthetic panel predicts how a segment will react. It does not measure it. Generic LLM role-play fails in known ways: it likes whatever it is shown (sycophancy), its "different" personas give near-identical answers (homogeneity), it favours whatever comes first (position bias), and it invents people who don't match the real customers. This skill exists to make those failures visible, label confidence honestly, and keep score against reality over time, so the user learns how far to trust it.

Everything below serves that goal. When in doubt, choose the option that makes the result more honest rather than more impressive.

## Modes

| The user… | Mode |
|---|---|
| Wants reactions to stimuli | **Run** (steps 1–9) |
| Reports what really happened for an earlier run | **Log result** (bottom of this file) |
| Asks how accurate panels have been | **Score** (bottom of this file) |

Scripts live in `scripts/` and need only Python 3's standard library. Use `python3`, `python`, or `py`, whichever exists. Paths below are relative to this skill's folder.

## Run

### 1. Brief

Get these, asking only for what's missing (one question at a time; propose a default):

- **Stimuli:** 2–6 options, with exact wording. Give each a short id (A, B, C…).
- **Segment:** who reacts (e.g. "enterprise CMOs at ASX 200 companies").
- **Context of exposure:** where and how they meet it (a LinkedIn feed scroll, a pricing page they sought out, a cold email). Attention level changes everything, so be concrete.
- **Choice question:** what each persona decides (e.g. "Which would you click, if any?").
- **Decision and metric:** what the user will do with the answer, and what real metric would settle it (CTR, sign-up, reply rate). This becomes the live test at the end.
- **Grounding data (optional but valuable):** reviews, survey results, interview notes, CRM exports, analytics, a website. Read it.
- **Panel size:** default 12. Use 8–20.
- **Output folder and name:** default the current folder, with a short lowercase slug.

### 2. Grounding

Extract facts from the grounding data as `G1`, `G2`… with a one-line summary and source each: who the customers are, what they care about, the words they use, and what they complain about. If there is no data, say so plainly. The panel will still run, but the scripts will mark confidence Low, which is the honest outcome.

Never invent statistics about the segment. A persona trait is either `grounded` (traceable to a G-fact) or `assumed`.

### 3. Decoy

Write one extra option that a real competitor could plausibly run, but that is weaker on the decision metric for this segment. Real customers rarely pick it; a panel that does is telling you it's agreeing to please.

A decoy only tests for sycophancy if it is tempting. One that every persona scores 1 out of 7 tells you nothing, and the scripts flag it as `weak_decoy`. To make it tempting:

- **Match the real options' form:** same length, tone, and structure, and the same kind of concrete claim. A one-line headline among headlines, not a slogan among specific promises.
- **Use the segment's own words** (from the G-facts where there are any), so it doesn't read as obviously off-target.
- **Make it weaker in one specific way:** a generic benefit everyone claims, a feature instead of an outcome, a promise this segment doesn't rank highly, or a vague claim with no proof. Name that weakness in `decoy_reason`.
- **Avoid giveaways:** no category clichés ("AI-powered", "for modern brands", "for everyone"), nothing absurd, and nothing noticeably shorter or blander than the rest.

Before you build the roster, check it: would a busy member of the segment hesitate for a second between the decoy and the weakest real option? If not, rewrite the decoy. Mark it `"decoy": true`.

### 4. Roster

Build N personas that span the segment's real spread, not N variations of the average buyer. Vary role, seniority or life stage, budget, current solution, attitude to the category, and attention. Include at least 2 people who are indifferent or sceptical, because most real people ignore most messages.

For each persona write: `id` (P01…), `name`, a one-line `summary`, and 4–6 `traits`, each tagged `grounded` (with its G source) or `assumed`.

Write the traits in your own words, never in an option's wording. A persona whose card says "research takes 6-8 weeks" will favour the headline "not 6-8 weeks" because it echoes their card, not because it persuades them. This applies even when a G-fact uses the same words as an option: paraphrase the fact ("studies take about two months"). Save the roster to panel.json (stimuli and personas, no responses yet) and check it:

```bash
py scripts/leakage.py <folder>/panel.json
```

It lists any phrase shared between an option and a persona card, and exits with an error if there is one. Rewrite those traits and run it again until it is clean. If a leak gets through, `aggregate.py` flags `leakage` later.

### 5. Orders

```bash
py scripts/orders.py --stimuli A,B,C,D --n 12 --seed <any int>
```

Each persona sees the options in its own order (the decoy included), with every option shown first about equally often.

### 6. Run each persona independently

Spawn one subagent per persona, **all in the same turn**, so they run in parallel and none can see another's answer. Independence is the point: one context writing 12 personas converges on one voice. Use the prompt in `references/persona-prompt.md`, filled with that persona's card, the context of exposure, the choice question, and the options in that persona's order.

Give each subagent only what its persona would know. Leave out the user's hypothesis, the decision, which option is the decoy, and the other personas.

If subagents aren't available, write each persona's answer yourself, one at a time, and set `"single_context": true` in panel.json. The scripts then cap confidence at Medium and flag it, because the answers are not independent.

### 7. Assemble and score

Write `panel.json` to the output folder (the schema is in `references/panel-schema.md`), then:

```bash
py scripts/aggregate.py <folder>/panel.json
```

Read the flags before writing anything:

| Flag | Meaning | What to do |
|---|---|---|
| `sycophancy` | Decoy share is above 15% | Treat the ranking as unreliable. Report it; don't explain it away |
| `weak_decoy` | The decoy's mean intent is 1.5/7 or lower | The sycophancy check didn't really run, so confidence is capped at Medium. Say so, and in caveats name what a stronger decoy would have looked like. Don't rerun with a new decoy to clear the flag |
| `leakage` | An option's wording appears in a persona card | Those personas may have been primed. Confidence is capped at Medium; name the personas and the phrase in caveats. Step 4's check should have caught it, so note that it was missed |
| `homogeneity` | More than 85% gave the same answer ("none" counts as an answer) | Possible real consensus, but more often a roster that's too narrow. Say which you think it is and why |
| `position_bias` | More than 50% picked whatever was shown first | The stimuli may be too similar to tell apart |
| `single_context` | Personas weren't independent | Note it in caveats |

Don't rerun or edit answers to make flags disappear. The flags are findings.

### 8. Narrative and render

Add a `narrative` block to panel.json: a headline, 3–5 findings (each with its own confidence and evidence such as "7 of 12 chose A"), the minority view, the top objections in the personas' words, the live test that would settle the question (channel, variants, rough budget, duration, and metric), and caveats. A finding's confidence can be lower than the overall label but never higher.

```bash
py scripts/render.py <folder>/panel.json --out-dir <folder> --name <slug> --pdf --png
```

This writes `<slug>_synthetic-panel.md`, `.html`, `.pdf`, and a `.png` screenshot of the report. Read the PNG to check the layout: every section present, no overflowing tables, and the winner row highlighted. Reading the PNG works on every platform, unlike reading the PDF. If no Chrome or Edge is found, deliver the Markdown and HTML and say so.

The report lists the G-facts and each persona's grounded vs assumed trait count, so a reader can judge how much of the panel rests on evidence.

### 9. Log and report

```bash
py scripts/calibration.py add <folder>/panel.json
```

This appends the prediction to the global `calibration-log.csv` in this skill's folder. Use `--log <path>` (before or after the subcommand) only when the user asks for a separate log or when testing. The log stores only the real options: the decoy is left out, because nobody will run it live.

Then tell the user: the predicted winner and its lead, the confidence label and why, any flags, the most useful objection, the live test, the file paths, and the run id they'll need to log the real result.

## Log result

When the user reports a real outcome ("B won, CTR 2.1% vs 1.4%"), find the run id with `py scripts/calibration.py list`, then:

```bash
py scripts/calibration.py record <run_id> <actual_winner_id> --note "<what happened>"
```

The winner must be one of the logged options. If the user reports results for only some options (e.g. "B beat A" when A, B, and C were tested), record the best reported option as the winner. Then say plainly in the note and to the user what you assumed about the unreported ones (e.g. "C not run live; assumed it lost"). If the live test ran a different set of options, ask before recording.

Then run **Score** and say whether the panel got it right.

## Score

```bash
py scripts/calibration.py score
```

Report the hit rate against the chance rate (1 ÷ number of real options, decoy excluded, averaged across resolved runs), the breakdown by confidence label, and how many runs are still pending. With fewer than 10 resolved runs, say the track record is too small to judge. If High-confidence runs aren't beating Low ones, say that the confidence labels aren't calibrated yet.
