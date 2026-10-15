# The Average Human Data Package (`jev-average-human`)

**Mishra, P.K. (2026). The Average Human: What a Calibrated Model Can and Cannot Tell You About One Person.** *Borrowed Intuitions.* `content/posts/the-average-human.md`.

This package holds every request sent to TypeSafe's Jev, every raw response, and the
derived summaries behind the write-up. Nassim Taleb's illustration (the average human has
one breast and one testicle) is rebuilt as a three-sentence JSON state and put to the model
in eight small probes. The question is not whether the model is accurate but what each of
its outputs (the Choice `choice` and `confidence`, the Score expectation, a Noul
probability) is a statement *about*: a population of similar questions, not the item in
front of you.

Unlike the other packages here, this is not a replication of a human-subjects study and
carries no human baseline. It is a demonstration on a synthetic state with ground truth
known by construction.

## Methodology

**Design.** One model, one pinned version (`jev-1.13.0`), 38 variants, 42 API calls, one
question per call. Jev returns a probability distribution rather than a sampled choice and
is near-deterministic, so each variant is a single call; E0 repeats one request five times
to measure that directly.

**State ("Taleb's room").**

```json
{"population": "Adult humans. About half are women and half are men.",
 "women": "Each woman has two breasts and zero testicles.",
 "men": "Each man has zero breasts and two testicles."}
```

**Probes.**

| Probe | What varies | Calls |
|---|---|---:|
| E0 | Nothing: E1's breasts Choice sent five times | 5 |
| E1 | The naive question as Choice and as Score, breasts and testicles | 4 |
| E2 | State replaced by one person (Maria / Tom); mean computed in code | 4 |
| E3 | Five paraphrases (average, typical, arithmetic mean, random person, most), both organs | 10 |
| E4 | Four option orders, both organs | 8 |
| E5 | Clean state vs. state plus a planted false sentence | 2 |
| E6 | Arithmetic: a 10-person group whose mean is 1.2 | 1 |
| E7 | A deliberately non-exclusive option set | 1 |
| E8 | One Noul per claim, including a polarity pair | 7 |

**Shared options.** Choice: `zero`, `one`, `two`, `other` (descriptions in the request
bodies). Score levels: `zero`, `one`, `two`, `three or more`.

**Model.** TypeSafe `jev-1.13.0` via `POST https://api.typesafe.ai/v1/systemone`; every
response echoed that id. Input tokens only are billed ($0.042 per million).

**Statistics.** None in the inferential sense: there is no sampling distribution to test,
so `significance.csv` is absent and the analysis JSON reports `overall.testable: false`.
The summaries are per-option means, min/max/spread across phrasings, SD across option
orders, deltas between conditions, the polarity-pair sum, and TypeSafe's `confidence`
recomputed from its published formulas as a check on the API's values.

## Results (summary)

1. **E0.** Five identical calls, identical answers: SD 0.000 on every option.
2. **E1.** The whole mass on `one` for both primitives and both organs (Score expectation
   1.0 at confidence 1.0 for breasts; 0.98 for testicles). The population mean, reported as
   a count.
3. **E2.** Per-person answers were crisp (Maria: two breasts, zero testicles; Tom: zero,
   two); the mean of 1.0 was built in code.
4. **E3.** P(one) ranged from 1.00 (*average*, *arithmetic mean*) to 0.04 (*most*).
   *Typical human being* returned `one` at 0.98, confidence 0.97. *One person at random*
   split 0.46 / 0.53 between `one` and `other`.
5. **E4.** No order effect: SD across orders at most 0.004; the argmax never moved.
6. **E5.** The planted sentence lowered P(one) by 0.18 and confidence by 0.24.
7. **E6.** The model's bucket (`over_one`, 0.92) agreed with the code's 1.2.
8. **E7.** `one_breast` 0.76, `other` 0.21, `one_testicle` 0.03: an uninterpretable split
   over non-exclusive options.
9. **E8.** "Mean breasts is one" 0.96; "typical woman has two" 0.98; "anyone has exactly
   one" 0.13. Polarity pair sums to 1.06.

**Verdict.** Not a replication, so no verdict badge. The reading: confidence, expectation
and argmax describe a population of questions; varying the question (paraphrase,
decomposition) exposed uncertainty that repetition and reordering did not.

## Package contents

```
jev-average-human/
├── README.md                          # this file (hand-written; preserved by the exporter)
├── manifest.json                      # model, run id, probes, calls per variant, spend
├── jev-average-human-data-package.zip
├── methodology/
│   ├── jev-average-human.yaml         # the experiment as code
│   └── request_<variant>.json         # the exact request body for each variant (38)
├── raw/
│   ├── runs/jev-1-13-0__<runId>.json  # the full run: request + response per call
│   └── trials.csv                     # long format, one row per outcome
└── results/
    ├── analysis/jev-1-13-0__<runId>.json
    ├── summary.json                   # the `systemone` block the post and widgets read
    └── summary.csv                    # one row per variant
```

`content/runs/jev-average-human/` also holds an earlier five-call E0 pilot run
(`20261015T203606Z`), superseded by the full run (`20261015T203628Z`) that the post pins.

## Data dictionary

`raw/trials.csv` (long format; a Choice call yields one row per option, a Score call one
per level, a Noul call two rows: `true` and `false`):

| Column | Meaning |
|---|---|
| `condition` | Variant id (also the question key in the request). |
| `probe` | E0 … E8. |
| `organ` | `breasts` / `testicles` where applicable. |
| `question_type` | `choice`, `score`, `noul`. |
| `trial` | Repeat index (0 except E0: 0–4). |
| `outcome` | Option name, level label, or `true`/`false`. |
| `probability` | The API's probability for that outcome. |
| `choice`, `confidence`, `score`, `noul` | The answer-level fields as returned. |
| `response_model` | The versioned model id echoed by the API. |
| `input_tokens`, `latency_ms` | Per call. |

`results/summary.csv`: one row per variant with its question text, the headline answer
(`choice`, `score` or `p`), confidence, and the full distribution as JSON.

`results/summary.json`: `meta` (calls, tokens, spend, latency), `variants` (per-variant
summaries), `e0` … `e8` (per-probe readouts), `sieve` (an illustrative confidence-gated
routing table over the run's own count questions), and `confidenceCheck`.

## How to replicate

With this repository:

```bash
export TYPESAFE_API_KEY=...            # or put it in .env (git-ignored)
python -m server.run_experiment jev-average-human --model jev --dry-run   # print the 42 bodies
python -m server.run_experiment jev-average-human --model jev --only E0 --no-post
python -m server.run_experiment jev-average-human --model jev --no-post
python -m server.export_experiment jev-average-human
python -m server.check_post_numbers the-average-human
```

Without it: POST each `methodology/request_*.json` to
`https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <key>`. The bodies are
complete; the `model` field pins `jev-1.13.0`.

## Caveats

- One synthetic state, one model version, one day (15 October 2026). `jev-1.14.0` was
  released the day before and was not run.
- Instructions say "the population described in the state" rather than naming state
  fields, because the documentation does not say how field names are presented.
- The documentation does not state that `criteria` key order is the presentation order;
  E4 treats it as an assumption under test.
- The sieve in `summary.json` uses this run's own 26 count questions as its population. It
  illustrates the coverage/reliability trade, nothing more.
- `temperature` in the YAML is inert; Jev has no sampling parameters.

## Citation

Mishra, P.K. (2026). *The Average Human: What a Calibrated Model Can and Cannot Tell You
About One Person.* Borrowed Intuitions. Data package `experiments/jev-average-human/`.
