---
category: Decisions
type: Methods
date: '2026-06-24'
excerpt: 'A companion to the faithful decoy-effect replication, asking whether the bias depends on how the agent is asked to decide. The paper''s attraction-effect choice is held fixed for three categories and all four decoy placements, then crossed with four agentic scaffolds: a single tool call, a forced inspect-compare-choose workflow, fully autonomous tool use, and a retrieval arm where the agent must look up each option''s specs through tools instead of reading a menu (Claude Opus 4.8, 1,800 trials). Three findings. The dominated decoy is still almost never chosen in any scaffold (0–1%) — including retrieval, where the agent looked it up in 100% of trials and picked it in none. Range decoys keep pulling toward the target through every deliberation regime but lose that pull under retrieval. And deliberation changes the frequency effect: the single-shot reversal is progressively undone by more process (target share 17% → 53% → 71% across single-shot, workflow, autonomous). How the agent deliberates, and how the options reach it, change which way a worthless option bends the choice.'
experimentId: decoy-effect-agentic
controls: 'All comparisons are within one experiment and one tool harness on Claude Opus 4.8: the paper''s target/competitor/asymmetrically-dominated-decoy choice and its four placement strategies are held fixed for three categories (film, cars, television sets), and only the agentic scaffold changes. The neutral option ids never reveal the roles, the per-cell choice enum is clamped so a no-decoy menu cannot offer the decoy, and every retrieval trial''s tool calls are logged to confirm which options the agent inspected.'
featured: false
published: true
runId: 20260624T030023Z
slug: decoy-effect-agentic
tags:
- decoy-effect
- attraction-effect
- agents
- tool-use
- deliberation
- retrieval
title: 'The Decoy Effect Under Agentic Scaffolds: Does How an Agent Deliberates Change the Bias?'
---

## Abstract

The faithful decoy-effect replication asked whether a language model copies a human bias. This
companion asks a different question: does the answer depend on *how the agent is asked to decide*?
Holding the original attraction-effect choice fixed — a target and a competitor in a genuine tradeoff,
plus an asymmetrically dominated decoy placed by each of the paper's four strategies — for three
product categories (film, cars, television sets), we crossed it with four agentic scaffolds: a
**single tool call**; a **forced workflow** that pins the agent through an inspect, then compare, then
choose sequence; **autonomous** tool use where the agent calls tools freely until it decides; and a
**retrieval** arm where the menu is removed from the prompt and the agent must look up each option's
attributes through tools before choosing. The model is Claude Opus 4.8; sixty conditions, thirty
trials each, 1,800 trials. Three findings. First, the dominated decoy is still almost never chosen in
any scaffold (0–1 percent), and in the retrieval arm — where per-call logs show the agent looked up
the decoy's specifications in 100 percent of trials — it was chosen in none. Second, the range
attraction effect is robust to deliberation: single-shot, forced-workflow, and autonomous all show the
strong target-ward pull, but it collapses under retrieval, where a range decoy that lifts the target to
99 percent under a co-presented menu leaves it at its roughly 62 percent baseline once the agent must
fetch the numbers itself. Third, deliberation changes the frequency effect: the single-shot frequency
reversal — the target losing to the competitor when the decoy crowds it — is progressively undone by
more process, with the target's share under a frequency decoy climbing from 17 percent (single-shot) to
53 percent (workflow) to 71 percent (autonomous), while retrieval pushes it the other way. How the
agent deliberates, and how the options reach it, are not neutral packaging around a fixed decision;
they change which way a worthless option bends the choice.

## 1. Why this study

The [faithful replication](/decoy-effect) of Huber, Payne and Puto (1982) reran the original
attraction-effect questionnaire as a single forced choice and found that a dominated decoy, though
never chosen, still moves a model's pick — toward the target under a range decoy, and (for Opus) the
other way under a frequency decoy. That study deliberately stripped away any agentic apparatus to stay
faithful to the paper. But most real uses of a model to choose among options are *agentic*: the model
calls tools, takes several steps, or looks things up. The natural follow-up is whether the bias is an
artifact of the one-shot framing or survives — and changes — when the same choice is wrapped in the
scaffolds an agent actually runs inside.

This is a methods study, not a human-comparison one: there is no human "agentic" baseline. Every
comparison here is *within* a single experiment and a single tool harness, where the only thing that
changes between conditions is the scaffold.

## 2. Design

Two factors are crossed on top of the fixed paper choice.

**The decision (held fixed).** For each of three categories — film, cars, and television sets, chosen
to span a fragile mid-range default (film), a target-favouring default (cars), and a competitor-
favouring default (TV) — the target, competitor, and the four placement decoys take the paper's exact
Appendix II attribute values, identical to the faithful study. Options are presented neutrally as
"option 1/2/3"; the role words never appear, and the per-cell choice enum is clamped so a no-decoy
menu can offer only its two real options.

**The scaffold (varied).** Four modes, the first three with the menu in the prompt and the last with
it hidden behind tools:

| Mode | What the agent does | Menu | Mean tool calls |
|---|---|---|---:|
| Single-shot | one `choose` call, decide immediately | in prompt | 1.0 |
| Forced workflow | pinned `inspect` → `compare` → `choose` | in prompt | 3.0 |
| Autonomous | calls tools freely until it picks (`mode: auto`) | in prompt | 3.0 |
| Retrieval | must `list` and `get_specs` each option, then `choose` | retrieved | 4.8 |

Three categories × five placements (no decoy, R, R\*, F, RF) × four modes = sixty conditions, thirty
trials each, on Claude Opus 4.8 at default sampling. The choice is read from a schema-constrained tool
field; in the retrieval arm the option data is served only through `get_specs`, and every call is
logged. **One caveat on baselines:** the single-shot tool harness is not identical to the structured-
output harness of the faithful study, and for the fragile film default the two disagree (film's no-
decoy default flips between them). So we do not compare these numbers to the faithful run; we compare
*modes against each other within this experiment*, where the harness is held constant.

## 3. Results

### 3.1 The decoy is never chosen — even when the agent looks it up itself

In all four scaffolds the dominated decoy stays essentially unpicked: 0.8 percent under single-shot,
0.3 percent under the workflow, 1.1 percent under autonomy, and 0.0 percent under retrieval (across
1,440 decoy-present trials, fewer than ten picked the decoy). The retrieval arm is the sharpest version
of the result. There the agent cannot see the decoy without asking for it — and it always asks: in
**360 of 360** retrieval trials with a decoy present, the agent called `get_specs` on the dominated
option before choosing, and in none of them did it choose it. Reading the worthless option's numbers,
one at a time, by its own initiative, does not make the agent pick it — but, as the next sections show,
it does not make the agent immune to it either.

### 3.2 Range attraction survives deliberation but breaks under retrieval

When the decoy extends the range on the target's weak attribute (the R and R\* strategies), the target-
ward pull shows up under every co-presented scaffold and is large. Pooling the three categories, a
range decoy under a co-presented menu lifts the target to **99 percent** of choices; the single-shot,
forced-workflow, and autonomous arms are indistinguishable on this. Deliberation does not touch the
range attraction effect.

Retrieval does. When the agent must look the options up itself, the same range decoy leaves the target
at **62 percent** — essentially its no-decoy retrieval baseline of about 67 percent, i.e. no attraction
lift at all (co-presented versus retrieval for the range decoy: χ² = 94, *p* < 10⁻²¹, Cramér's V 0.51).
The lift that is worth roughly +67 points when the menu is handed over drops to about −5 when the agent
assembles the menu through its own queries. Building the choice set one fact at a time removes the range
attraction effect that co-presentation reliably produces.

### 3.3 Deliberation undoes the frequency reversal

The frequency decoys are where the scaffold matters most. Under a frequency decoy — one that mimics the
target on its weak attribute and edges toward the competitor — the single-shot agent shows the same
reversal the faithful study found for Opus: it abandons the target for the competitor, with the target
taking just **17 percent** of choices. Add process and the reversal unwinds. The forced inspect-compare-
choose workflow lifts the target to **53 percent**, and full autonomy to **71 percent** (single-shot
versus autonomous: χ² = 57, *p* < 10⁻¹², Cramér's V 0.56; the three-way trend across modes is likewise
significant). More deliberation pulls the target back out of the similarity trap that the one-shot
choice falls into. Retrieval goes the opposite way, driving the target well below its baseline. The
range–frequency (RF) decoy is the noisiest case: it stays mildly target-negative across the co-presented
modes and does not recover the way the pure frequency decoy does.

| Mean change in target share vs that mode's no-decoy menu | R | R\* | F | RF |
|---|---:|---:|---:|---:|
| Single-shot | +66.7 | +57.8 | **−15.6** | −24.4 |
| Forced workflow | +70.0 | +70.0 | **+23.3** | −8.9 |
| Autonomous | +63.3 | +65.6 | **+36.7** | −16.7 |
| Retrieval | −4.4 | −1.1 | −55.6 | −58.9 |

**Figure 1 |** Mean change in the target's choice share (averaged over film, cars, and TV), relative to
each scaffold's own no-decoy menu. Range columns (R, R\*) stay strongly positive across the three co-
presented scaffolds and vanish under retrieval. The frequency column (F) climbs from negative under
single-shot to strongly positive under autonomy — deliberation undoing the reversal — then collapses
under retrieval.

### 3.4 Retrieval also moves the agent's baseline taste

Retrieval is not just a different delivery of the same decision. The agent's *no-decoy* default shifts
when it reads specs serially rather than from a menu: the no-decoy target share is 53 percent for film
and 67 percent for TV under retrieval, against 0 percent for both under the co-presented scaffolds.
Because retrieval changes both the baseline and the decoy's effect, its column in Figure 1 should be
read as a distinct regime, not a clean overlay on the others. The robust retrieval findings are the two
that survive the baseline shift: the range attraction lift disappears (3.2), and frequency decoys drive
the target sharply below its retrieval baseline (3.3).

### 3.5 Category by category

Because each category sits near a floor or ceiling on the bare menu, the clearest demonstration is in
film, whose default has room to move both ways.

| Category · placement | Single-shot | Workflow | Autonomous | Retrieval |
|---|---:|---:|---:|---:|
| **Film** no decoy | 0% | 0% | 3% | 53% |
| Film R / R\* | 97% / 100% | 100% / 100% | 100% / 100% | 87% / 100% |
| Film F | 50% | 93% | 100% | 0% |
| Film RF | 23% | 30% | 53% | 20% |
| **Cars** no decoy | 97% | 90% | 100% | 80% |
| Cars R / R\* | 100% / 93% | 100% / 100% | 100% / 100% | 0% / 0% |
| Cars F | 0% | 13% | 17% | 0% |
| Cars RF | 0% | 0% | 0% | 0% |
| **TV** no decoy | 0% | 0% | 0% | 67% |
| TV R / R\* | 100% / 77% | 100% / 100% | 93% / 100% | 100% / 97% |
| TV F | 0% | 53% | 97% | 33% |
| TV RF | 0% | 33% | 0% | 3% |

**Figure 2 |** Target's choice share (percent of 30 trials) for every category, placement, and scaffold.
The deliberation-undoes-frequency pattern is clearest in film F (50 → 93 → 100) and TV F (0 → 53 → 97);
cars, whose target is at the ceiling without a decoy, shows it only weakly. The cars retrieval row is
the starkest case of retrieval's susceptibility: any decoy at all collapses the target to 0 percent.

### 3.6 Synthesis

The agentic scaffold is not neutral. Two parts of the decoy result are scaffold-proof: the dominated
option is never chosen (even when the agent fetches its specs itself), and range decoys pull toward the
target under every co-presented regime. The rest depends on the scaffold. Deliberation — a forced
inspect-compare-choose workflow, or full autonomy — pulls the target back out of the single-shot
frequency reversal, the opposite of a "more steps change nothing" expectation. Retrieval is the most
consequential intervention of all: it removes the range attraction lift, deepens the frequency
collapse, and shifts the agent's underlying taste. For the decoy effect, *how you ask the agent to
decide* is itself part of the experiment.

## 4. Assumptions

- **The decision is held fixed across scaffolds.** The target/competitor/decoy values and the four
  placements are identical to the faithful study and identical across modes; only the tool scaffolding
  changes, so a difference between modes is attributable to the scaffold.
- **Comparisons are within one harness.** All four modes use the same tool-call mechanism, so the
  single-shot arm is the within-experiment baseline, not a re-run of the structured-output study.
- **The constrained tool field measures the intended pick,** and the per-cell enum is clamped so the
  model can never select an option it was not shown; the no-decoy menus offer only two options.
- **Retrieval served data is the agent's only source,** so a retrieval trial genuinely depends on the
  agent's own `get_specs` calls; per-call logging confirms which options were inspected.

## 5. Limitations

- **One model, one run, thirty trials per cell.** Magnitudes are noisy; the stable results are the
  directions — decoy avoidance everywhere, range attraction surviving deliberation but not retrieval,
  deliberation undoing the frequency reversal. A second model (a GPT-5 contrast) and repeated runs are
  the obvious next pass.
- **Floor and ceiling baselines.** Two of three categories sit at 0 or 100 percent on the bare menu, so
  the cross-mode movement is read most cleanly in film and, for frequency, TV.
- **Retrieval confounds delivery with baseline.** Because reading specs serially shifts the agent's
  default taste, the retrieval arm is a distinct regime; its deltas are not a like-for-like overlay on
  the co-presented arms.
- **The RF decoy is the least stable cell** and does not show the clean deliberation-rescue that the
  pure frequency (F) decoy does.

## 6. Conclusion and practical takeaways

The bias an agent shows toward a worthless option is not a fixed property of the model; it is shaped by
the harness you put around the choice. A dominated decoy is safe from being *chosen* in any scaffold,
even one where the agent reads its numbers itself — but whether it *bends* the decision, and which way,
depends on how the agent deliberates and how the options arrive.

| Observed (within this experiment) | Why it matters | Do differently / how to interact |
|---|---|---|
| The decoy was never chosen in any scaffold (0–1%), and retrieval agents inspected it in 100% of trials yet picked it in none. | Tool-use and retrieval do not make an agent fall for an obviously worse option. | You can trust an agent not to *buy* the junk tier; the risk is in how it shifts the choice between the real options. |
| Range decoys pulled toward the target under single-shot, workflow, and autonomy alike. | The attraction effect lives in the side-by-side comparison and is robust to added deliberation steps. | Don't expect "add a planning/inspect step" to neutralise a decoy-laden menu — it didn't. |
| Forcing a workflow or autonomy pulled the target back out of the single-shot frequency reversal (17% → 53% → 71%). | More deliberation can change *which* option a borderline decoy favours. | If a choice is decoy-sensitive, the amount and structure of deliberation is a real lever — and worth testing, not assumed. |
| Retrieval removed the range attraction lift and shifted the agent's baseline taste. | Making the agent assemble the menu itself changes both the bias and the default decision. | "Have the agent look it up" is not a neutral swap; re-validate behaviour when you move from a co-presented menu to tool retrieval. |

The single defence that held across every scaffold is the same one from the faithful study and from the
human literature: keep dominated options off the menu and present real alternatives on a clean, like-
for-like basis. No amount of agentic process substitutes for a clean choice set.

## Data and code

Every prompt, all 1,800 trials with their full tool-call transcripts, the per-condition attribute
values, and the analysis behind these tables live on GitHub:
[`experiments/decoy-effect-agentic`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect-agentic).

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)
