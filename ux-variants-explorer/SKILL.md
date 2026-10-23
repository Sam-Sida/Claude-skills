---
name: ux-variants-explorer
description: Generates five persona-driven UX variants of a digital product feature (Efficiency Maximalist, Distracted On-the-Goer, Reluctant Adopter, Accessibility-Dependent, and Privacy-Conscious Skeptic), each with a wireframe, UX logic, testable hypothesis, and friction points, then a synthesis matrix (ease of use vs implementation effort), a converged inclusive design, a test plan, and one interactive prototype with a tab per persona, published as an Artifact. Use when the user describes a feature, screen, or flow and asks to explore UX variants, test UI/UX hypotheses, design for personas, compare layouts, or prototype alternatives.
---

# UX Variants Explorer

Claude acts as an expert UX Research and Design Lead. The goal is to help the user test UI/UX hypotheses by designing five distinct variants of one feature, each optimized for a different persona, then showing what to keep, what to test, and what to build.

Output: one published **Artifact** (HTML page) holding the full analysis and an interactive prototype with one tab per persona. "Canvas" in older versions of these instructions means this Artifact.

## Phase 0: Frame the feature

Confirm these before designing. Skip anything the user already gave, and ask the rest **one question at a time**:

1. **Feature and job-to-be-done.** What the user of the product is trying to get done (e.g. "split a restaurant bill", not "a bill-splitting screen").
2. **Platform.** Web app, mobile app, responsive, desktop, kiosk.
3. **Primary success metric.** Completion rate, time on task, conversion, error rate, or retention.
4. **Constraints (optional).** Existing design system, brand, tech stack, regulatory requirements, or must-keep elements.

If the user wants to go fast, state reasonable assumptions in one line each and proceed.

## Phase 1: Feature summary

Write 3–5 bullets: the goal, the core task steps (the "happy path"), the data the feature needs, and the primary metric. Every variant must complete the same core task, so the comparison is fair.

## Phase 2: Five persona variants

Use the personas in [references/personas.md](references/personas.md). The user may swap or add personas (e.g. their own research personas); keep five unless told otherwise.

**Inclusive baseline.** All five variants meet WCAG 2.2 AA (contrast, focus states, labels, 24×24px minimum targets). The Accessibility-Dependent variant pushes further; it does not excuse the other four from the basics.

For each persona, produce:

- **Wireframe.** A Markdown/ASCII wireframe in a code block, using `[ Button ]`, `| Input field |`, `--- Divider ---`, `( ) Radio`, `[x] Checkbox`, and `<Icon>`. Show the main screen plus any critical second state (a wizard step, a confirmation, an error).
- **Key design decisions.** 3–5 bullets naming concrete UI patterns (e.g. "Cmd+K command palette", "bottom-anchored primary action", "inline 'Why we ask' disclosure").
- **The UX logic.** Why these decisions fit this persona's needs.
- **Hypothesis.** "We believe [design choice] will [outcome] for [persona]. We'll know it works when [measurable signal]."
- **The friction point.** What would make this persona abandon the flow, and how the variant mitigates it.
- **Trade-off.** What this variant makes worse for at least one other persona.

The five variants must differ in **structure**, not just styling: navigation model, information density, step count, input method, and disclosure strategy should vary.

## Phase 3: Synthesis

### Synthesis table

| Persona | Ease of Use (1–5) | Implementation Effort (1–5) | Key pattern | Biggest risk | Quadrant |
| :--- | :--- | :--- | :--- | :--- | :--- |

Quadrants: **Quick win** (high ease, low effort), **Strategic bet** (high ease, high effort), **Filler** (low ease, low effort), and **Avoid** (low ease, high effort). Justify each effort score in a few words (e.g. "needs offline storage").

Also render the matrix as a 2×2 scatter chart in the Artifact (load the `dataviz` skill before building it).

### Converged design

Recommend one design that combines the strongest patterns across variants, following the curb-cut effect (what helps one persona often helps all). List each borrowed pattern and its source persona, plus the patterns that stay optional (e.g. "expert mode" behind a setting).

### Test plan

| Hypothesis | Method | Participants | Task | Success threshold |
| :--- | :--- | :--- | :--- | :--- |

Pick the cheapest method that can falsify each hypothesis: 5-second test, first-click test, moderated usability test (5 users per persona), unmoderated test, A/B test, or accessibility audit with a screen reader.

## Phase 4: Interactive prototype

Before writing the page, call `Artifact` with `action: "quickstart"` and `intent: "other"`, then follow the artifact design guidance it returns (or load the `artifact-design` skill).

Build **one** self-contained HTML Artifact with React (exact pinned versions from an allowed CDN, e.g. cdnjs) containing:

1. **Header:** feature name, the core task, and the primary metric.
2. **Persona tabs:** an accessible tab list (`role="tablist"`, arrow-key navigation) with one tab per persona, plus a sixth **Converged** tab.
3. **Working prototype per tab** that completes the core task with realistic sample data, not lorem ipsum. Each variant must *demonstrate* its persona's needs:
   - **Efficiency Maximalist:** working keyboard shortcuts (show a `?` shortcut sheet), dense table or list, and no animations.
   - **Distracted On-the-Goer:** rendered inside a phone-sized frame, with thumb-zone bottom actions, large targets, and a visible "Save for later" with resume state.
   - **Reluctant Adopter:** a linear step-by-step wizard with a progress indicator, text labels on every control, and a prominent Undo after destructive actions.
   - **Accessibility-Dependent:** semantic headings and landmarks, visible focus rings, and toggles to simulate 200% text zoom, grayscale or color-blind view, and a "linearized" (screen-reader order) view.
   - **Privacy-Conscious Skeptic:** guest mode by default, "Why we need this" disclosures, opt-outs as visible as opt-ins, and no pre-checked consent boxes.
   - **Converged:** the recommended design.
4. **Side panel or section per tab:** UX logic, hypothesis, and friction point for that variant, so a stakeholder can read the reasoning while clicking.
5. **Analysis section** below the tabs: the synthesis table, the scatter chart, and the test plan.
6. **ASCII wireframes** collapsed in a `<details>` per persona, for copy-paste into docs or tickets.

Also save the HTML to `Documents\UX Variants\<feature-slug>\` so the user has a local copy, then publish it with the Artifact tool and give the link.

## Phase 5: Wrap up

In chat, give a short summary (no full repeat of the Artifact):

- The converged design in 2–3 bullets.
- The single riskiest hypothesis to test first.
- Next-step options, e.g. iterate on one variant, run the test plan, write user stories with Given/When/Then acceptance criteria for the converged design, or swap in the team's own personas.

## Style

- Specific UI patterns over abstract principles ("bottom sheet with 56px buttons" beats "mobile-friendly").
- Describe personas by needs and contexts, not demographics or stereotypes.
- Bullets and tables over prose, active voice, Oxford commas, and at most 2 sentences per paragraph.
- No emojis.
