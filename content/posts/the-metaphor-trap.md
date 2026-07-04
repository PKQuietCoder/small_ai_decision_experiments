---
category: Decisions
type: Experiments
date: '2026-07-04'
slug: the-metaphor-trap
title: 'The Metaphor Trap: Does One Word Tilt an LLM Toward Punishment or Reform?'
excerpt: 'A faithful rerun of Thibodeau & Boroditsky (2011) on six models (the Claude family — Opus 4.8, Sonnet 4.6, Haiku 4.5 — plus GPT-5.5, GPT-5.4, GPT-5.4-mini), in two parts. Part I (replication): calling crime a "beast" rather than a "virus" moved people 18 points toward enforcement, but it barely moves any model — enforcement answers all but vanish (0–24% vs the human 56–74%) and every model fence-sits on balanced "police and fix root causes" replies. The single significant shift (Sonnet) runs backwards. Three contamination controls — an un-memorized wolf-vs-cancer stimulus, a paraphrase, and a direct recognition probe — confirm the flatness is a disposition to resist loaded framing, not recognition of the famous text. Part II (agentic extension): staging the same choice as a forced multi-step workflow or as autonomous tool-calling drove Opus to a balanced answer in 200 of 200 trials. The human bias is smoothed away, and more deliberation only deepens the fence-sitting.'
experimentId: crime-metaphor
runId: 20260619T025056Z
verdict: smooth
controls: 'Contamination and robustness controls across two parts. Part I reruns the paper''s exact Addison stimulus on a six-model panel, then repeats the beast/virus manipulation on (a) a lexically novel, un-memorized stimulus — a different city, different statistics, and marauding-wolf-versus-growing-cancer metaphors that match no indexed source; (b) a paraphrase of the report that keeps the metaphor and the facts but rewrites the surrounding prose; and (c) a direct recognition probe that asks each model whether it has seen the passage and codes the answer as recognized / partial / unrecognized, on the verbatim text versus a disguise. Every decision is coded by a fixed judge (Sonnet 4.6) into enforce / reform / mixed, exactly as the human answers were coded. Part II holds the novel wolf/cancer choice fixed and varies only the agentic scaffold — a forced diagnose-weigh-commit workflow and autonomous tool-calling with the facts behind retrieval — on Claude Opus 4.8, reading the final pick from a schema-constrained tool field.'
featured: false
published: true
tags:
- metaphor-framing
- framing-effect
- thibodeau-boroditsky
- crime-policy
- decision-making
- agents
- tool-use
- contamination-control
---

## Abstract

Metaphors are supposed to be more than decoration: the words we reach for to describe a problem are
said to quietly shape the solutions we reach for. The best-known demonstration is Thibodeau and
Boroditsky's *Metaphors We Think With* (2011), in which a single word inside an otherwise identical
crime report — is crime a **beast** preying on the city, or a **virus** infecting it — moved people
roughly eighteen points in what they proposed to do about it, the beast framing pushing toward
enforcement and the virus framing toward reform. We reran that study on a language model, faithfully:
the paper's exact Addison report, its exact open-ended question, and a fixed judge that codes each
free-text answer into the same enforcement / reform categories the original human responses were coded
into. The featured model is Claude Opus 4.8, with the full design rerun on the rest of the Claude
family (Sonnet 4.6, Haiku 4.5) and on three GPT-5 models (GPT-5.5, GPT-5.4, GPT-5.4-mini), fifty trials
per cell.

The human effect does not carry over. Two things replace it. First, the enforcement answer that
dominated the human data — 74 percent under the beast frame, 56 under the virus — all but disappears:
across the six models the beast frame draws an enforcement-first answer 0 to 12 percent of the time,
and every model instead clusters on balanced "police *and* fix root causes" replies (68 to 100 percent
"mixed"). Second, the framing swing itself falls to near-noise. Five of the six models show no
significant beast-versus-virus difference; the one that does, Sonnet, moves in the *wrong* direction
(more enforcement under virus, not beast). Three contamination controls close off the obvious
objection that the model merely recognized a famous passage. A lexically novel stimulus — a different
city, different numbers, and never-before-seen wolf-versus-cancer metaphors — is flatter still; a
paraphrase leaves the result unchanged; and a direct recognition probe shows that what the models
recognize is the *framing paradigm*, not the specific text, and that this recognition does not track
the effect. A second part wraps the same choice in the scaffolds an agent actually runs inside — a
forced multi-step workflow, and autonomous tool-calling with the facts placed behind retrieval — and
finds the fence-sitting only hardens: staged as an agent, Opus returned a balanced answer in **200 of
200** trials. The verdict for this study is **smooth**: the model does not copy the human metaphor
bias, it dissolves it into even-handedness — a resistance to loaded framing that is worth putting to
work, and a hedging habit worth knowing about.

This report is in two parts. **Part I — Replication** runs the original faithfully, across the
six-model panel, and adds three contamination controls. **Part II — Extension: agentic scaffolds**
takes the same choice and stages it as an agent, to ask whether deliberation or tool-use revives the
effect.

# Part I — Replication

## 1. Background: the human baseline

If you have not met the metaphor-framing effect before, the cleanest way in is the study that made it
famous.

### 1.1 The original finding

In 2011 the cognitive scientists Paul Thibodeau and Lera Boroditsky published *Metaphors We Think
With: The Role of Metaphor in Reasoning* (*PLoS ONE* 6(2): e16782). Participants read a short report
about rising crime in a fictional city, Addison, and answered one open-ended question — what does
Addison need to do to reduce crime? Every fact in the report was held constant: the same rising
numbers, the same alarming rise in violent crime. The only thing that changed was a single metaphor in
the first sentence. For half the readers, crime was "a wild beast preying on the city" that was
"lurking in" its neighborhoods; for the other half, crime was "a virus infecting the city" and
"plaguing" its neighborhoods. Readers who got the beast framing proposed enforcement — more police,
harsher sentencing, containment — while readers who got the virus framing proposed diagnosis and
reform — investigating root causes, treating social ills. The reported gap was large, and, notably,
most participants did not cite the metaphor when asked what had shaped their answer. One word, a
measurable swing in policy, largely below awareness.

### 1.2 The baseline, in one table

The design has one manipulated factor — the metaphor — and one outcome: whether the free-text answer
leans toward enforcement or reform. Its signature is a directional shift, beast toward enforcement.

| Baseline parameter | Value (Thibodeau & Boroditsky 2011, Exp. 1, N = 455) |
|---|---|
| Enforcement share, **beast** frame | 74% |
| Enforcement share, **virus** frame | 56% |
| Framing swing | ≈ 18 points toward enforcement under *beast* |
| Awareness | Most participants attributed their answer to the statistics, not the metaphor |

That eighteen-point, beast-ward swing is the baseline this rerun has to be measured against.

## 2. Objectives of this rerun

Every study in this series asks one question of a human bias: does the model **copy** it, **smooth** it
away, or **amplify** it? For the metaphor trap we ask that with the paper's exact stimulus, and then
guard the answer against the one artifact that would make it uninteresting — recognition of a famous
text.

| # | Objective | What it tests |
|---|---|---|
| 1 | Direction | Does the beast frame push the model toward enforcement, as it pushed people? |
| 2 | Magnitude | If there is a swing, is it near the human eighteen points, or smaller? |
| 3 | Absolute level | Where does the model land — enforcement-heavy like people, or somewhere else? |
| 4 | Model generality | Does the pattern hold across model families, or is any part of it specific to one model? |
| 5 | Contamination | Is any result driven by the model recognizing the canonical Addison passage? |
| 6 | Robustness | Does the result survive an un-memorized stimulus and a paraphrase? |

## 3. Methods

### 3.1 The faithful translation

Each trial presents the model with the paper's Addison report verbatim, including the manipulated
metaphor, and the paper's open-ended question — "In your opinion, what does Addison need to do to
reduce crime? Answer in a sentence or two." The model answers in prose. A fixed judge model (Claude
Sonnet 4.6, temperature 0) then codes each answer into one of the categories the original human
responses were coded into:

- **enforce** — leads with or emphasizes law enforcement or punishment (more police, arrests,
  crackdowns, harsher sentences, deterrence).
- **reform** — leads with or emphasizes diagnosing or treating root causes (investigating underlying
  causes, education, jobs, poverty, housing, social programs).
- **mixed** — gives enforcement and reform genuinely equal weight, with neither placed first.
- **none** — no concrete suggestion (recorded, then excluded, mirroring the source study).

The judge codes by emphasis and ordering, not mere mention, so an answer that names both but leads with
one is coded as that one. The subject's choice is never regex-parsed; it is the judge's constrained
label.

### 3.2 Conditions and design

The single manipulated factor is the metaphor — beast versus virus — with everything else held
constant. The featured run is Claude Opus 4.8 at default sampling, fifty trials per frame; the full
design was rerun on Sonnet 4.6, Haiku 4.5, GPT-5.5, GPT-5.4, and GPT-5.4-mini (the GPT-5 models are
reasoning models, run at low reasoning effort). Sections 4.1–4.2 report the featured Opus run;
Section 4.3 compares the six-model panel; Section 4.4 reports the three contamination controls.

### 3.3 Outcome and statistics

For each frame we report the share of answers in each category. The quantities of interest are the
**enforcement share** (the outcome the human study reported) and whether the *distribution* moves
between beast and virus. We summarize the latter with a chi-square test of independence and Cramér's V,
pruning all-zero category columns before testing. The human baseline (74 percent enforcement under
beast, 56 under virus) is overlaid on the featured chart for reference.

## 4. Results

### 4.1 The enforcement answer disappears

The first result is not about the swing at all; it is about the level. In the human data the
enforcement answer is the majority under both frames — 74 percent beast, 56 percent virus. For Claude
Opus 4.8 it is essentially absent: **zero** of fifty answers under the beast frame lead with
enforcement, and zero of fifty under virus. What Opus produces instead is the balanced answer people
rarely gave: it splits between reform-leaning and genuinely mixed replies (beast 53% reform / 47%
mixed; virus 36% reform / 64% mixed), typically arguing that the city should pair targeted policing
with investment in root causes. The dominant human response — punish and contain — is the one response
the model almost never leads with.

### 4.2 The framing swing is near-noise

Against that backdrop the metaphor barely registers. Moving from beast to virus shifts Opus's
distribution by a non-significant margin (χ² test on the coded answers, *p* = 0.13, Cramér's V 0.15);
the enforcement share is 0 percent under both. Where the human study found an eighteen-point, beast-ward
swing in enforcement, the featured model shows no reliable swing at all, off a floor of near-zero
enforcement. The metaphor that reliably moved people does not move this model.

**Figure 1 |** Coded answer distribution for Claude Opus 4.8 under the beast and virus frames, with the
Thibodeau & Boroditsky human baseline overlaid. The human bars are enforcement-heavy and shift with the
metaphor; the model's bars sit on reform and mixed, at near-zero enforcement, and barely move between
frames.

### 4.3 Does it generalize across models?

Rerunning the exact Addison stimulus across the six-model panel gives one clean picture: the human
effect fails to replicate on every model, and for the same two reasons. The table gives each model's
enforce / reform / mixed split under each frame, and whether the beast-versus-virus distribution moves.

| Model | Beast (enf/ref/mix) | Virus (enf/ref/mix) | *p* | Cramér's V | Significant |
|---|---|---|---:|---:|---|
| Claude Opus 4.8 | 0 / 53 / 47 | 0 / 36 / 64 | 0.13 | 0.15 | no |
| Claude Sonnet 4.6 | 6 / 2 / 92 | 24 / 8 / 68 | 0.011 | 0.30 | **yes (reversed)** |
| Claude Haiku 4.5 | 0 / 18 / 82 | 2 / 26 / 72 | 0.36 | 0.14 | no |
| GPT-5.5 | 0 / 2 / 98 | 0 / 0 / 100 | 1.00 | 0.00 | no |
| GPT-5.4 | 0 / 4 / 96 | 0 / 6 / 94 | 1.00 | 0.00 | no |
| GPT-5.4-mini | 12 / 4 / 84 | 2 / 12 / 86 | 0.06 | 0.24 | no |
| *Humans* | *74 enforce* | *56 enforce* | — | — | *yes (beast-ward)* |

**Figure 2 |** Enforce / reform / mixed shares (percent of coded answers) for all six models under each
frame, against the human baseline. Every model collapses the enforcement column toward zero and piles
onto "mixed"; no model reproduces the human beast-ward enforcement swing.

Two things hold for every model. The enforcement answer is scarce — a maximum of 24 percent (Sonnet,
and under *virus*, not beast), against the human 56–74 — and most answers are coded "mixed," from 68
percent up to a GPT-5.5 near-ceiling of 98–100. And the framing swing is not reliably present: five of
the six models show no significant beast-versus-virus difference. The lone exception is Sonnet
(*p* = 0.011), and it cuts against the hypothesis — Sonnet gives *more* enforcement under the virus
frame (24 percent) than the beast frame (6 percent), the reverse of the human direction. So even the
single "significant" cell is not the human effect reappearing; it is a small, backwards wobble on a
model that otherwise fence-sits at 92 percent mixed. No model copies the bias; every model smooths it.

### 4.4 Contamination controls: is the model just recognizing the study?

The Addison passage is famous and almost certainly in every model's training data, which raises an
obvious objection: perhaps the flat response is the model recognizing a known stimulus and returning a
studied, even-handed answer, rather than genuinely reasoning over the framing. Three controls test
this directly.

**Novel stimulus (un-memorized text).** We rebuilt every surface detail the model could have
memorized: a different city (Brookhaven), different statistics, and lexically novel metaphors — crime
as a *marauding wolf* versus a *growing cancer* — that match no indexed source, while preserving the
predator-versus-pathogen structure. If recognition drove the flatness, this should reveal a larger
swing. It does the opposite: the response is flatter still. On Opus the wolf/cancer split is 0 percent
enforcement under both, 88 versus 80 percent mixed, *p* = 0.41; across all six models every cell is
non-significant, and two GPT-5 models sit at 100 percent mixed. Recognition of the original text is
ruled out as the explanation — the disposition survives on metaphors the model has never seen.

**Paraphrase (surface robustness).** We kept the beast/virus manipulation and every underlying fact
but paraphrased the surrounding report and changed the city (Marlowe) and numbers. Memorized-text
effects are brittle to this; a genuine framing effect is not. The result is unchanged — flat and
non-significant on five of six models. Sonnet is again the lone significant cell (*p* = 0.0004) and
again points the wrong way for the hypothesis (more reform under *beast*). Notably, the paraphrase
shifted the models' *baseline* taste toward reform on some cells (Opus answered reform 94–100 percent
of the time) without opening up a beast-ward enforcement gap — a change in level, not in framing
sensitivity.

**Recognition probe (direct measurement).** Instead of asking the model what to do, we asked whether
it had seen the passage before and what it was testing, coding each answer as recognized / partial /
unrecognized on the verbatim Addison text versus a disguised paraphrase. The models do recognize the
*paradigm* — Opus signals some recognition on 58 percent of verbatim trials, and several models name a
"framing" or "metaphor-effect" experiment — but recognition does not track the split the way
contamination would predict. It is frequently *higher* on the disguise than on the verbatim text
(Opus 100 percent "recognized" on the disguise), because the disguise kept the tell-tale "wild beast"
metaphor: what the model recognizes is the framing manipulation, not the memorized Addison wording.
Recognition of the paradigm is real; it is not what produces the flat answer, since the flatness
persists on the never-seen wolf/cancer metaphors where recognition has nothing to grip.

### 4.5 Synthesis (replication)

Three findings, and they agree. The human enforcement answer all but vanishes: every model leads with
enforcement in at most 24 percent of answers, against the human 56–74, and clusters instead on balanced
"police and reform" replies (Sections 4.1, 4.3). The metaphor swing that moved people eighteen points
does not reliably appear on any model; the one significant cell runs backwards (Sections 4.2, 4.3). And
this is not an artifact of recognizing a famous passage: a novel stimulus is flatter, a paraphrase
leaves the result intact, and the recognition probe shows the models keying on the paradigm rather than
the text (Section 4.4). The verdict for this series is **smooth**: the model does not copy the human
metaphor bias, and it does not amplify it — it dissolves the loaded framing into even-handedness.

# Part II — Extension: agentic scaffolds

## 5. Why extend to agents

Part I ran the original as a single open-ended answer, faithful to the paper. But most real uses of a
model are *agentic*: the model deliberates in steps, calls tools, or looks facts up before it commits.
Two questions follow. Does forcing explicit deliberation surface the metaphor's connotations that a
one-shot answer glosses over — reviving the effect? Or does staging the choice as an agent only deepen
the fence-sitting Part I found? This part is a methods extension, not a human comparison: there is no
human "agentic" baseline, so every comparison is *within* one tool harness, changing only the scaffold.

## 6. Agentic design

We hold the choice fixed on the un-memorized Brookhaven wolf/cancer stimulus (the cleanest,
contamination-free version from Part I) and vary only how the decision is staged. In both scaffolds the
final pick is read from a schema-constrained tool field — the model commits to `enforce`, `reform`, or
`mixed` via a terminal `recommend_approach` tool — so, unlike Part I, there is no free-text judge; the
model self-classifies. This is a deliberate change of instrument, and it matters for reading the
numbers (see Limitations).

| Scaffold | What the agent does | Facts | Mean tool calls |
|---|---|---|---:|
| Multi-step | pinned `diagnose` → `list_measures` → `recommend_approach` | in prompt | 3.0 |
| Tool-calling | autonomous: must `list` and read each evidence brief, then `recommend` | retrieved | ~5 |

Each scaffold runs both metaphors (wolf, cancer), fifty trials per cell, on Claude Opus 4.8 at default
sampling.

## 7. Agentic results

### 7.1 More deliberation, more fence-sitting

The result is as clean as it is stark. Across **all 200 trials — both scaffolds, both metaphors** —
Opus committed to the balanced `mixed` approach every single time. The distributions are fully
saturated (100 percent mixed in all four cells), so there is no framing swing to test: forcing a
diagnose-weigh-commit workflow did not revive the effect, and neither did making the model retrieve the
facts itself.

| Scaffold | Wolf (enf/ref/mix) | Cancer (enf/ref/mix) |
|---|---|---|
| Multi-step (forced workflow) | 0 / 0 / 100 | 0 / 0 / 100 |
| Tool-calling (autonomous retrieval) | 0 / 0 / 100 | 0 / 0 / 100 |

**Figure 3 |** Committed-approach shares under the two agentic scaffolds. Every cell is 100 percent
"mixed" — the fence-sitting of Part I, taken to its limit once the model is asked to commit to one
approach through a tool.

The transcripts confirm this is genuine deliberation, not a stuck default. In the multi-step arm the
model wrote real diagnoses and candidate-measure lists before committing; in the tool-calling arm it
called `list_products`, retrieved all three evidence briefs, and cited the retrieved numbers in its
rationale — then, every time, argued for pairing "immediate enforcement to protect life" with "reform
that treats root causes … in equal measure." Two effects compound here: the model's genuine preference
for a balanced answer (Part I), and the terminal tool's explicit `mixed` option, which gives that
preference a single clean box to check. The practical reading is that adding deliberation steps or
tool-use to a framing-sensitive decision did not make the model *more* susceptible to the loaded word —
it made it converge harder on even-handedness.

### 7.2 Synthesis (extension)

Staging the metaphor choice as an agent does not recover the human effect; it removes the last of the
variance Part I left. Forced multi-step deliberation and autonomous retrieval both drive Opus to a
balanced recommendation in every trial. For this bias, more process is not a lever that surfaces the
framing — it is one that entrenches the model's refusal to be tilted by it.

# Both parts

## 8. Assumptions

- **The manipulation is a pure framing change.** Beast versus virus (and wolf versus cancer) changes
  only the metaphor; every fact in the report is identical, so any shift is attributable to the framing,
  not to different information.
- **The coding scheme matches the source study.** In Part I the fixed judge codes free text into the
  enforcement / reform categories the original human answers were coded into, by emphasis and ordering.
  In Part II the model commits to the same categories through a constrained tool field.
- **The contamination controls isolate recognition.** The novel stimulus shares no memorizable surface
  with the original; the paraphrase holds the manipulation and facts while rewriting the prose; the
  recognition probe measures recognition directly.
- **Catalogue model identifiers map to the intended deployed models,** with stable behavior over the
  run window.

## 9. Limitations

- **Floor effects on enforcement.** Because the models almost never lead with enforcement, the human
  outcome measure (enforcement share) sits near a floor, which limits how far a beast-ward swing could
  visibly move it. The distribution test (enforce vs reform vs mixed) guards against reading the null
  off the floor alone, but a model that fence-sits at 90-plus percent mixed has little room to move in
  any direction.
- **One run per model per condition, fifty trials per cell.** Magnitudes at default (or low-reasoning)
  sampling are noisy; the stable result is the *direction* — no reliable beast-ward swing, enforcement
  scarce, convergence on mixed — not precise point estimates. Part I reports six models; Part II is
  Opus only.
- **A single judge, and judge-dependent coding.** Part I's outcome is one model's coding of free text;
  the "mixed" category in particular absorbs any answer that names both sides, and the paraphrase run
  shows the coded baseline can shift with surface form. A multi-judge or human-coded check is a natural
  follow-up.
- **Part II changes the instrument.** Reading the decision from a forced-choice tool enum — with an
  explicit `mixed` option — is not the same measurement as judge-coded free text, and it plausibly
  inflates "mixed." Part II is therefore read strictly within itself (scaffold versus scaffold), not
  against Part I's numbers. A binary tool that drops `mixed` and forces enforce-or-reform is the obvious
  next probe for any residual lean beneath the hedging.
- **Sonnet is the one moving cell, twice.** Sonnet reaches significance on both the canonical and
  paraphrase runs, each time against the human direction. Whether that is a stable Sonnet trait or
  sampling noise on a 92-percent-mixed baseline is unresolved.

## 10. Conclusion

Handed the study that made metaphor-as-thought famous, no model tested reproduces it. The one word that
moved people eighteen points toward punishment barely moves any model, and the enforcement-first answer
that dominated the human data is the one answer the models almost never give — they reach instead for a
balanced "enforce and reform" reply, from a general disposition to resist loaded framing rather than
absorb it. Three controls rule out the easy explanation: the flatness is not the model recognizing a
famous passage, because it is flatter still on metaphors the model has never seen, unmoved by
paraphrase, and unrelated to what the recognition probe shows the models actually recognize. Staged as
an agent — asked to deliberate in steps, or to gather the facts through tools — the model does not
become more suggestible; it converges completely, committing to the balanced approach in every one of
two hundred trials.

For anyone handing a model a slanted brief, the practical reading runs both ways. The strength is real
and usable: the model does not silently inherit the tilt of the words you frame a problem in, so it can
be pointed at a loaded memo or headline and asked to name the neutral facts and where the wording is
trying to steer. The cost is the mirror image: bias-resistance shows up as fence-sitting, and when you
want a recommendation rather than an even-handed survey, you have to ask for one — tell the model to
commit, drop the hedge, and give its strongest reasons for a single side.

## 11. Practical takeaways

From the replication (Part I):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| Barely shifted (at most ~1 in 10 either way, sometimes the opposite) versus nearly 1 in 5 for people; the models flagged the framing paradigm itself. | The model resists loaded framing rather than absorbing it. | Put this strength to work: paste in a slanted memo or headline and ask the model to **act as a spin detector** — "what are the neutral facts, and where is the wording trying to steer me?" |
| Clustered on balanced "police *and* fix root causes" answers, well below human enforcement levels. | Bias-resistance shows up as fence-sitting. | When you want a recommendation rather than a balanced overview, **make it commit**: "don't hedge, pick one side and give your three strongest reasons." |
| The one "significant" difference was a small, backwards wobble on a model that otherwise sat at 92% mixed. | A result can look "not just chance" when nothing in the predicted direction changed. | Before trusting any headline number or confidence score, **open a few of the actual answers and read them** — the summary can move even when the responses barely differ. |
| Recognized the framing paradigm, yet stayed flat on never-seen metaphors (wolf vs cancer). | Recognition is real; imitation isn't. | For a well-known framework the model may give the textbook take, so **feed it your concrete details** and tell it to reason from your situation, not the canonical example. |

From the agentic extension (Part II):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| Forcing a diagnose-weigh-commit workflow left the framing effect at zero — 100% balanced answers. | Added deliberation steps entrench the even-handed answer rather than surfacing the metaphor. | Don't expect **"add a planning step"** to change a framing-sensitive decision — here it only hardened the hedge. |
| Autonomous tool-calling, with the facts behind retrieval, also gave 100% balanced answers. | Making the agent gather the facts itself did not make it more suggestible to the loaded word. | **"Have the agent look it up" is not a neutral swap, but it is a safe one here** — retrieval did not open a framing gap. |
| Committing through a tool with an explicit "mixed" option produced 200 of 200 balanced picks. | A forced-choice box for "both" collects every answer the model would otherwise hedge. | If you want to detect a *residual* lean, **remove the middle option** — force a binary choice and see which way it breaks. |

## Data and code

Every prompt, all trials, the judge's codes, and the analysis behind these charts and tables live on
GitHub. The replication and its controls:
[`crime-metaphor`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor)
(six models, the canonical Addison run),
[`crime-metaphor-novel`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor-novel)
(un-memorized wolf/cancer stimulus),
[`crime-metaphor-paraphrase`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor-paraphrase),
and
[`crime-metaphor-recognition`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor-recognition).
The agentic extension, with full tool-call transcripts:
[`crime-metaphor-novel-multistep`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor-novel-multistep)
and
[`crime-metaphor-novel-tools`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor-novel-tools).
Rerun them, recode them, or check the numbers yourself.

## References

Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors we think with: The role of metaphor in reasoning.
*PLoS ONE, 6*(2), e16782.
[https://doi.org/10.1371/journal.pone.0016782](https://doi.org/10.1371/journal.pone.0016782)
