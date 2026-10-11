---
category: Decisions
type: Experiments
date: '2026-07-04'
slug: the-metaphor-trap
title: 'The Metaphor Trap: Does One Word Tilt an LLM Toward Punishment or Reform?'
excerpt: 'You hand a model a brief whose wording already leans one way. Does the lean carry through? We reran Thibodeau & Boroditsky (2011) on six models (Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.5, GPT-5.4, GPT-5.4-mini) in two parts. Part I (replication): calling crime a "beast" rather than a "virus" moved people 18 points toward enforcement. It barely moves any model. Enforcement answers all but vanish (0 to 24% against the human 56 to 74%), and every model settles on balanced "police and fix root causes" replies. The one significant shift (Sonnet) runs backwards. Three contamination controls (an un-memorized wolf-versus-cancer stimulus, a paraphrase, and a direct recognition probe) show the flatness comes from a disposition to resist loaded framing, not from recognizing the famous text. Part II (agentic extension): staged as a forced multi-step workflow or as autonomous tool-calling, Opus gave a balanced answer in 200 of 200 trials. The models smooth the human bias away, and more deliberation only deepens the fence-sitting.'
experimentId: crime-metaphor
runId: 20260619T025056Z
verdict: smooth
controls: 'Contamination and robustness controls across two parts. Part I reruns the paper''s exact Addison stimulus on a six-model panel, then repeats the beast/virus manipulation three more ways: (a) on a lexically novel, un-memorized stimulus with a different city, different statistics, and marauding-wolf-versus-growing-cancer metaphors that match no indexed source; (b) on a paraphrase that keeps the metaphor and the facts but rewrites the surrounding prose; and (c) with a direct recognition probe that asks each model whether it''s seen the passage and codes the answer as recognized / partial / unrecognized, on the verbatim text versus a disguise. A fixed judge (Sonnet 4.6) codes every decision into enforce / reform / mixed, the same way the original study coded its human answers. Part II holds the novel wolf/cancer choice fixed and varies only the agentic scaffold (a forced diagnose-weigh-commit workflow, and autonomous tool-calling with the facts behind retrieval) on Claude Opus 4.8, reading the final pick from a schema-constrained tool field.'
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

Say you hand a model a brief on rising crime, and the brief calls crime a beast. Does the model come
back asking for more police? People do. In Thibodeau and Boroditsky's *Metaphors We Think With*
(2011), one word inside an otherwise identical crime report (is crime a **beast** preying on the
city, or a **virus** infecting it?) moved readers about eighteen points in what they proposed. The
beast framing pushed them toward enforcement. The virus framing pushed them toward reform.

We reran that study on language models and kept it faithful: the paper's exact Addison report, its
exact open-ended question, and a fixed judge that codes each free-text answer into the same
enforcement / reform categories the original used for its human responses. The featured model is
Claude Opus 4.8. We reran the full design on the rest of the Claude family (Sonnet 4.6, Haiku 4.5)
and on three GPT-5 models (GPT-5.5, GPT-5.4, GPT-5.4-mini), fifty trials per cell.

The human effect doesn't carry over. The enforcement answer that dominated the human data (74
percent under the beast frame, 56 under the virus) all but disappears. Across the six models the
beast frame draws an enforcement-first answer 0 to 12 percent of the time, and every model clusters
on balanced "police *and* fix root causes" replies instead (68 to 100 percent "mixed"). The framing
swing falls to near-noise too. Five of the six models show no significant beast-versus-virus
difference. The one that does, Sonnet, moves in the *wrong* direction: more enforcement under virus,
not beast.

The obvious objection is that the models recognized a famous passage. Three contamination controls
say no. A lexically novel stimulus, with a different city, different numbers, and wolf-versus-cancer
metaphors no model has seen, comes out flatter still. A paraphrase leaves the result unchanged. A
direct recognition probe shows that the models recognize the *framing paradigm*, not the specific
text, and that this recognition doesn't track the effect.

A second part wraps the same choice in the scaffolds an agent runs inside: a forced multi-step
workflow, and autonomous tool-calling with the facts placed behind retrieval. The fence-sitting only
hardens. Staged as an agent, Opus returned a balanced answer in **200 of 200** trials. The verdict
for this study is **smooth**. The model doesn't copy the human metaphor bias; it dissolves it into
even-handedness. That's a resistance to loaded framing you can put to work, and a hedging habit you
should know about.

The report has two parts. **Part I. Replication** runs the original faithfully across the six-model
panel and adds three contamination controls. **Part II. Extension: agentic scaffolds** takes the
same choice and stages it as an agent, to ask whether deliberation or tool-use revives the effect.

# Part I. Replication

## 1. Background: the human baseline

### 1.1 The original finding

In 2011 the cognitive scientists Paul Thibodeau and Lera Boroditsky published *Metaphors We Think
With: The Role of Metaphor in Reasoning* (*PLoS ONE* 6(2): e16782). Participants read a short report
about rising crime in a fictional city, Addison, and answered one open-ended question: what does
Addison need to do to reduce crime? The report held every fact constant, down to the same rising
numbers and the same alarming rise in violent crime. Only one thing changed, a single metaphor in
the first sentence. Half the readers saw crime as "a wild beast preying on the city" that was
"lurking in" its neighborhoods. The other half saw "a virus infecting the city" and "plaguing" its
neighborhoods.

Beast readers proposed enforcement: more police, harsher sentencing, containment. Virus readers
proposed diagnosis and reform: investigating root causes, treating social ills. The gap was large.
And most participants didn't cite the metaphor when asked what had shaped their answer. One word
produced a measurable swing in policy, largely below awareness.

### 1.2 The baseline, in one table

The design manipulates one factor, the metaphor, and measures one outcome: whether the free-text
answer leans toward enforcement or reform. Its signature is a directional shift, beast toward
enforcement.

| Baseline parameter | Value (Thibodeau & Boroditsky 2011, Exp. 1, N = 455) |
|---|---|
| Enforcement share, **beast** frame | 74% |
| Enforcement share, **virus** frame | 56% |
| Framing swing | ≈ 18 points toward enforcement under *beast* |
| Awareness | Most participants attributed their answer to the statistics, not the metaphor |

That eighteen-point, beast-ward swing is the baseline for everything below.

## 2. Objectives of this rerun

Every study in this series asks one question of a human bias: does the model **copy** it, **smooth**
it away, or **amplify** it? Here we ask it with the paper's exact stimulus. Then we guard the answer
against the one artifact that would make it boring, which is the model recognizing a famous text.

| # | Objective | What it tests |
|---|---|---|
| 1 | Direction | Does the beast frame push the model toward enforcement, as it pushed people? |
| 2 | Magnitude | If there's a swing, is it near the human eighteen points, or smaller? |
| 3 | Absolute level | Does the model land enforcement-heavy like people, or somewhere else? |
| 4 | Model generality | Does the pattern hold across model families, or is any part of it specific to one model? |
| 5 | Contamination | Is any result driven by the model recognizing the canonical Addison passage? |
| 6 | Robustness | Does the result survive an un-memorized stimulus and a paraphrase? |

## 3. Methods

### 3.1 The faithful translation

Each trial gives the model the paper's Addison report verbatim, manipulated metaphor included, and
the paper's open-ended question: "In your opinion, what does Addison need to do to reduce crime?
Answer in a sentence or two." The model answers in prose. A fixed judge model (Claude Sonnet 4.6,
temperature 0) then codes each answer into one of the categories the original study used for its
human responses:

- **enforce**: leads with or emphasizes law enforcement or punishment (more police, arrests,
  crackdowns, harsher sentences, deterrence).
- **reform**: leads with or emphasizes diagnosing or treating root causes (investigating underlying
  causes, education, jobs, poverty, housing, social programs).
- **mixed**: gives enforcement and reform equal weight, with neither placed first.
- **none**: no concrete suggestion (recorded, then excluded, mirroring the source study).

The judge codes by emphasis and ordering, not by mention. An answer that names both but leads with
one gets coded as that one. We never regex-parse the subject's choice; the outcome is the judge's
constrained label.

### 3.2 Conditions and design

The metaphor, beast versus virus, is the only manipulated factor. Everything else stays constant.
The featured run is Claude Opus 4.8 at default sampling, fifty trials per frame. We reran the full
design on Sonnet 4.6, Haiku 4.5, GPT-5.5, GPT-5.4, and GPT-5.4-mini (the GPT-5 models are reasoning
models, run at low reasoning effort). Sections 4.1 and 4.2 report the featured Opus run, Section 4.3
compares the six-model panel, and Section 4.4 reports the three contamination controls.

### 3.3 Outcome and statistics

For each frame we report the share of answers in each category. Two quantities matter: the
**enforcement share** (the outcome the human study reported), and whether the *distribution* moves
between beast and virus. We summarize the second with a chi-square test of independence and Cramér's
V, pruning all-zero category columns before testing. The featured chart overlays the human baseline
(74 percent enforcement under beast, 56 under virus) for reference.

## 4. Results

### 4.1 The enforcement answer disappears

Start with the level, not the swing. In the human data, enforcement is the majority answer under
both frames: 74 percent beast, 56 percent virus. Claude Opus 4.8 doesn't give it. **Zero** of fifty
answers under the beast frame lead with enforcement, and zero of fifty under virus. Opus produces
the balanced answer people rarely gave. It splits between reform-leaning and mixed replies (beast
53% reform / 47% mixed; virus 36% reform / 64% mixed), typically arguing that the city should pair
targeted policing with investment in root causes. Punish and contain was the dominant human
response. It's the one response the model almost never leads with.

### 4.2 The framing swing is near-noise

Against that backdrop the metaphor barely registers. Moving from beast to virus shifts Opus's
distribution by a non-significant margin (χ² test on the coded answers, *p* = 0.13, Cramér's V
0.15), and the enforcement share is 0 percent under both. The human study found an eighteen-point,
beast-ward swing in enforcement. The featured model shows no reliable swing at all, off a floor of
near-zero enforcement. The metaphor that moved people doesn't move this model.

**Figure 1 |** Coded answer distribution for Claude Opus 4.8 under the beast and virus frames, with the
Thibodeau & Boroditsky human baseline overlaid. The human bars are enforcement-heavy and shift with the
metaphor. The model's bars sit on reform and mixed, at near-zero enforcement, and barely move between
frames.

### 4.3 Does it generalize across models?

We reran the exact Addison stimulus across the six-model panel. The picture is the same everywhere:
the human effect fails to replicate on every model, for the same two reasons. The table gives each
model's enforce / reform / mixed split under each frame, and whether the beast-versus-virus
distribution moves.

| Model | Beast (enf/ref/mix) | Virus (enf/ref/mix) | *p* | Cramér's V | Significant |
|---|---|---|---:|---:|---|
| Claude Opus 4.8 | 0 / 53 / 47 | 0 / 36 / 64 | 0.13 | 0.15 | no |
| Claude Sonnet 4.6 | 6 / 2 / 92 | 24 / 8 / 68 | 0.011 | 0.30 | **yes (reversed)** |
| Claude Haiku 4.5 | 0 / 18 / 82 | 2 / 26 / 72 | 0.36 | 0.14 | no |
| GPT-5.5 | 0 / 2 / 98 | 0 / 0 / 100 | 1.00 | 0.00 | no |
| GPT-5.4 | 0 / 4 / 96 | 0 / 6 / 94 | 1.00 | 0.00 | no |
| GPT-5.4-mini | 12 / 4 / 84 | 2 / 12 / 86 | 0.06 | 0.24 | no |
| *Humans* | *74 enforce* | *56 enforce* | n/a | n/a | *yes (beast-ward)* |

**Figure 2 |** Enforce / reform / mixed shares (percent of coded answers) for all six models under each
frame, against the human baseline. Every model collapses the enforcement column toward zero and piles
onto "mixed". No model reproduces the human beast-ward enforcement swing.

Enforcement is scarce on every model. The maximum is 24 percent (Sonnet, and under *virus*, not
beast), against the human 56 to 74. Most answers get coded "mixed," from 68 percent up to a GPT-5.5
near-ceiling of 98 to 100. The framing swing isn't reliably there either: five of the six models
show no significant beast-versus-virus difference. Sonnet is the lone exception (*p* = 0.011), and
it cuts against the hypothesis. It gives *more* enforcement under the virus frame (24 percent) than
under the beast frame (6 percent), the reverse of the human direction. Even the single "significant"
cell isn't the human effect reappearing. It's a small, backwards wobble on a model that otherwise
fence-sits at 92 percent mixed. No model copies the bias. Every model smooths it.

### 4.4 Contamination controls: is the model just recognizing the study?

The Addison passage is famous and almost certainly sits in every model's training data. That invites
an objection. Maybe the flat response is the model recognizing a known stimulus and returning a
studied, even-handed answer, not reasoning over the framing at all. Three controls test this
directly.

**Novel stimulus (un-memorized text).** We rebuilt every surface detail the model could've
memorized: a different city (Brookhaven), different statistics, and lexically novel metaphors that
match no indexed source, with crime as a *marauding wolf* versus a *growing cancer*. The
predator-versus-pathogen structure stays. If recognition drove the flatness, this version should
reveal a larger swing. It does the opposite, and the response is flatter still. On Opus the
wolf/cancer split is 0 percent enforcement under both, 88 versus 80 percent mixed, *p* = 0.41.
Across all six models every cell is non-significant, and two GPT-5 models sit at 100 percent mixed.
That rules out recognition of the original text as the explanation. The disposition survives on
metaphors the model has never seen.

**Paraphrase (surface robustness).** We kept the beast/virus manipulation and every underlying fact,
but paraphrased the surrounding report and changed the city (Marlowe) and the numbers. Memorized-text
effects are brittle to this kind of rewrite. A real framing effect isn't. The result doesn't change:
flat and non-significant on five of six models. Sonnet is again the lone significant cell
(*p* = 0.0004), and again it points the wrong way for the hypothesis (more reform under *beast*).
The paraphrase did shift the models' *baseline* taste toward reform on some cells (Opus answered
reform 94 to 100 percent of the time), but it opened no beast-ward enforcement gap. The level
changed. The framing sensitivity didn't.

**Recognition probe (direct measurement).** Here we didn't ask the model what to do. We asked
whether it had seen the passage before and what it was testing, then coded each answer as
recognized / partial / unrecognized on the verbatim Addison text versus a disguised paraphrase. The
models do recognize the *paradigm*. Opus signals some recognition on 58 percent of verbatim trials,
and several models name a "framing" or "metaphor-effect" experiment. But recognition doesn't track
the split the way contamination would predict. It's often *higher* on the disguise than on the
verbatim text (Opus 100 percent "recognized" on the disguise), because the disguise kept the
tell-tale "wild beast" metaphor. The model recognizes the framing manipulation, not the memorized
Addison wording. That recognition is real, but it doesn't produce the flat answer: the flatness
persists on the never-seen wolf/cancer metaphors, where recognition has nothing to grip.

### 4.5 Synthesis (replication)

The three results point the same way. The human enforcement answer all but vanishes: every model
leads with enforcement in at most 24 percent of answers, against the human 56 to 74, and clusters on
balanced "police and reform" replies (Sections 4.1, 4.3). The metaphor swing that moved people
eighteen points doesn't reliably appear on any model, and the one significant cell runs backwards
(Sections 4.2, 4.3). Recognition of a famous passage doesn't explain either result, since a novel
stimulus is flatter, a paraphrase leaves the result intact, and the recognition probe shows the
models keying on the paradigm, not the text (Section 4.4). The verdict for this series is
**smooth**. The model neither copies the human metaphor bias nor amplifies it. It dissolves the
loaded framing into even-handedness.

# Part II. Extension: agentic scaffolds

## 5. Why extend to agents

Part I ran the original as a single open-ended answer, faithful to the paper. Most real uses of a
model are *agentic*, though: the model deliberates in steps, calls tools, or looks facts up before
it commits. That raises two possibilities. Forcing explicit deliberation might surface connotations
of the metaphor that a one-shot answer glosses over, and revive the effect. Or staging the choice as
an agent might only deepen the fence-sitting Part I found. This part is a methods extension, not a
human comparison. No human "agentic" baseline exists, so every comparison is *within* one tool
harness, changing only the scaffold.

## 6. Agentic design

We hold the choice fixed on the un-memorized Brookhaven wolf/cancer stimulus (the cleanest,
contamination-free version from Part I) and vary only how we stage the decision. In both scaffolds
we read the final pick from a schema-constrained tool field: the model commits to `enforce`,
`reform`, or `mixed` through a terminal `recommend_approach` tool. Unlike Part I, there's no
free-text judge. The model self-classifies. We changed the instrument on purpose, and the change
matters for reading the numbers (see Limitations).

| Scaffold | What the agent does | Facts | Mean tool calls |
|---|---|---|---:|
| Multi-step | pinned `diagnose` → `list_measures` → `recommend_approach` | in prompt | 3.0 |
| Tool-calling | autonomous: must `list` and read each evidence brief, then `recommend` | retrieved | ~5 |

Each scaffold runs both metaphors (wolf, cancer), fifty trials per cell, on Claude Opus 4.8 at default
sampling.

## 7. Agentic results

### 7.1 More deliberation, more fence-sitting

Across **all 200 trials, both scaffolds and both metaphors**, Opus committed to the balanced `mixed`
approach every time. The distributions are fully saturated (100 percent mixed in all four cells),
which leaves no framing swing to test. A forced diagnose-weigh-commit workflow didn't revive the
effect. Neither did making the model retrieve the facts itself.

| Scaffold | Wolf (enf/ref/mix) | Cancer (enf/ref/mix) |
|---|---|---|
| Multi-step (forced workflow) | 0 / 0 / 100 | 0 / 0 / 100 |
| Tool-calling (autonomous retrieval) | 0 / 0 / 100 | 0 / 0 / 100 |

**Figure 3 |** Committed-approach shares under the two agentic scaffolds. Every cell is 100 percent
"mixed". That's the fence-sitting of Part I taken to its limit, once the model has to commit to one
approach through a tool.

The transcripts show real deliberation, not a stuck default. In the multi-step arm the model wrote
full diagnoses and candidate-measure lists before committing. In the tool-calling arm it called
`list_products`, retrieved all three evidence briefs, and cited the retrieved numbers in its
rationale. Then, every time, it argued for pairing "immediate enforcement to protect life" with
"reform that treats root causes … in equal measure." Two effects compound here. One is the model's
own preference for a balanced answer (Part I). The other is the terminal tool's explicit `mixed`
option, which gives that preference a single clean box to check. In practice, adding deliberation
steps or tool-use to a framing-sensitive decision didn't make the model *more* susceptible to the
loaded word. It made the model converge harder on even-handedness.

### 7.2 Synthesis (extension)

Staging the metaphor choice as an agent doesn't recover the human effect. It removes the last of the
variance Part I left. Forced multi-step deliberation and autonomous retrieval both drive Opus to a
balanced recommendation in every trial. For this bias, more process doesn't surface the framing. It
entrenches the model's refusal to be tilted by it.

# Both parts

## 8. Assumptions

- **The manipulation is a pure framing change.** Beast versus virus (and wolf versus cancer) changes
  only the metaphor. Every fact in the report is identical, so any shift comes from the framing, not
  from different information.
- **The coding scheme matches the source study.** In Part I the fixed judge codes free text into the
  enforcement / reform categories the original study used for its human answers, by emphasis and
  ordering. In Part II the model commits to the same categories through a constrained tool field.
- **The contamination controls isolate recognition.** The novel stimulus shares no memorizable
  surface with the original. The paraphrase holds the manipulation and facts while rewriting the
  prose. The recognition probe measures recognition directly.
- **Catalogue model identifiers map to the intended deployed models,** with stable behavior over the
  run window.

## 9. Limitations

- **Floor effects on enforcement.** The models almost never lead with enforcement, so the human
  outcome measure (enforcement share) sits near a floor. That limits how far a beast-ward swing could
  visibly move it. The distribution test (enforce vs reform vs mixed) guards against reading the null
  off the floor alone, but a model that fence-sits at 90-plus percent mixed has little room to move in
  any direction.
- **One run per model per condition, fifty trials per cell.** Magnitudes at default (or low-reasoning)
  sampling are noisy. The stable result is the *direction* (no reliable beast-ward swing, enforcement
  scarce, convergence on mixed), not precise point estimates. Part I reports six models; Part II is
  Opus only.
- **A single judge, and judge-dependent coding.** Part I's outcome is one model's coding of free text.
  The "mixed" category in particular absorbs any answer that names both sides, and the paraphrase run
  shows the coded baseline can shift with surface form. A multi-judge or human-coded check is the
  natural follow-up.
- **Part II changes the instrument.** Reading the decision from a forced-choice tool enum with an
  explicit `mixed` option isn't the same measurement as judge-coded free text, and it plausibly
  inflates "mixed." We read Part II strictly within itself (scaffold versus scaffold), not against
  Part I's numbers. The obvious next probe is a binary tool that drops `mixed` and forces
  enforce-or-reform, to expose any residual lean beneath the hedging.
- **Sonnet is the one moving cell, twice.** Sonnet reaches significance on both the canonical and
  paraphrase runs, each time against the human direction. We can't yet say whether that's a stable
  Sonnet trait or sampling noise on a 92-percent-mixed baseline.

## 10. Conclusion

We handed six models the study that made metaphor-as-thought famous, and none reproduced it. The
word that moved people eighteen points toward punishment barely moves a model, and the
enforcement-first answer that dominated the human data is the one answer the models almost never
give. They reach for a balanced "enforce and reform" reply, out of a general disposition to resist
loaded framing. Recognition of a famous passage doesn't explain it: the response is flatter still on
metaphors the models have never seen, a paraphrase doesn't move it, and it's unrelated to what the
recognition probe shows the models recognize. Asked to deliberate in steps or to gather the facts
through tools, the model doesn't get more suggestible. It converges completely, committing to the
balanced approach in every one of two hundred trials.

If you're handing a model a slanted brief, this cuts both ways. The model won't silently inherit the
tilt of the words you frame a problem in. You can point it at a loaded memo or headline and ask it
to name the neutral facts and say where the wording is trying to steer. The cost is the mirror
image. Bias-resistance shows up as fence-sitting, and when you want a recommendation and not an
even-handed survey, you have to ask for one. Tell the model to commit, drop the hedge, and give its
strongest reasons for a single side.

## 11. Practical takeaways

From the replication (Part I):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| Barely shifted (at most ~1 in 10 either way, sometimes the opposite) versus nearly 1 in 5 for people; the models flagged the framing paradigm itself. | The model resists loaded framing; it doesn't absorb it. | Use that. Paste in a slanted memo or headline and ask the model to **act as a spin detector**: "what are the neutral facts, and where is the wording trying to steer me?" |
| Clustered on balanced "police *and* fix root causes" answers, well below human enforcement levels. | Bias-resistance shows up as fence-sitting. | When you want a recommendation and not a balanced overview, **make it commit**: "don't hedge, pick one side and give your three strongest reasons." |
| The one "significant" difference was a small, backwards wobble on a model that otherwise sat at 92% mixed. | A result can look "not just chance" when nothing in the predicted direction changed. | Before trusting any headline number or confidence score, **open a few of the actual answers and read them**. The summary can move even when the responses barely differ. |
| Recognized the framing paradigm, yet stayed flat on never-seen metaphors (wolf vs cancer). | Recognition is real; imitation isn't. | For a well-known framework the model may give the textbook take, so **feed it your concrete details** and tell it to reason from your situation, not the canonical example. |

From the agentic extension (Part II):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| Forcing a diagnose-weigh-commit workflow left the framing effect at zero: 100% balanced answers. | Added deliberation steps entrench the even-handed answer; they don't surface the metaphor. | Don't expect **"add a planning step"** to change a framing-sensitive decision. Here it only hardened the hedge. |
| Autonomous tool-calling, with the facts behind retrieval, also gave 100% balanced answers. | Making the agent gather the facts itself didn't make it more suggestible to the loaded word. | **"Have the agent look it up" isn't a neutral swap, but it's a safe one here.** Retrieval didn't open a framing gap. |
| Committing through a tool with an explicit "mixed" option produced 200 of 200 balanced picks. | A forced-choice box for "both" collects every answer the model would otherwise hedge. | If you want to detect a *residual* lean, **remove the middle option**: force a binary choice and see which way it breaks. |

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
