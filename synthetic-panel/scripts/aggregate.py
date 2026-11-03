"""Score a synthetic panel: choice shares, winner, bias flags, and a confidence label.

Usage: py aggregate.py panel.json
Prints the results as JSON. The schema for panel.json is in references/panel-schema.md.
"""
import argparse
import json
import statistics

import leakage

DECOY_MAX = 0.15        # decoy share above this means personas are agreeing to please
WEAK_DECOY_MAX = 1.5    # decoy mean intent at or below this means it was too easy to reject
AGREEMENT_MAX = 0.85    # top share above this means personas are not independent enough
POSITION_MAX = 0.5      # share of picks that went to the first-shown option
HIGH_COVERAGE = 0.6     # grounded share of traits needed for High
LOW_COVERAGE = 0.3      # below this, the panel is mostly invented
HIGH_MARGIN = 0.25      # winner's lead over the runner-up needed for High
MIN_PANEL = 8           # smaller panels can't earn High


def _validate(panel):
    ids = [s["id"] for s in panel["stimuli"]]
    for p in panel["personas"]:
        r = p["response"]
        if r["choice"] not in ids + ["none"]:
            raise ValueError(f"{p['id']}: choice {r['choice']!r} is not a stimulus or 'none'")
        for sid, score in r.get("intent", {}).items():
            if sid not in ids:
                raise ValueError(f"{p['id']}: intent for unknown stimulus {sid!r}")
            if not 1 <= score <= 7:
                raise ValueError(f"{p['id']}: intent {score} for {sid} is outside 1-7")


def summarise(panel):
    _validate(panel)
    people = panel["personas"]
    n = len(people)
    stimuli = panel["stimuli"]
    ids = [s["id"] for s in stimuli]
    decoys = {s["id"] for s in stimuli if s.get("decoy")}
    real = [s for s in ids if s not in decoys]

    choices = [p["response"]["choice"] for p in people]
    shares = {s: choices.count(s) / n for s in ids + ["none"]}

    mean_intent, intent_sd = {}, {}
    for s in ids:
        scores = [p["response"]["intent"][s] for p in people if s in p["response"].get("intent", {})]
        mean_intent[s] = statistics.mean(scores) if scores else None
        intent_sd[s] = statistics.pstdev(scores) if len(scores) > 1 else None

    ranked = sorted(real, key=lambda s: (-shares[s], -(mean_intent[s] or 0), ids.index(s)))
    winner = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    margin = shares[winner] - (shares[runner_up] if runner_up else 0)

    decoy_share = sum(shares[d] for d in decoys)
    decoy_scores = [mean_intent[d] for d in decoys if mean_intent[d] is not None]
    decoy_intent = statistics.mean(decoy_scores) if decoy_scores else None
    top_share = max(shares[s] for s in ids + ["none"])
    picked = [p for p in people if p["response"]["choice"] != "none" and p.get("order")]
    first_pick_rate = (
        sum(p["response"]["choice"] == p["order"][0] for p in picked) / len(picked) if picked else 0
    )
    traits = [t for p in people for t in p.get("traits", [])]
    coverage = sum(t.get("basis") == "grounded" for t in traits) / len(traits) if traits else 0

    flags, reasons = [], []
    if decoy_share > DECOY_MAX:
        flags.append("sycophancy")
        reasons.append(f"The decoy won {decoy_share:.0%} of picks (limit {DECOY_MAX:.0%})")
    if decoy_intent is not None and decoy_intent <= WEAK_DECOY_MAX:
        flags.append("weak_decoy")
        reasons.append(f"The decoy scored {decoy_intent:.1f}/7 on intent, too easy to reject to test for sycophancy")
    leaks = leakage.find_leaks(stimuli, people)
    if leaks:
        flags.append("leakage")
        who = sorted({x["persona"] for x in leaks})
        reasons.append(f"Option wording appears in {len(who)} persona card(s) ({', '.join(who)}), which can prime their picks")
    if top_share > AGREEMENT_MAX:
        flags.append("homogeneity")
        reasons.append(f"{top_share:.0%} chose the same option (limit {AGREEMENT_MAX:.0%})")
    if len(ids) >= 3 and first_pick_rate > POSITION_MAX:
        flags.append("position_bias")
        reasons.append(f"{first_pick_rate:.0%} picked whichever option was shown first")
    if panel.get("single_context"):
        flags.append("single_context")
        reasons.append("Personas were written in one context, not answered independently")

    if "sycophancy" in flags or coverage < LOW_COVERAGE:
        confidence = "Low"
        if coverage < LOW_COVERAGE:
            reasons.append(f"Only {coverage:.0%} of persona traits are grounded in data")
    elif flags or coverage < HIGH_COVERAGE or margin < HIGH_MARGIN or n < MIN_PANEL:
        confidence = "Medium"
        if coverage < HIGH_COVERAGE:
            reasons.append(f"{coverage:.0%} of traits grounded (High needs {HIGH_COVERAGE:.0%})")
        if margin < HIGH_MARGIN:
            reasons.append(f"Winner leads by {margin:.0%} (High needs {HIGH_MARGIN:.0%})")
        if n < MIN_PANEL:
            reasons.append(f"Panel of {n} (High needs {MIN_PANEL}+)")
    else:
        confidence = "High"
        reasons.append("Grounded, clear lead, and no bias flags")

    return {
        "n": n,
        "shares": shares,
        "mean_intent": mean_intent,
        "intent_sd": intent_sd,
        "winner": winner,
        "runner_up": runner_up,
        "margin": margin,
        "decoy_share": decoy_share,
        "decoy_intent": decoy_intent,
        "first_pick_rate": first_pick_rate,
        "grounding_coverage": coverage,
        "flags": flags,
        "leaks": leaks,
        "confidence": confidence,
        "confidence_reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("panel")
    args = ap.parse_args()
    with open(args.panel, encoding="utf-8") as f:
        print(json.dumps(summarise(json.load(f)), indent=2))


if __name__ == "__main__":
    main()
