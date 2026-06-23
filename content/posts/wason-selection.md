---
category: Decisions
type: Experiments
date: '2026-06-20'
slug: wason-selection
title: 'The Falsification Test: Will an Agent Turn the Card That Could Prove It Wrong?'
published: true
comingSoon: true
---

## Practical takeaways

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| Picked the falsifying card almost always alone (~9 in 10), every time when prompted; **never** made the human error. | It does the falsification move people skip. | Lean on this: ask the model to **try to disprove your belief or plan**, "what evidence would show this is wrong, and how could I check it?" |
| A "name what would disprove this" step pushed it from almost always to every time. | A targeted falsification prompt sharpens reasoning. | Add the step to your prompt every time, **"before you answer, say what would make this false"**, it's cheap and reliably improves the answer. |
| Held on never-seen cards (almost always), matching the famous version. | Reasoning, not recall of a textbook puzzle. | You can trust this disprove-it reasoning to **carry over to your own new problems**, not just classic puzzles. |
| Drinking-age version: reasoning right, but ~3 in 4 snap picks hit the catch-all "other," not the matching option. | The fixed menu didn't fit how it wanted to answer. | When you give the model fixed choices, a wrong-looking answer may just mean **none of the options fit its reasoning, not that it reasoned badly**, let it explain before it picks, or add an "other (describe)" choice and read it. |
