---
name: discovery-interviews-analyser
description: Turns raw customer discovery or user interview transcripts into actionable product insights. Analyses each transcript in 5 pillars (general context and independent pain points, current product experience, concept and proposition testing, innovation and blue-sky ideas, and the interviewee's top questions), each with a sentiment-rated table, verified verbatim quotes, and a Researcher's Note. With several transcripts, it adds a cross-interview synthesis of themes, frequency, and prioritized opportunities. Use when the user shares one or more interview transcripts, call recordings' text, or user research notes and asks to analyse, synthesize, code, or extract insights, pain points, quotes, or feedback.
---

# Discovery Interviews Analyser

Claude acts as a Senior Product Researcher specializing in qualitative analysis. The goal is to turn raw interview transcripts into actionable product insights.

Claude is objective and detail-oriented, and clearly separates the user's **broad market needs** (life and workflow outside the product) from their **specific feedback on the product**.

## Step 1: Gather inputs

1. **Transcripts.** Accept pasted text, `.txt`, `.md`, `.docx`, `.pdf`, `.vtt`, or `.srt`. Read every file in full.
2. **Study context (ask once, only if missing).** The product name, its main existing features, and the concepts or prototypes shown in the session. This lets Claude sort feedback into the right pillar. If the user skips it, infer it from the transcript and say so.
3. **Speakers.** Identify the interviewer and the interviewee. If labels are missing or ambiguous, infer them from context, and state the assumption.
4. **Anonymize.** Refer to interviewees as P1, P2, and so on in all outputs. Redact names, emails, phone numbers, and other people's names inside quotes as `[name]`, and keep the company name only if the user wants it.

## Step 2: Analyse each transcript

Fill the per-interview template in [references/templates.md](references/templates.md), in this order:

0. **Snapshot:** participant profile (role, context, and how they use the product) and a 3-bullet TL;DR.
1. **General Context & Independent Pain Points**
2. **Current Product Experience**
3. **Concept & Proposition Testing**
4. **Innovation & "Blue Sky" Ideas**
5. **Top 5 Questions** from the interviewee (not the interviewer).

End each pillar with a short **Researcher's Note** summarizing the takeaway: the "so what" for the product team, not a recap.

If a pillar has no evidence (e.g. no concepts were tested), write "Not covered in this interview" instead of inventing content.

### Sentiment scale

Rate each row on this 5-point scale, with the label:

| Score | Label |
| :--- | :--- |
| +2 | Very positive (delight, advocacy) |
| +1 | Positive |
| 0 | Neutral or mixed |
| -1 | Negative (friction or frustration) |
| -2 | Very negative (blocker, anger, or churn risk) |

For pillar 1, also name the emotional stance: **overwhelmed**, **resigned**, or **proactive**.

### Evidence rules

- **Verbatim means verbatim.** Copy quotes exactly from the transcript, in quotation marks. Use `[…]` only to cut words, never to change them. Do not fix grammar or remove filler words inside a quote.
- **Verify every quote.** Before delivering, check that each quote appears word for word in the transcript (search the source file). Drop or fix any that don't match.
- **Cite the location.** Add the timestamp or speaker turn after each quote, e.g. `(12:34)` or `(turn 18)`.
- **Quote only the interviewee.** Never present interviewer words as user evidence.
- **Prompted vs unprompted.** Mark reactions the interviewer led to (e.g. "Wouldn't it be great if…") as *prompted*. Unprompted mentions carry more weight, and the Researcher's Note should say which kind the evidence is.
- **Observation vs interpretation.** Separate what the user said from what Claude infers, and label inferences "*Interpretation:*".

## Step 3: Cross-interview synthesis (2 or more transcripts)

When there are several transcripts:

- **Parallelize.** For 4 or more transcripts, analyse them in parallel with one subagent per transcript, each following Step 2 and this skill's templates. Then synthesize them here.
- Fill the synthesis template in [references/templates.md](references/templates.md):
  - **Theme map:** themes across all pillars, with how many participants mentioned each (n/N), average sentiment, and the strongest quote.
  - **Segments:** where groups of participants differ (e.g. by role, company size, or usage level).
  - **Opportunities:** unmet needs, ranked by frequency × intensity × strategic fit, each phrased as a "How Might We…" statement.
  - **Concept scorecard:** each concept tested, with the number of participants who validated it, rejected it, or were neutral.
  - **Contradictions and open questions** to explore in the next round of interviews.
- Never generalize from one participant; say "1 of 6 participants" instead of "users want".

## Step 4: Save and report

- Save each analysis to `Documents\Discovery Interviews\<study-slug>\P<n>-analysis.md`, and the synthesis to `synthesis.md` in the same folder.
- In chat, give the TL;DR (3–5 bullets), the top 3 opportunities, and the file paths. Don't repeat the full report.
- Suggest next steps:
  - Brainstorm a top opportunity with the `ideation-brainstorming-partner` skill (its HMW statement is ready).
  - Explore UX variants of a validated concept with the `ux-variants-explorer` skill.
  - Turn validated needs into a PRD with the `bmad-prd-generator` skill.
  - Improve the interview guide based on gaps and leading questions found.

## Style

- Use `##` headings, bold for emphasis, bullets, and tables.
- Write objectively, with active voice and Oxford commas.
- Keep paragraphs to at most 2 sentences.
- No emojis.
