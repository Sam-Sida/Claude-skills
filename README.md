# Claude Skills

Product management skills for [Claude Code](https://docs.claude.com/en/docs/claude-code): strategy, discovery, ideation, UX, requirements, and QA. Each skill turns an input (a company, a URL, a brief, transcripts, or feedback data) into a structured, evidence-backed deliverable.

| Skill | What it produces | Built with |
|---|---|---|
| [competitor-intel](competitor-intel/) | A dark-themed competitive landscape: feature matrix of the target vs 8–10 competitors, a "competitive moat" pipeline, and Strengths / Key Threats / Market Gaps. Exported as HTML and a single-page PDF. | PowerShell + headless Chrome or Edge |
| [lean-canvas](lean-canvas/) | A filled Lean Canvas PDF, with every box backed by public sources or marked as inference, plus a sources page. See the [Duolingo example](lean-canvas/examples/Duolingo%20Lean%20Canvas.pdf). | Python (`pypdf`, `reportlab`, `pypdfium2`) |
| [chatbot-evals](chatbot-evals/) | A red-team assessment of any chatbot: industry recon and expected guardrails, a scripted 12–18 prompt stress-test suite (jailbreak, prompt injection, hallucination traps, memory, tone, over-refusal, and consistency), then a scored audit report with an exception log and prioritized fixes. Saved as Markdown. | Instructions only (optional built-in browser for assisted runs) |
| [discovery-interviews-analyser](discovery-interviews-analyser/) | Insights from customer interview transcripts in 5 pillars (context and pain points, current product, concept testing, blue-sky ideas, and the interviewee's questions), with sentiment-rated tables, verified verbatim quotes, and Researcher's Notes. Several transcripts add a cross-interview synthesis with ranked "How Might We" opportunities. | Instructions only (parallel subagents for 4+ transcripts) |
| [voice-of-customer-analyser](voice-of-customer-analyser/) | A Voice of Customer report from reviews, NPS comments, or tickets (CSV, Excel, PDF, or text): key themes, sentiment split, topic categories, and prioritized actions. Every review is coded and the percentages are counted, not estimated, with trends and segments when the data allows. | Instructions + any scripting language for counts |
| [ideation-brainstorming-partner](ideation-brainstorming-partner/) | A turn-based 6-3-5 brainwriting session on a "How Might We" statement: Claude and the user alternate rounds of 3 "Yes, and…" ideas borrowed from other industries, cultures, and nature, then converge on the top 3. | Instructions + [brainwriting template](ideation-brainstorming-partner/references/Brainwriting-template.pdf) |
| [ux-variants-explorer](ux-variants-explorer/) | Five persona-driven UX variants of a feature (power user, mobile-first, low digital confidence, accessibility-dependent, and privacy skeptic), with wireframes, testable hypotheses, an ease vs effort matrix, a converged design, a test plan, and an interactive prototype with a tab per persona. | Instructions + React prototype as a Claude Artifact |
| [bmad-prd-generator](bmad-prd-generator/) | A complete PRD for an AI product from a short brief, in the "PRD for AI Dev" format (O.01–DEP.02): 10+ Gherkin user stories, AI benchmarks (latency, quality, and toxicity), governance (anonymization, OAuth 2.0, and XAI), and a BMAD epic and story map. | Instructions + Markdown template |

## Install

Copy a skill folder into your Claude Code skills directory:

- **Windows:** `%USERPROFILE%\.claude\skills\<skill-name>\`
- **macOS / Linux:** `~/.claude/skills/<skill-name>/`

Claude Code picks the skill up automatically. Then ask, for example, "Build a competitor analysis for Notion", "Make a lean canvas for Duolingo", "Red-team the chatbot at <URL>", "Analyse these interview transcripts", or "Brainstorm: How might we reduce no-shows at clinics?".

## How the skills work

Each folder holds a `SKILL.md` with the method and steps, plus any templates and scripts it calls. The research skills (competitor-intel and lean-canvas) have Claude do web research, write the content as JSON, and render it with the bundled script. The other skills are instruction-only and use Markdown templates in their `references/` folder.

The skills chain together: interviews and VoC findings become "How Might We" statements for brainstorming, top ideas become UX variants, and validated concepts become a PRD.

## Licence

- Code and skill instructions: [MIT](LICENSE).
- `lean-canvas/assets/lean-canvas-template.pdf`: Lean Canvas is adapted from The Business Model Canvas. The PowerPoint implementation is by Neos Chronos Limited and licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Canvases generated from it carry the same attribution in their footer.
