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

- Three of four studies run only Opus 4.8 — weakens "do *LLMs*…" to "does Opus…".
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
