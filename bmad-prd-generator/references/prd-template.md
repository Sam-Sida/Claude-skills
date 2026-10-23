# PRD template (PRD for AI Dev format)

Each part is a table of **ID | Component | Requirement**. The guidance in italics describes each component and gives an example; replace it with the product-specific requirement.

Copy this structure exactly. Keep every ID and component name, fill every row, and use `<br>` for line breaks inside a cell.

```markdown
# PRD: <Product / Feature Name>

| Field | Value |
| :--- | :--- |
| Owner | |
| Status | Draft |
| Version | v1 |
| Last updated | <YYYY-MM-DD> |
| Source brief | <path or "pasted"> |
| AI task type | <summarization / RAG / extraction / classification / agentic / …> |

## I. Overview & Context (O.xx)

| ID | Component | Requirement |
| :--- | :--- | :--- |
| O.01 | Product Vision | *High-level, long-term aspiration and direction, in one sentence.* |
| O.02 | Target Users & Personas | *Primary audience, their role and context, and the existing access profile (e.g. RBAC role).* |
| O.03 | Problem Statement | **User problem:** …<br>**Why it's a problem:** *cost in time, money, or risk*<br>**Validation that it's a problem:** *evidence, or `[Assumption]` plus how to validate* |
| O.04 | Hypothesis | *The hypothesis de-risked through prototyping: what the AI can do that humans can't (speed, scale, consistency, or cost), stated so it can be proven wrong, with the experiment and pass threshold.* |
| O.05 | Goals | *The outcomes of the feature, 3–5 bullets.* |
| O.06 | Customer Value Proposition | *How we say it to the customer, in one line, e.g. "Get a reviewed shortlist in 24 hours".* |
| O.07 | Differentiator / USP | *The competitive differentiator versus manual work, incumbents, and other AI tools.* |
| O.08 | Business Objectives & Success Criteria | *Measurable outcomes as KPIs and OKRs, each with an ID (KPI-1, OKR-1), baseline, target, and timeframe.* |
| O.09 | Cost structure | *What drives cost (e.g. pages analyzed, tokens, human review), with the formula and an estimate per 1,000 units.* |
| O.10 | Pricing structure | *How we charge (included in plan, per seat, usage, or tiered) and the margin versus O.09.* |
| O.11 | Dependencies & Constraints | **Constraints:** *technical, budget, and market limits (e.g. must use a pre-trained LLM)*<br>**Dependencies:** *model provider, data availability, APIs, and teams* |
| O.12 | Risks & Assumptions | **Risks:** *each with likelihood, impact, and mitigation*<br>**Assumptions:** *each with how to validate (e.g. "User trusts the output")* |
| O.13 | User journey | *Where this experience sits in the journey: what the user is doing, the previous step, and the next step.* |
| O.14 | Out-of-scope | *Explicit exclusions for this release, plus future considerations.* |

## II. Functional Requirements (FR.xx)

| ID | Component | Requirement |
| :--- | :--- | :--- |
| FR.01 | Core Feature: "<name>" | *The primary function the user interacts with. Summary here; the full user stories go in FR.01 detail below.* |
| FR.02 | Instrumentation | *Metrics collected to monitor the feature (e.g. adherence to output range, time to generate, confidence, cost per request, and feedback rate), with dashboards and alert thresholds.* |
| FR.03 | Output Parameter Control | *Parameters users can set for the AI output (length in sentences or words, format, tone, and language), with defaults and limits.* |
| FR.04 | User Feedback Mechanism | *How feedback is captured to evaluate and retrain the model (upvote or downvote, reason codes, and free text) and where it flows.* |
| FR.05 | Error State Handling | *Expected behavior on bad input or failure (profanity, toxicity, timeouts, provider outage, or empty input), with the polite user-facing message and recovery action for each.* |
| FR.06 | Data Input Validation | *Rules for acceptable input: character or token limits (e.g. reject over 5,000 characters to prevent API timeout), file types, languages, PII detection, and prompt-injection screening.* |
| FR.07 | AI Fallback Strategy | *Behavior when the AI is uncertain: IF confidence < 70%, THEN [message or action]. Define how confidence is computed and whether to abstain, ask a clarifying question, route to a human, or fall back to rules.* |

### FR.01 detail: user stories (10 or more)

| ID | User story | Priority (MoSCoW) | Traces to |
| :--- | :--- | :--- | :--- |
| US.01 | As a [persona], I want [action], so that [outcome]. | Must | KPI-1 |

**Acceptance criteria (Gherkin)**

- **US.01**
  - Given [context], When [action], Then [result].
  - Given [edge case], When [action], Then [result].

## III. Non-Functional Requirements (NFR.xx)

| ID | Component | Requirement |
| :--- | :--- | :--- |
| NFR.01 | Latency/Performance | *Speed of the AI service, e.g. P95 model inference time ≤ 400 ms, plus P50 and P99 and time to first token if streaming.* |
| NFR.02 | Scalability & Load | *Capacity, e.g. sustained load of 10,000 requests per minute, plus peak, concurrency, and rate limits per tenant.* |
| NFR.03 | Reliability & Uptime (SLO) | *Availability target for the production endpoint (e.g. 99.9%), error budget, and degraded-mode behavior.* |
| NFR.04 | Explainability (XAI) Requirement | *Transparency of AI decisions: what gets logged for audit (e.g. the top five tokens that influenced the output, retrieved sources, model version, and prompt) and what the user sees (citations, confidence, or "why").* |
| NFR.05 | Data Governance & Privacy | *Compliance and data handling, e.g. all user input anonymized and deleted from temporary storage within 24 hours, plus training consent, residency, GDPR or CCPA, and EU AI Act classification.* |
| NFR.06 | Security & Authentication | *Access control and data protection, e.g. all model APIs secured via OAuth 2.0 and run in a private VPC, plus RBAC, encryption, and OWASP LLM Top 10 controls.* |

## IV. Data & Validation (VAL.xx)

| ID | Component | Requirement |
| :--- | :--- | :--- |
| VAL.01 | Training Data Specifications | *Source, size, format, and labeling quality (e.g. inter-rater reliability ≥ 0.8), plus train/eval/test split and refresh cadence.* |
| VAL.02 | Model Success Metrics | *Technical quality metrics that fit the task, e.g. ROUGE-L ≥ 0.35 on the test dataset for summarization. Name the eval set and frequency.* |
| VAL.03 | Ethical AI & Bias Mitigation | *Responsible development checks, e.g. automated check that no output exceeds a toxicity score of 0.1, plus bias tests across relevant groups, red-teaming, and hallucination rate.* |
| VAL.04 | Human Evaluation Rubric | *Subjective criteria for human testers, scored 1–5 with a pass threshold: Factuality, Tone Alignment, and Readability, plus any domain-specific ones.* |

## V. Deployment & Monitoring (DEP.xx)

| ID | Component | Requirement |
| :--- | :--- | :--- |
| DEP.01 | Launch Strategy (A/B Test/Rollout) | *How the product is released, e.g. shadow mode for 1 week, then a staged canary release to 5% of users, with the go/no-go metric and rollback trigger for each stage.* |
| DEP.02 | Monitoring & Retraining Plan | *Post-launch maintenance, e.g. alerts for model drift (if ROUGE-L drops by 5%) that trigger the automatic retraining pipeline, plus feedback review cadence and version rollback.* |

## Appendix

### A. Epic & Story Map (BMAD handoff)
| Epic | Stories | Depends on |

### B. Open Questions
| # | Question | Owner | Needed by |

### C. Glossary
```
