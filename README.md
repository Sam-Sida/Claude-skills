# Claude Skills

Product-strategy and QA skills for [Claude Code](https://docs.claude.com/en/docs/claude-code). Each skill turns a company name or URL into a research-backed deliverable.

| Skill | What it produces | Built with |
|---|---|---|
| [competitor-intel](competitor-intel/) | A dark-themed competitive landscape: feature matrix of the target vs 8–10 competitors, a "competitive moat" pipeline, and Strengths / Key Threats / Market Gaps. Exported as HTML and a single-page PDF. | PowerShell + headless Chrome or Edge |
| [lean-canvas](lean-canvas/) | A filled Lean Canvas PDF, with every box backed by public sources or marked as inference, plus a sources page. See the [Duolingo example](lean-canvas/examples/Duolingo%20Lean%20Canvas.pdf). | Python (`pypdf`, `reportlab`, `pypdfium2`) |
| [chatbot-evals](chatbot-evals/) | A red-team assessment of any chatbot: industry recon and expected guardrails, a scripted 12–18 prompt stress-test suite (jailbreak, prompt injection, hallucination traps, memory, tone, over-refusal, and consistency), then a scored audit report with an exception log and prioritized fixes. Saved as Markdown. | Instructions only (optional built-in browser for assisted runs) |

## Install

Copy a skill folder into your Claude Code skills directory:

- **Windows:** `%USERPROFILE%\.claude\skills\<skill-name>\`
- **macOS / Linux:** `~/.claude/skills/<skill-name>/`

Claude Code picks the skill up automatically. Then ask, for example, "Build a competitor analysis for Notion" or "Make a lean canvas for Duolingo", or "Red-team the chatbot at <URL>".

## How the skills work

Each folder holds a `SKILL.md` with the research method and build steps, plus the scripts and templates it calls. Claude does the web research, writes the content as JSON, and the bundled script renders it into the final PDF.

## Licence

- Code and skill instructions: [MIT](LICENSE).
- `lean-canvas/assets/lean-canvas-template.pdf`: Lean Canvas is adapted from The Business Model Canvas. The PowerPoint implementation is by Neos Chronos Limited and licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Canvases generated from it carry the same attribution in their footer.
