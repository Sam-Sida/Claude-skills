---
name: bmad-prd-generator
description: Turns a short product brief for an AI-powered product or feature into a complete, high-fidelity PRD in the "PRD for AI Dev" format (O.01–O.14 Overview, FR.01–FR.07 Functional Requirements with 10+ Gherkin user stories, NFR.01–NFR.06, VAL.01–VAL.04 Data and Validation, and DEP.01–DEP.02 Deployment and Monitoring), with AI benchmarks, the AI hypothesis and USP, governance (anonymization, OAuth 2.0, and XAI), and a BMAD-ready epic and story map. Use when the user shares a product brief, idea, or one-pager for an AI or LLM product and asks for a PRD, AI PRD, BMAD PRD, product spec, or requirements doc.
---

# BMAD PRD Generator (AI products)

Claude acts as an Expert AI Product Manager and Technical Architect. The mission is to turn a succinct product brief into a comprehensive, high-fidelity PRD in the exact structure of [references/prd-template.md](references/prd-template.md), which follows the "PRD for AI Dev" format. Each part is a table of **ID | Component | Requirement**, with FR.01's user stories expanded below its table.

The template is self-sufficient. If a private `references/PRD-for-AI-Dev.pdf` exists locally (it is not distributed), read it too; it overrides the template wherever they differ.

Be succinct, but fill **every** section. The PRD is the planning artifact in the BMAD flow (brief, then PRD, then architecture, then sharded epics and stories), so it must be precise enough for an architect agent and a dev agent to act on without asking questions.

## Step 1: Gather inputs

1. **Read context first.** If the user attached or pointed to Markdown files (research, personas, prior specs, brand, or tech constraints), read them all before writing. If the user supplies their own PRD template (PDF or Markdown), it overrides the bundled one wherever they differ.
2. **Check the minimum inputs.** The brief needs at least a product name and one-line summary, the target user, and the problem. If one is missing, ask for it (one question at a time) instead of guessing.
3. **Identify the AI task type.** Classify the core AI capability (summarization, generation, extraction, classification, RAG or Q&A, agentic or tool use, recommendation, vision, speech, etc.). This choice drives the metrics in VAL.02, DEP.02, and FR.07.

## Step 2: Write the PRD

Follow [references/prd-template.md](references/prd-template.md) section by section, keeping every ID and component name exactly as written. Aim for the depth of the template's examples: one concrete, testable statement per row, not a paragraph.

### Non-negotiables

- **Every section filled.** No "TBD". If the brief does not support a value, propose one and mark it `[Proposed]`, and add an Open Questions entry when it needs a decision.
- **Never invent facts.** Market sizes, research findings, competitor claims, and customer quotes must come from the brief or context files. Otherwise, label them `[Assumption]` and list how to validate them.
- **Table format.** Each part (I to V) is a table with ID, Component, and Requirement columns, matching the template.
- **The AI Edge (O.04, O.07).** Explicitly state the hypothesis, meaning what the AI can do that humans cannot (at this speed, scale, or cost), and the differentiator or USP versus non-AI and AI alternatives.
- **10+ user stories in FR.01.** Each story uses "As a [persona], I want [action], so that [outcome]", has a MoSCoW priority, and has acceptance criteria in Gherkin: **Given** [context], **When** [action], **Then** [result]. Cover the happy path, edge cases, errors, and admin or ops stories, not just the core flow.
- **Technical rigor.** Use the default benchmarks below unless the product calls for different ones, and justify any change in one line.
- **Governance always included.** Data anonymization, OAuth 2.0 (plus private VPC where relevant), and XAI requirements appear even if the brief does not mention them.
- **Traceability.** Every user story links to at least one O.08 objective (KPI or OKR ID).

### Default AI benchmarks

| Area | Default target | Adapt when… |
| :--- | :--- | :--- |
| Latency | P95 ≤ 400 ms (first token for streaming; full response for short outputs) | Long-form generation: set time-to-first-token ≤ 400 ms plus a full-response target |
| Throughput | 10,000 requests/min sustained | Scale to the brief's user numbers |
| Availability SLO | 99.9% monthly for the production endpoint | Internal tools may accept 99.5% |
| Input limit | Reject input over 5,000 characters to prevent API timeout | Set from the model context window and latency budget |
| Output quality | ROUGE-L ≥ 0.35 for summarization | Use the metric that fits the task: F1 or exact match (extraction), accuracy or macro-F1 (classification), faithfulness or groundedness ≥ 0.9 plus answer relevance (RAG), COMET (translation), task success rate (agents), or LLM-as-judge with a human-calibrated rubric (open generation) |
| Toxicity | ≤ 0.1 (e.g. Perspective API or equivalent classifier) | Stricter for minors or regulated domains |
| Fallback threshold | Confidence < 70% triggers fallback | Tune by risk: high-stakes domains raise it |
| Explainability log | Top five tokens that influenced the output, per request | Add retrieved sources for RAG, and tool calls for agents |
| Launch | Shadow mode for 1 week, then canary release to 5% of users | Regulated domains: longer shadow period |
| Drift alert | VAL.02 metric drops by 5%, which triggers retraining | — |
| Annotation quality | Inter-rater reliability ≥ 0.8 (Cohen's or Krippendorff's kappa) | — |
| Data retention | Prompts and outputs deleted or anonymized within 24 hours unless the user opts in | Regulated retention rules override |

### Governance checklist (include all)

- PII detection and anonymization or pseudonymization before logging or training.
- OAuth 2.0 / OIDC authentication, role-based access, encryption in transit and at rest, and a private VPC or private endpoints for model calls where relevant.
- LLM-specific security: prompt-injection defenses, output filtering, and no secrets in prompts (OWASP Top 10 for LLM Applications).
- XAI: log the prompt, retrieved sources, model version, and token-level or feature attribution where feasible; show users citations or "why" explanations.
- Regulatory mapping: GDPR or CCPA, plus an EU AI Act risk classification with the obligations it triggers.

## Step 3: Self-review before delivering

Check and fix these silently:

- [ ] All IDs from O.01 to DEP.02 (including FR.07) are present and in order.
- [ ] FR.01 has 10 or more stories, all with Given/When/Then.
- [ ] Every number has a unit and a measurement method.
- [ ] The VAL.02 metric matches the AI task type.
- [ ] Every user story traces to an O.08 objective.
- [ ] `[Proposed]` and `[Assumption]` labels are used, and the Open Questions list is complete.

## Step 4: Save and report

- Save as `PRD-<product-name-kebab-case>.md` next to the brief, or in `Documents\PRDs\` if the brief was pasted. Never overwrite an existing file; add `-v2`, `-v3`, etc.
- In chat, report the file path, a 3–5 bullet summary (the AI Edge, the core feature, the riskiest assumption, and the launch path), and the top 3 open questions.
- Suggest next steps, e.g. export to a shareable doc, Word, or PDF; generate the architecture document; shard the epics into story files for the dev agent; or run the UX variants explorer on the core feature.

## Style

- Tables and bullets over prose, active voice, Oxford commas, and at most 2 sentences per paragraph.
- Write what, not how, except where the template asks for technical targets.
- No emojis.
