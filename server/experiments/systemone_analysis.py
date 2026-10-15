"""Summaries for ``systemone_probe`` runs (TypeSafe's Jev).

The generic analysis in ``content_store.build_analysis`` counts discrete choices
across repeated trials and tests them with chi-square. A System One probe is a
different object: each variant is one typed question whose answer is already a
probability distribution, and the experiment's claims are about how those
distributions move when the *question* changes (phrasing, option order, a
planted statement, decomposition), not about sampling variance. So this module
computes the per-experiment readouts the post and its widgets need — E0
repeatability, E3 paraphrase spread, E4 order sensitivity, E5 steering, E8 polarity
sums — straight from the run's trials, and recomputes TypeSafe's published
``confidence`` formulas from the returned probabilities as a self-check.

Everything here is a pure function of (experiment config, run); nothing is
hard-coded from any particular run. Each ``eN`` block is present only when the
run contains that experiment's variants, so a partial run (``--only E0``) still
analyses cleanly.
"""

from __future__ import annotations

from statistics import mean, pstdev
from typing import Any, Dict, List, Optional

# Count-word options map to integers so per-person answers can be averaged in
# code (E2). ``other`` has no integer value.
COUNT_VALUES: Dict[str, Optional[int]] = {"zero": 0, "one": 1, "two": 2, "other": None}


# --------------------------------------------------------------------------- #
# TypeSafe's confidence formulas (docs.typesafe.ai/confidence), recomputed
# --------------------------------------------------------------------------- #
def choice_confidence(probabilities: Dict[str, float]) -> Optional[float]:
    """``(p_max − 1/n) / (1 − 1/n)``: 1 for a single spike, 0 for a flat spread."""
    n = len(probabilities)
    if n < 2:
        return None
    p_max = max(probabilities.values())
    return (p_max - 1 / n) / (1 - 1 / n)


def score_confidence(probabilities: Dict[str, float]) -> Optional[float]:
    """``max(0, 1 − Σ p_i·|i − m| / MAD_unif)`` with ``m`` the most likely level."""
    n = len(probabilities)
    if n < 2:
        return None
    levels = sorted(int(k) for k in probabilities)
    m = max(levels, key=lambda i: probabilities[str(i)])
    weighted = sum(probabilities[str(i)] * abs(i - m) for i in levels)
    centre = (n - 1) / 2
    mad_unif = sum(abs(i - centre) for i in levels) / n
    return max(0.0, 1 - weighted / mad_unif) if mad_unif else None


def score_expectation(probabilities: Dict[str, float]) -> float:
    """Probability-weighted mean of the level indices (TypeSafe's ``score``)."""
    return sum(int(k) * p for k, p in probabilities.items())


def noul_confidence(p: float) -> float:
    """``|2p − 1|``: the docs' suggested sharpness statistic for a Noul."""
    return abs(2 * p - 1)


# --------------------------------------------------------------------------- #
# Per-variant summaries
# --------------------------------------------------------------------------- #
def _r(x: Optional[float], places: int = 4) -> Optional[float]:
    return None if x is None else round(float(x), places)


def _mean_distribution(dists: List[Dict[str, float]]) -> Dict[str, float]:
    keys = list(dists[0].keys())
    return {k: _r(mean(d.get(k, 0.0) for d in dists)) for k in keys}


def _sd_distribution(dists: List[Dict[str, float]]) -> Dict[str, float]:
    keys = list(dists[0].keys())
    return {k: _r(pstdev([d.get(k, 0.0) for d in dists])) for k in keys}


def _variant_summary(variant: Dict[str, Any], trials: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Collapse a variant's (usually single) trial(s) into one answer record."""
    question = variant.get("question") or {}
    qtype = question.get("type")
    answers = [t["answer"] for t in trials if t.get("ok") and t.get("answer")]
    summary: Dict[str, Any] = {
        "variantId": variant["id"],
        "label": variant.get("label", variant["id"]),
        "experiment": variant.get("experiment"),
        "organ": variant.get("organ"),
        "questionType": qtype,
        "instructions": question.get("instructions"),
        "trials": len(answers),
        "latencyMs": _r(mean(t["latencyMs"] for t in trials if t.get("latencyMs") is not None), 1)
        if any(t.get("latencyMs") is not None for t in trials)
        else None,
    }
    if not answers:
        return summary

    if qtype == "choice":
        criteria = question.get("criteria") or {}
        summary["options"] = list(criteria.keys())
        dists = [a.get("probabilities", {}) for a in answers]
        probs = _mean_distribution(dists)
        summary["probabilities"] = probs
        summary["choice"] = max(probs, key=probs.get)
        summary["choices"] = [a.get("choice") for a in answers]
        summary["confidence"] = _r(mean(a.get("confidence", 0.0) for a in answers))
        summary["confidenceRecomputed"] = _r(choice_confidence(probs))
        summary["topProbability"] = _r(max(probs.values()))
        ranked = sorted(probs.values(), reverse=True)
        summary["topToSecondRatio"] = (
            _r(ranked[0] / ranked[1], 2) if len(ranked) > 1 and ranked[1] > 0 else None
        )
    elif qtype == "score":
        levels = list(question.get("criteria") or [])
        dists = [a.get("probabilities", {}) for a in answers]
        probs = _mean_distribution(dists)  # keys "0".."n-1"
        summary["levels"] = levels
        summary["probabilities"] = probs
        summary["probabilitiesByLevel"] = {
            levels[int(k)] if int(k) < len(levels) else k: v for k, v in probs.items()
        }
        summary["score"] = _r(mean(a.get("score", 0.0) for a in answers))
        summary["scoreRecomputed"] = _r(score_expectation(probs))
        summary["confidence"] = _r(mean(a.get("confidence", 0.0) for a in answers))
        summary["confidenceRecomputed"] = _r(score_confidence(probs))
        top = max(probs, key=probs.get)
        summary["modalLevel"] = levels[int(top)] if int(top) < len(levels) else top
        exp = summary["score"]
        summary["betweenLevels"] = exp is not None and abs(exp - round(exp)) > 0.05
    elif qtype == "noul":
        p = mean(a.get("noul", 0.0) for a in answers)
        summary["p"] = _r(p)
        summary["confidenceAbs"] = _r(noul_confidence(p))
    return summary


# --------------------------------------------------------------------------- #
# Per-experiment readouts
# --------------------------------------------------------------------------- #
def _by_experiment(variants: List[Dict[str, Any]], tag: str) -> List[Dict[str, Any]]:
    return [v for v in variants if v.get("experiment") == tag]


def _e0(variant: Dict[str, Any], trials: List[Dict[str, Any]]) -> Dict[str, Any]:
    answers = [t for t in trials if t.get("ok") and t.get("answer")]
    dists = [t["answer"].get("probabilities", {}) for t in answers]
    if not dists:
        return {"variantId": variant["id"], "n": 0}
    sd = _sd_distribution(dists)
    confidences = [t["answer"].get("confidence", 0.0) for t in answers]
    return {
        "variantId": variant["id"],
        "instructions": (variant.get("question") or {}).get("instructions"),
        "n": len(dists),
        "options": list(dists[0].keys()),
        "perTrial": [
            {
                "trial": t.get("trial"),
                "probabilities": t["answer"].get("probabilities"),
                "choice": t["answer"].get("choice"),
                "confidence": _r(t["answer"].get("confidence")),
                "latencyMs": t.get("latencyMs"),
            }
            for t in answers
        ],
        "mean": _mean_distribution(dists),
        "sd": sd,
        "maxSd": max(sd.values()),
        "confidenceSd": _r(pstdev(confidences)) if len(confidences) > 1 else 0.0,
        "distinctChoices": sorted({t["answer"].get("choice") for t in answers}),
        # The docs' own self-consistency figure for comparison in the post.
        "docsReferenceMeanSd": 0.0098,
    }


def _spread_block(
    rows: List[Dict[str, Any]], key: str, with_sd: bool
) -> Dict[str, Any]:
    """Per-option mean/min/max/spread (and SD) across a set of answer rows."""
    rows = [r for r in rows if r.get("probabilities")]
    if not rows:
        return {key: [], "perOption": {}}
    options = list(rows[0]["probabilities"].keys())
    per_option: Dict[str, Dict[str, Optional[float]]] = {}
    for opt in options:
        values = [r["probabilities"].get(opt, 0.0) for r in rows]
        entry = {
            "mean": _r(mean(values)),
            "min": _r(min(values)),
            "max": _r(max(values)),
            "spread": _r(max(values) - min(values)),
        }
        if with_sd:
            entry["sd"] = _r(pstdev(values))
        per_option[opt] = entry
    block: Dict[str, Any] = {
        key: rows,
        "options": options,
        "perOption": per_option,
        "maxSpread": max(e["spread"] for e in per_option.values()),
        "distinctChoices": sorted({r.get("choice") for r in rows if r.get("choice")}),
        "meanOfMeans": {opt: per_option[opt]["mean"] for opt in options},
    }
    if with_sd:
        block["maxSd"] = max(e["sd"] for e in per_option.values())
    block["meanChoice"] = max(block["meanOfMeans"], key=block["meanOfMeans"].get)
    return block


def _organ_groups(
    summaries: Dict[str, Dict[str, Any]], variants: List[Dict[str, Any]], field: str
) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for v in variants:
        s = summaries.get(v["id"])
        if not s or not s.get("probabilities"):
            continue
        row = {
            field: v.get(field),
            "variantId": v["id"],
            "instructions": s.get("instructions"),
            "probabilities": s["probabilities"],
            "choice": s.get("choice"),
            "confidence": s.get("confidence"),
        }
        if field == "order":
            row["criteriaOrder"] = list((v.get("question") or {}).get("criteria", {}).keys())
        groups.setdefault(v.get("organ", "all"), []).append(row)
    return groups


def summarize(experiment: Dict[str, Any], run: Dict[str, Any]) -> Dict[str, Any]:
    """Build the ``systemone`` analysis block for a probe run."""
    variants = experiment.get("variants", [])
    trials_by_variant: Dict[str, List[Dict[str, Any]]] = {}
    for t in run.get("trials", []):
        trials_by_variant.setdefault(t.get("variantId"), []).append(t)

    summaries = {
        v["id"]: _variant_summary(v, trials_by_variant.get(v["id"], [])) for v in variants
    }
    ok_trials = [t for t in run.get("trials", []) if t.get("ok")]

    out: Dict[str, Any] = {
        "state": experiment.get("state"),
        "meta": _meta(run, ok_trials, variants),
        "variants": summaries,
        "confidenceCheck": _confidence_check(summaries),
        "sieve": _sieve(summaries, experiment),
    }

    e0 = _by_experiment(variants, "E0")
    if e0:
        out["e0"] = _e0(e0[0], trials_by_variant.get(e0[0]["id"], []))

    e1 = _by_experiment(variants, "E1")
    if e1:
        block: Dict[str, Any] = {}
        for v in e1:
            s = summaries[v["id"]]
            if s.get("trials"):
                block.setdefault(v.get("organ"), {})[s["questionType"]] = s
        out["e1"] = block

    e2 = _by_experiment(variants, "E2")
    if e2:
        persons = []
        totals: Dict[str, List[int]] = {}
        for v in e2:
            s = summaries[v["id"]]
            if not s.get("trials"):
                continue
            value = COUNT_VALUES.get(s.get("choice"))
            persons.append(
                {
                    "person": v.get("person"),
                    "organ": v.get("organ"),
                    "variantId": v["id"],
                    "probabilities": s.get("probabilities"),
                    "choice": s.get("choice"),
                    "confidence": s.get("confidence"),
                    "integer": value,
                }
            )
            if value is not None:
                totals.setdefault(v.get("organ"), []).append(value)
        out["e2"] = {
            "persons": persons,
            "codeMeans": {organ: _r(mean(vals), 3) for organ, vals in totals.items()},
        }

    e3 = _by_experiment(variants, "E3")
    if e3:
        out["e3"] = {
            organ: _spread_block(rows, "phrasings", with_sd=False)
            for organ, rows in _organ_groups(summaries, e3, "phrasing").items()
        }

    e4 = _by_experiment(variants, "E4")
    if e4:
        out["e4"] = {
            organ: _spread_block(rows, "orders", with_sd=True)
            for organ, rows in _organ_groups(summaries, e4, "order").items()
        }

    e5 = _by_experiment(variants, "E5")
    if e5:
        by_condition = {v.get("condition"): summaries[v["id"]] for v in e5}
        clean = by_condition.get("clean") or {}
        planted = by_condition.get("planted") or {}
        block = {"clean": clean, "planted": planted}
        if clean.get("probabilities") and planted.get("probabilities"):
            block["deltaPOne"] = _r(
                planted["probabilities"].get("one", 0.0) - clean["probabilities"].get("one", 0.0)
            )
            block["deltaConfidence"] = _r(
                (planted.get("confidence") or 0.0) - (clean.get("confidence") or 0.0)
            )
            block["choiceChanged"] = planted.get("choice") != clean.get("choice")
            block["plantedNote"] = next(
                (v.get("state", {}).get("note") for v in e5 if v.get("condition") == "planted"),
                None,
            )
        out["e5"] = block

    e6 = _by_experiment(variants, "E6")
    if e6:
        v = e6[0]
        s = summaries[v["id"]]
        out["e6"] = {
            **s,
            "state": v.get("state"),
            "codeValue": v.get("code_value"),
            "codeBucket": v.get("code_bucket"),
            "agrees": s.get("choice") == v.get("code_bucket") if s.get("trials") else None,
        }

    e7 = _by_experiment(variants, "E7")
    if e7:
        out["e7"] = summaries[e7[0]["id"]]

    e8 = _by_experiment(variants, "E8")
    if e8:
        claims = []
        pair: Dict[str, Optional[float]] = {}
        for v in e8:
            s = summaries[v["id"]]
            if not s.get("trials"):
                continue
            claims.append(
                {
                    "variantId": v["id"],
                    "claim": v.get("claim"),
                    "instructions": s.get("instructions"),
                    "p": s.get("p"),
                    "confidenceAbs": s.get("confidenceAbs"),
                }
            )
            if v.get("polarity_pair") == "a":
                pair["exactlyTwo"] = s.get("p")
            elif v.get("polarity_pair") == "b":
                pair["fewerThanTwo"] = s.get("p")
        block = {"claims": claims}
        if pair.get("exactlyTwo") is not None and pair.get("fewerThanTwo") is not None:
            block["polarity"] = {
                **pair,
                "sum": _r(pair["exactlyTwo"] + pair["fewerThanTwo"]),
                "residual": _r(1 - pair["exactlyTwo"] - pair["fewerThanTwo"]),
            }
        out["e8"] = block

    return out


def _meta(
    run: Dict[str, Any], ok_trials: List[Dict[str, Any]], variants: List[Dict[str, Any]]
) -> Dict[str, Any]:
    latencies = [t["latencyMs"] for t in ok_trials if t.get("latencyMs") is not None]
    input_tokens = sum(int((t.get("usage") or {}).get("input_tokens") or 0) for t in ok_trials)
    output_tokens = sum(int((t.get("usage") or {}).get("output_tokens") or 0) for t in ok_trials)
    return {
        "responseModels": sorted({t.get("responseModel") for t in ok_trials if t.get("responseModel")}),
        "requestedModel": next(
            (t.get("request", {}).get("model") for t in ok_trials if t.get("request")), None
        ),
        "runId": run.get("runId"),
        "startedAt": run.get("startedAt"),
        "finishedAt": run.get("finishedAt"),
        "calls": len(run.get("trials", [])),
        "okCalls": len(ok_trials),
        "failedCalls": len(run.get("trials", [])) - len(ok_trials),
        "variants": len(variants),
        "experiments": sorted({v.get("experiment") for v in variants if v.get("experiment")}),
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "estimatedUsd": _r(sum(float(t.get("estimatedUsd") or 0.0) for t in ok_trials), 6),
        "latencyMs": {
            "mean": _r(mean(latencies), 1) if latencies else None,
            "min": _r(min(latencies), 1) if latencies else None,
            "max": _r(max(latencies), 1) if latencies else None,
            "total": _r(sum(latencies), 1) if latencies else None,
        },
    }


SIEVE_THRESHOLDS = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def _sieve(summaries: Dict[str, Dict[str, Any]], experiment: Dict[str, Any]) -> Dict[str, Any]:
    """An illustrative confidence-gated sieve over the run's own count questions.

    Items are every Choice variant that used the experiment's shared
    ``decision_options`` (E0's repeats excluded). For each threshold: how many
    would be auto-accepted (``confidence >= t``) versus sent to a person. The
    post quotes these counts, so they are computed here rather than by hand.
    """
    decision_ids = {opt["id"] for opt in experiment.get("decision_options", [])}
    items = [
        {
            "variantId": s["variantId"],
            "experiment": s.get("experiment"),
            "label": s.get("label"),
            "choice": s.get("choice"),
            "confidence": s.get("confidence"),
        }
        for s in summaries.values()
        if s.get("questionType") == "choice"
        and s.get("experiment") != "E0"
        and set(s.get("options") or []) == decision_ids
        and s.get("confidence") is not None
    ]
    items.sort(key=lambda i: -i["confidence"])
    by_threshold = []
    for t in SIEVE_THRESHOLDS:
        accepted = sum(1 for i in items if i["confidence"] >= t)
        by_threshold.append(
            {
                "threshold": t,
                "accepted": accepted,
                "review": len(items) - accepted,
                "coverage": _r(accepted / len(items)) if items else None,
            }
        )
    return {"items": items, "count": len(items), "byThreshold": by_threshold}


def _confidence_check(summaries: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Reported vs. recomputed confidence for every Choice/Score answer."""
    rows = []
    for s in summaries.values():
        if s.get("confidence") is None or s.get("confidenceRecomputed") is None:
            continue
        rows.append(
            {
                "variantId": s["variantId"],
                "questionType": s["questionType"],
                "reported": s["confidence"],
                "recomputed": s["confidenceRecomputed"],
                "delta": _r(s["confidence"] - s["confidenceRecomputed"]),
            }
        )
    return {
        "rows": rows,
        "maxAbsDelta": _r(max((abs(r["delta"]) for r in rows), default=0.0)),
    }
