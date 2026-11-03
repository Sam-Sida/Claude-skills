"""Per-persona stimulus orders, so no option always benefits from being shown first.

Usage: py orders.py --stimuli A,B,C,D --n 12 [--seed 7]
Prints JSON: {"P01": ["C", "A", "D", "B"], ...}
"""
import argparse
import json
import random


def make_orders(ids, n, seed=None):
    if len(set(ids)) != len(ids):
        raise ValueError("stimulus ids must be unique")
    rng = random.Random(seed)
    base = list(ids)
    rng.shuffle(base)
    result = {}
    for i in range(n):
        # Rotate the first slot so every option leads equally often; shuffle the rest.
        first = base[i % len(base)]
        rest = [s for s in base if s != first]
        rng.shuffle(rest)
        result[f"P{i + 1:02d}"] = [first] + rest
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stimuli", required=True, help="comma-separated ids, decoy included")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--seed", type=int)
    args = ap.parse_args()
    print(json.dumps(make_orders(args.stimuli.split(","), args.n, args.seed), indent=2))


if __name__ == "__main__":
    main()
