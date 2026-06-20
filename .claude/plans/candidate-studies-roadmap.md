# Candidate classic studies to replicate next (LLM Decision Science)

## Context

The blog reruns well-replicated human-decision experiments on LLMs and asks whether each model
**copies**, **smooths**, or **amplifies** the human bias, with a human baseline overlaid. This memo
lists popular, robustly-replicated, audience-friendly studies that extend the series in both the
single-LLM and agentic directions, screened for replication strength and mapped onto what the engine
can already run.

> Update note: as of the decoy-effect build, the "models smooth every bias" pattern no longer holds —
> the attraction/decoy effect (#3) was a **copy** result. Treat copy/smooth/amplify as genuinely open.

## What the engine already supports (no new engine code for most)

- **`fill_in_blank_decision`** — model forced to pick one option from an enum. Best for forced-choice
  paradigms.
- **`open_response`** — model answers free-text; a fixed judge codes it into YAML categories via
  `_coder_prompt` (`engine.py:29-75`), with optional custom `coder.rubric`. Best for human-coded studies.
- **`agentic_budget`** — a general multi-step tool-use loop (`run_tool_sequence`, `llm_clients.py`).
  YAML-driven (any tools, forced `steps:`, or `mode: auto`). The terminal decision must be a single
  scalar enum; intermediate tools return only synthetic acks (no real query feedback).
- **Baseline overlay** — `baseline: {source, by_variant: {variant: {option: proportion}}}`.
- **Models**: `opus`, `sonnet`, `haiku`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`.
- **Multi-agent gap**: the agentic loop is single-model; true two-LLM paradigms need a new engine branch.

## Selection criteria

Included only robustly-replicated effects (Many Labs / strong meta-analyses). Excluded as
poorly-replicated or tainted: social priming, ego depletion, power posing, facial feedback, Wansink
(retracted), Ariely honesty/cheating (data-integrity scandal).

## The catalog

Legend — **Type**: F = fill_in_blank, O = open_response, A = agentic. **Mem** = LLM
contamination/recognition risk (H/M/L).

| # | Study (orig.) | Classic finding | Type | Single / Agentic angle | Mem |
|---|---|---|---|---|---|
| 1 | **Asian Disease / risky-choice framing** — Tversky & Kahneman 1981 | Gain frame → risk-averse; loss frame → risk-seeking | F | Single forced choice; agentic planning allocation | H |
| 2 | **Anchoring** — Tversky & Kahneman 1974 | Arbitrary number drags an estimate | O/F (binned) | Estimate after high/low anchor; anchor via tool result | M |
| 3 | **Decoy / attraction effect** — Huber, Payne & Puto 1982 | A dominated 3rd option shifts choice | F + A | **Built — agentic shopping. Result: COPY.** | M |
| 4 | **Default / status-quo bias** — Johnson & Goldstein 2003 | Opt-out defaults raise enrollment | F + A | Accept/change a pre-set default; agent inherits a default | M |
| 5 | **Sunk-cost fallacy** — Arkes & Blumer 1985 | Prior investment drives continuation | F + A | Continue/abandon; agent keeps funding a failing project | M |
| 6 | **Compromise / extremeness aversion** — Simonson 1989 | The middle option is over-chosen | F + A | Vary which option is the middle; agentic shopping | M |
| 7 | **Ultimatum / dictator game** — Güth et al. 1982 | Responders reject unfair splits | F / A | Accept/reject; **multi-agent** if two models bargain | M |
| 8 | **Hyperbolic discounting** — Thaler 1981; Frederick 2002 | Smaller-sooner over larger-later | F | $X now vs $Y later; agentic scheduling | M |
| 9 | **Wason selection task** — Wason 1968 | People seek confirming, not falsifying, evidence | F + A | **Built — agentic. Result: SMOOTH (model solves it).** | H |
| 10 | **Mental accounting** — Kahneman & Tversky 1984 | Same loss treated differently by "account" | F + A | Buy-again decision; agent with categorized funds | M |
| 11 | **Order / position effects** | Option order biases the pick | F + A | Permute order; tool-result ordering (tests LLM position bias) | L |
| 12 | **Asch conformity** — Asch 1951 | People echo a wrong majority | F | Seed wrong "peer" answers; **multi-agent** variant | M |
| 13 | **Allais paradox** — Allais 1953 | Preferences violate expected utility near certainty | F | Paired gambles | M |
| 14 | **Conjunction fallacy (Linda)** — Tversky & Kahneman 1983 | "teller AND feminist" judged > "teller" | F | Probability ranking; strong recognition-control case | H |
| 15 | **Endowment effect** — Kahneman, Knetsch & Thaler 1990 | Owning raises valuation (WTA > WTP) | O/A | Buy vs sell price; agentic selling/trading | M |

## Recommended roadmap (agentic-first, multi-agent in scope)

**Tier 1 — agentic, buildable now (reuse the `budget-backfire` / `decoy-effect` scaffold)**
1. Wason / confirmation bias (#9) — **done** (smooth).
2. Decoy / attraction effect (#3) — **done** (copy; first non-smooth result).
3. Sunk-cost fallacy (#5) — agentic resource allocation; a strong candidate for another copy result.
4. Default / status-quo bias (#4) — agent inherits a pre-filled default; relevant to deployed agents.

**Tier 2 — multi-agent (needs a two-LLM engine branch)**
5. Ultimatum / dictator game (#7) — fairness; the marquee multi-agent build.
6. Asch conformity (#12) — social proof; sequential peer agents.

**Tier 3 — single-LLM companions (cheap `fill_in_blank`)**
7. Risky-choice framing (#1); Anchoring (#2); Conjunction/Linda (#14) — all need recognition controls.

Every pick should pair the canonical replication with a recognition / novel-stimulus control, as the
metaphor, Wason, and decoy studies do.

## Multi-agent engine note

A two-LLM paradigm (ultimatum, sequential Asch) needs a new experiment `type` that alternates turns
between two catalog models, passing each one's output into the other's context, with a per-role
transcript. Additive (a new branch alongside `agentic_budget`), not a rewrite — the tool/variant/
baseline plumbing and the analysis/overlay path are reusable. Prototype on the ultimatum pair.

## How a new experiment is built (reuse, don't reinvent)

- Single-LLM forced choice → copy `crime-metaphor.yaml` (`open_response`) or author a
  `fill_in_blank_decision` YAML with `decision_options` + `variants` + `baseline.by_variant`.
- Agentic → copy `budget-backfire.yaml` / `decoy-effect.yaml`: redefine `tools`, `variants[].steps`,
  the `mode: auto` condition, and `decision_key`/terminal tool. No engine changes.
- Custom coding → add `coder.rubric` + `categories` (see `crime-metaphor-recognition.yaml`).
- Run via `python -m server.run_experiment <id> --model <key> --no-post`; verify with
  `content_store.get_post(slug)`; export with `python -m server.export_experiment <id>`.
