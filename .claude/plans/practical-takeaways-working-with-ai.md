# Practical takeaways: what three bias experiments tell you about working with AI

**Audience:** semi-technical — you use AI tools and maybe build with them, but you don't need the
statistics. **How to read this:** every recommendation is tied back to a specific result, in the form
**Observed → Why → Do differently**. Nothing here is generic advice; each item is something one of the
experiments actually showed.

## The series in one idea

Each study re-runs a classic *human* decision-bias experiment on language models and asks: does the
model **copy** the human bias, **smooth** it away, or **amplify** it? Across all three studies covered
here the answer was **smooth** — the models did not inherit the human mistake. That single fact drives
most of what follows: an AI is more useful as a *check on your thinking* than as a thing that thinks
like you.

| Study | Human bias | What the model did |
|---|---|---|
| The Metaphor Trap | One loaded word swings judgment 18 points | Barely moved (−9 to +9); frontier model named the trick |
| When Budgeting Backfires | "Set a budget first" makes people overspend | Flat — same mid-tier pick no matter the staging |
| The Falsification Test | Only ~4% seek evidence that could disprove a rule | Sought the disproof 90–100% of the time |

---

## Cross-cutting takeaways (read these first)

**1. Treat AI as a debiasing partner, not a mirror of your instincts.**
*Observed:* in all three studies the model declined to reproduce the human bias — it damped the
metaphor effect, ignored the budgeting nudge, and inverted the confirmation-bias result.
*Why:* these models were trained toward even-handed, normatively "correct" responses, so loaded
framing and process tricks that steer people tend to slide off them.
*Do differently:* use AI to **stress-test** a decision — "what's the framing here?", "what would prove
this wrong?", "argue the opposite" — rather than to confirm the answer you already favor.

**2. The price of that bias-resistance is blandness.**
*Observed:* in the budgeting study the model bought the same middle-tier $1.99 pen in ~98–100% of
trials; in the metaphor study it defaulted to comprehensive "do both" answers.
*Why:* resisting manipulation and regressing to the safe, defensible middle are the same behavior seen
from two sides.
*Do differently:* don't expect a bold, committed call by default. **Ask for it explicitly** — "pick
one and defend it," or "give me four genuinely different options, including one most people would
reject."

**3. More steps ≠ better thinking — the *right* prompt is what moves the needle.**
*Observed:* forcing the budgeting agent through 1, 2, or 5 steps produced the **same** choice with more
justification. But in the Falsification Test, one targeted prompt — "name what would disprove this
rule" — lifted correct answers from 90% to 100%.
*Why:* generic deliberation ("think step by step") mostly elaborates the existing answer; a prompt that
demands a specific cognitive move (falsify, compare, argue against) actually changes the process.
*Do differently:* scaffold for the *move you want*, not for length. Ask it to falsify, to argue the
other side, or to compare named alternatives.

**4. Consistency isn't correctness; a statistic isn't an effect; a long rationale isn't a vetted
decision.**
*Observed:* the budgeting agent gave nearly the same answer whether asked once or 50 times, even at
maximum randomness. The one "statistically significant" result in the metaphor study turned out to be
coding noise over near-identical text.
*Why:* a model can be confidently and repeatably wrong, and a summary number can cross a threshold
while the underlying behavior hasn't changed.
*Do differently:* **read the actual outputs**, not just the verdict or the confidence. Re-rolling the
same prompt won't surface alternatives — change the prompt to get a real second opinion.

**5. The model knows the famous cases — but knowing isn't copying. Still, anchor it to your specifics.**
*Observed:* recognition probes showed the models clearly recognize these classic studies, yet on
brand-new, un-memorized versions (novel metaphors; novel Wason cards) the results held — recognition
did not become imitation.
*Why:* the behavior comes from a general trained disposition, not recall of one paper.
*Do differently:* trust that the reasoning *move* generalizes, but for your own decision, push the
model off the textbook answer and **onto your concrete details** so it reasons about your case, not the
canonical one.

---

## Post 1 — The Metaphor Trap

> **Result in one line:** a single loaded word ("crime is a *beast*" vs "a *virus*") swings humans 18
> points toward punishment; the models barely moved, and the strongest model named the manipulation
> out loud.

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| Models swung only −9 to +9 pts vs the human +18; the frontier model called out "this passage uses persuasive techniques like the metaphor 'crime is a wild beast'." | They resist loaded framing instead of absorbing it. | Use a model as a **spin detector**: paste a slanted memo/pitch/headline and ask, "what are the neutral facts, and where is the language steering me?" |
| The models clustered on balanced "more policing *and* address root causes" answers, well below the human enforcement levels. | Bias-resistance shows up as fence-sitting. | When you need a *decision*, not a survey, force it: "pick one side and defend it," or "if you had to choose, what would you drop?" |
| The lone "significant" model result was near-identical text on both sides — a coding artifact, not a real swing. | A p-value can move without behavior moving. | Never act on a summary statistic or a confidence score without **spot-reading the raw answers** behind it. |
| Models recognized the study, but stayed flat even on never-seen metaphors (wolf vs cancer). | Recognition is real; imitation isn't. | On famous frameworks the model may hand you the textbook answer — **anchor it to your specifics** so it reasons about your situation. |

---

## Post 2 — When Budgeting Backfires (agentic)

> **Result in one line:** telling people to set a budget first makes them spend *more*; telling an
> agent to do the same changed nothing — it bought the same mid-tier item every time, and budgeted on
> its own when left free.

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| Forcing the agent to "set a budget first" left mean spend flat ($2.01 → $1.99); the human backfire never appeared. | Human debiasing *and re-biasing* tricks don't transfer to the agent. | Don't assume an agent inherits human nudges. If you're building purchasing/ops agents, **test the behavior**, don't port the human heuristic. |
| Every condition landed on the same safe, middle-tier pick. | The model regresses to the conventional, defensible option. | Great for dodging obvious mistakes, weak at surfacing the bold-but-right one. Ask for **diverse options including one most people would reject**, with the case for each. |
| 1 step, 2 steps, 5 steps → same choice, just more reasoning. | Extra deliberation adds justification, not a different conclusion. | Don't mistake a long, confident rationale for a vetted decision — a lot of it is built after the fact. Check the conclusion independently. |
| Even at maximum randomness, asking once ≈ asking 50×; spread only appeared in the *unforced* conditions. | Sampling noise won't generate genuine alternatives. | Re-running the same prompt is not a second opinion. **Change the prompt** (different frame, different constraints) to get real variety. |
| A forced single-shot tool call dropped 17/50 trials with empty arguments; turning on strict (schema-guaranteed) tool use fixed all of them. | One cold tool call under sampling noise is the brittle case. | *(For builders)* Use **strict schemas and a couple of scaffolding steps** for reliable tool use; avoid forcing a complex tool call in a single cold step. |

---

## Post 3 — The Falsification Test / Wason selection (agentic)

> **Result in one line:** humans almost never check the evidence that could *disprove* a rule (~4%
> get it right); the agent turned the disproving card 90–100% of the time, and volunteered the
> "what would prove this wrong?" reasoning on its own.

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| The agent picked the falsifying card 90% unscaffolded, 100% when prompted, and **never** made the human confirming error. | It does the falsification move people skip. | Use AI to **find what would break your belief/plan**: "what evidence would prove this wrong, and how would I check it?" It's better at this than we are. |
| Adding a "name what would disprove this rule" step pushed 90% → 100%. | A targeted falsification prompt sharpens the reasoning. | Bake the move into your prompt: "before answering, state what would make this false." Cheap, and it measurably improves the answer. |
| Performance held on never-seen cards (97%), matching the famous version. | This is reasoning, not recall of a textbook puzzle. | You can rely on the *move* generalizing to your novel problem — not just to classic brain-teasers. |
| In the concrete (drinking-age) version, the agent's reasoning was right but 73% of its snap picks landed on the catch-all "other" instead of the matching menu option. | A fixed multiple-choice menu didn't capture how the model wanted to answer. | When you hand an AI a fixed set of choices, a wrong-looking pick may be a **menu mismatch, not a reasoning error**. Let it explain *before* forcing a choice, or give an "other + describe" escape hatch — then read it. |

---

## One-page cheat sheet (prompts grounded in the results)

- **Detect spin** (Metaphor Trap): "Strip the framing from this. What are the neutral facts, and where
  is the wording steering me?"
- **Force a decision** (Budget Backfire, Metaphor Trap): "Don't give me a balanced overview. Pick one
  and give three concrete, falsifiable reasons."
- **Get real alternatives** (Budget Backfire): "Give me four genuinely different options, including one
  most people would reject" — *not* the same prompt re-run.
- **Stress-test a belief** (Falsification Test): "What would prove this wrong, and what's the cheapest
  way to check it?" / "Make the strongest case against my conclusion."
- **Anchor to your case** (Metaphor Trap, recognition controls): "Ignore the textbook version. Reason
  only from these specifics: …"
- **Always verify substance** (all three): read the raw output, not the confidence or the summary
  number. Consistency and a long rationale are not evidence of correctness.

## The honest caveats (so you don't over-generalize)

These come from a handful of scenarios on a few current models (mostly Claude Opus 4.8 / Sonnet 4.6),
not a sweep across every task. The pattern — models smooth these particular human biases — has held in
each study so far, but it is *evidence*, not a law. Two specific limits worth carrying: a model can be
confidently and consistently wrong (so verify quantitative claims yourself), and how you present
choices to it (menus, schemas, steps) can change what you measure (so design the interaction, not just
the question).
