# Positioning & differentiation plan — "Borrowed Intuitions"

## Context

Three questions prompted this: is the blog a standout, who competes for common/semi-technical
readers, and how to make it (and how is it already) unique. This is a strategy brief, not a single
code change. Research (web + codebase) found:

- **Academic tier is crowded and rigorous but inaccessible.** A named field exists — "machine
  psychology" (Hagendorff) — with steady arxiv/Nature/Royal Society output on anchoring, framing,
  30-bias surveys (BIASBUSTER, arxiv 2412.00323), and the Royal Society "(Ir)rationality" paper.
  These are reviewer-facing PDFs, rarely reader-reproducible, and almost never cover agents.
- **Popular/semi-technical tier is thin.** A few Substacks (Bharat Chandar) and mainstream
  articles (Science, Cambridge personality test) — but one-off, no controls, no reproducible data.
  This is the underserved audience the blog targets.
- **The agentic angle is nearly empty.** The literature treats the LLM as a single-shot survey
  respondent. The blog's `agentic_budget` paradigm (multi-step tool use + autonomous condition)
  is ahead of the field; agent-bias papers only began appearing in late 2025.

**Verdict: genuinely standout, but on execution, not topic.** The defensible wedge is the
intersection of (1) agentic paradigm, (2) recognition/novel-stimulus controls, and (3)
plain-language reporting at journal-grade statistical rigor.

### The four published studies (current state)

| # | Study (post slug) | Classic replicated | Verdict | Model coverage |
|---|---|---|---|---|
| 1 | The Metaphor Trap (`the-metaphor-trap`) | Thibodeau & Boroditsky 2011, crime framing | **Smooth** | 6 models — Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.5 / 5.4 / 5.4-mini |
| 2 | When Budgeting Backfires (`budget-backfire`) | Larson & Hamilton 2012, pre-commit budget | **Smooth** | Opus 4.8 + Sonnet 4.6 (recognition control pending) |
| 3 | The Falsification Test (`wason-selection`) | Wason 1968 selection task | **Smooth** (strongest — model produces the normatively correct answer; holds across all six models) | 6 models — Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.5 / 5.4 / 5.4-mini (featured task) |
| 4 | The Decoy Effect (`decoy-effect`) | Huber, Payne & Puto 1982 attraction effect | **Copy** (first non-smooth result) — but provider-split: pronounced in Claude (full reversal in Sonnet/Haiku), weak-to-absent in GPT-5 (5.4 immune) | 6 models — Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.5 / 5.4 / 5.4-mini (featured laptop market) |

All four now carry a verdict badge and a "Controls" callout on their post pages (Tier 1, shipped).

**Tier 2 #4 — shipped (both phases).** Wason and decoy now span all six catalog models on their
featured experiments, with full cross-family sections added to both posts. Phase 1 added the Claude
family; Phase 2 added an OpenAI agentic engine (`_run_tool_sequence_openai` in
`server/experiments/llm_clients.py`, using the Responses API — GPT-5 reasoning models reject function
tools on Chat Completions) and the three GPT-5 runs. Findings:
- **Wason → smooth is universal.** All six models avoid the human confirming error; GPT-5.5 and GPT-5.4
  solve every condition at 100%. Strengthens the headline from "Opus solves it" to "frontier models
  solve it."
- **Decoy → copy is Claude-specific.** The attraction effect is *stronger* in Sonnet/Haiku (full
  0→100% reversal) than Opus (+37), and the Opus-only "autonomy dissolves it" caveat does **not**
  generalize. But GPT-5 largely resists: GPT-5.4 is immune, GPT-5.5 +13, mini +3. So the one "copy"
  result is model-dependent, not a universal LLM property.
- **Model brittleness.** Haiku is brittle on cold forced tool calls (49/120 null selections on the
  wason `direct` cell) so it is reported narratively, not in the wason table; no OpenAI model showed
  this. The featured Opus runIds (and verdict badges) are unchanged; all new data was run `--no-post`.

### How it is already unique (claim these explicitly)

1. **Agentic, not single-shot** — e.g. the decoy result where the bias appears under tool use but
   vanishes in the autonomous condition; the survey-style literature structurally can't produce this.
2. **Recognition controls as standard** — rules out "the model just recognized the famous puzzle,"
   the biggest unstated flaw in blog-tier (and much paper-tier) coverage.
3. **Reproducible by the reader** — code, prompts, per-trial JSON, downloadable package.
4. **A clean verdict vocabulary** — "copy / smooth / amplify" is a memorable, brandable frame.
5. **Trust-through-restraint presentation** — Wilson intervals + chi-square + human-baseline
   overlays in a calm Nature-style design with no hype.

### Where it is vulnerable

- Cross-model coverage on the *featured* experiments is now strong: metaphor, wason, and decoy all
  span the full six-model catalog across both providers (the agentic engine gained an OpenAI branch).
  Remaining gap: the *controls* (wason recognition/deontic, decoy storage-market) and the budget study
  are still single- or few-model, so the cross-family claims rest on the featured stimulus only.
- No multi-agent paradigms yet (ultimatum, Asch) — the most shareable experiments are still backlog.
- Discoverability: a file-based solo blog competes with arxiv on the same search terms.

## Differentiation moves (prioritized; each is independently shippable)

### Tier 1 — sharpen what already differentiates (low effort, high payoff)

1. **Lead with the agentic claim everywhere.** Update `content/site.yaml` tagline + `about` copy
   and the homepage hero to foreground "we test *agents*, not just chat answers — including a
   condition where the agent runs the decision itself." Competitors can't easily copy this. Keep
   the restrained design-system voice (`.claude/rules/design-system.md`).

2. **Make "copy / smooth / amplify" a first-class concept.** Give it a short explainer (about-page
   section or a tiny standalone page wired in `App.tsx`) and a recurring verdict badge on each post.

3. **Make the recognition-control story explicit and repeated.** Surface a standard "Controls"
   callout in every post template (`server/.../post_generator.py` for generated posts; hand-edit
   the curated ones): "the model might just recognize the famous puzzle — here's how we ruled it out."

### Tier 2 — close the credibility gaps

4. **Backfill cross-model runs on the single-model studies.** Wason and decoy ran only Opus 4.8.
   Re-run each across the catalog (`python -m server.run_experiment <id> --model <key>` per model,
   then a comparison table) so the headline becomes "do *LLMs*…". The metaphor study is the
   template. CLI is admin-only and must finish in one foreground shell call.
   - **Phase 1 (shipped):** Claude family (Sonnet, Haiku) added to both featured experiments; cross-
     model sections written into both posts.
   - **Phase 2 (shipped):** added OpenAI multi-turn tool support (`_run_tool_sequence_openai` in
     `server/experiments/llm_clients.py`, Responses API) and ran the three GPT-5 models on both
     featured experiments; both posts now carry full six-model cross-family tables. Headline is now "do
     *LLMs*…" on the featured stimulus. Open follow-up: extend the controls (recognition/deontic,
     storage-market) across the catalog too.

5. **Ship the first multi-agent experiment (ultimatum or Asch) from the roadmap.** The most
   shareable results; requires the new two-LLM engine branch noted in
   `.claude/plans/candidate-studies-roadmap.md`. Biggest leap in distinctiveness; scope separately.

### Tier 3 — distribution / discoverability

6. **Add a "how this differs from the papers" note** (about/methodology page): reader-reproducible,
   agentic, controls-first. Cite the field so the gap reads as deliberate.

7. **Per-post "replicate this" affordance.** The downloadable package already exists
   (`export_experiment`); surface a visible "download data + code to re-run" link on each post.

## Recommended starting point

Tier 1 (1–3) are pure content/UI edits in the existing design system — no engine work, no API
spend — and capture most of the positioning gain. Tier 2 #4 is the highest-value data work; Tier 2
#5 (multi-agent) is the highest-value new capability but a larger build.

## Critical files

- `content/site.yaml` — tagline, description, about copy (the positioning surface).
- `artifacts/client/src/pages/home.tsx`, `pages/about.tsx` — hero + about rendering.
- `artifacts/client/src/App.tsx` — route wiring if a new explainer/methodology page is added.
- `server/app/post_generator.py` (path per CLAUDE.md) — post template, for the Controls callout.
- `content/posts/*.md` — curated posts (hand-edit; `run_experiment` overwrites without `--no-post`).
- `.claude/plans/candidate-studies-roadmap.md` — multi-agent / cross-model backlog.

## Verification

- Content/UI changes: `pnpm run typecheck`, then run the client
  (`PORT=5173 BASE_PATH=/ pnpm --filter @workspace/client run dev`) and load home/about/post pages;
  confirm voice matches `design-system.md` (no emoji, sentence case, sharp corners).
- Confirm posts still load via `server.app.content_store.get_post(slug)`.
- Cross-model reruns: `run_experiment <id> --model <key> --no-post`, verify `parseFailures: 0`,
  inspect `content/analysis/<id>/<runId>.json` (`overall.testable`, per-model rows).
- Restart the `api-server` workflow after any server-side change (FastAPI caches module state).

## Competitive sources

- Royal Society, "(Ir)rationality and cognitive biases in LLMs" (2024).
- arxiv 2412.00323 — Cognitive Biases in LLMs: A Survey and Mitigation Experiments (BIASBUSTER).
- arxiv 2412.06593, 2511.05766 — anchoring bias experimental studies.
- Hagendorff — "machine psychology" framing.
- Bharat Chandar (Substack), "Can LLMs predict human behavior?"; Science, "Can AI chatbots replace
  human subjects in behavioral experiments?"; Cambridge personality-test coverage.
- Agentic-bias (late-2025): sunk-cost-in-agents (PMC12384923), 6G agentic networks (arxiv 2510.19973).
