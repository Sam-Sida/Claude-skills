"""Find option wording that leaked into persona cards, which primes personas toward that option.

Usage: py leakage.py panel.json
Run it on the roster before spawning personas (responses aren't needed). Prints the leaks as JSON;
exits 1 if there are any, so rewrite those traits in your own words and run it again.

A leak is a run of 3+ words from an option (at least one of them not a stop word), or 2 words
where one is a number (e.g. "6-8 weeks"), appearing in a persona's summary or traits.
"""
import argparse
import json
import re
import sys

STOP = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "at", "for", "with", "by", "from",
    "your", "you", "our", "we", "it", "is", "are", "be", "not", "no", "what", "they", "their", "this",
    "that", "do", "will", "can", "more", "less", "than", "so", "as", "if", "into", "next",
}


def _words(text):
    return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*", text.lower())


def _phrases(text):
    w = _words(text)
    out = [w[i:i + 3] for i in range(len(w) - 2) if any(x not in STOP for x in w[i:i + 3])]
    out += [w[i:i + 2] for i in range(len(w) - 1) if any(any(c.isdigit() for c in x) for x in w[i:i + 2])]
    return out


def _contains(words, phrase):
    n = len(phrase)
    return any(words[i:i + n] == phrase for i in range(len(words) - n + 1))


def find_leaks(stimuli, personas):
    leaks = []
    for p in personas:
        card = _words(" ".join([p.get("summary", "")] + [t["trait"] for t in p.get("traits", [])]))
        for s in stimuli:
            hit = next((ph for ph in _phrases(s["text"]) if _contains(card, ph)), None)
            if hit:
                leaks.append({"persona": p["id"], "stimulus": s["id"], "phrase": " ".join(hit)})
    return leaks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("panel")
    args = ap.parse_args()
    with open(args.panel, encoding="utf-8") as f:
        panel = json.load(f)
    leaks = find_leaks(panel["stimuli"], panel["personas"])
    print(json.dumps(leaks, indent=2))
    sys.exit(1 if leaks else 0)


if __name__ == "__main__":
    main()
