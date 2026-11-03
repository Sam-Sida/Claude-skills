"""Render a scored panel as Markdown and HTML, and optionally a PDF via headless Chrome or Edge.

Usage: py render.py panel.json --out-dir <folder> --name <slug> [--pdf] [--png]
--png writes a full-page screenshot so the layout can be checked by eye.
panel.json must include a "narrative" block (see references/panel-schema.md).
"""
import argparse
import html
import json
import os
import shutil
import subprocess

import aggregate

FLAG_TEXT = {
    "sycophancy": "sycophancy (the decoy won too many picks)",
    "weak_decoy": "weak_decoy (the decoy was too easy to reject to test for sycophancy)",
    "leakage": "leakage (option wording appeared in persona cards)",
    "homogeneity": "homogeneity (personas agreed too much to be independent)",
    "position_bias": "position_bias (picks followed display order)",
    "single_context": "single_context (personas did not answer independently)",
}
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "report.html")


def _pct(x):
    return f"{x:.0%}"


def _intent(x):
    return f"{x:.1f}" if x is not None else "-"


def _rows(panel, res):
    out = []
    for s in panel["stimuli"]:
        label = s["text"] + (" (decoy)" if s.get("decoy") else "")
        mi = res["mean_intent"][s["id"]]
        out.append((s["id"], label, _pct(res["shares"][s["id"]]), f"{mi:.1f}" if mi is not None else "-"))
    out.append(("none", "None of these", _pct(res["shares"]["none"]), "-"))
    return out


def _basis(p):
    traits = p.get("traits", [])
    g = sum(t.get("basis") == "grounded" for t in traits)
    return f"{g} grounded, {len(traits) - g} assumed"


NO_GROUNDING = "No grounding data was supplied, so every persona trait is assumed."


def to_markdown(panel, res):
    nar = panel["narrative"]
    lines = [
        f"# Synthetic panel: {panel['question']}",
        "",
        f"**Segment:** {panel['segment']} | **Panel:** {res['n']} personas | "
        f"**Date:** {panel.get('date', '')} | **Run:** `{panel['run_id']}`",
        "",
        f"**Decision:** {panel.get('decision', '')}",
        "",
        f"## {nar['headline']}",
        "",
        f"**Predicted winner:** {res['winner']}, leading by {_pct(res['margin'])} | "
        f"**Confidence: {res['confidence']}**",
        "",
    ]
    lines += [f"- {r}" for r in res["confidence_reasons"]]
    lines += ["", "## Results", "", "| ID | Option | Picked by | Mean intent (1-7) |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in _rows(panel, res)]
    lines += ["", "## Quality checks", ""]
    lines += [
        f"- Decoy share: {_pct(res['decoy_share'])} (limit {_pct(aggregate.DECOY_MAX)})",
        f"- Decoy mean intent: {_intent(res['decoy_intent'])} (weak at {aggregate.WEAK_DECOY_MAX:.1f} or below)",
        f"- Largest single answer, including none: {_pct(max(res['shares'].values()))} (limit {_pct(aggregate.AGREEMENT_MAX)})",
        f"- Picked the first-shown option: {_pct(res['first_pick_rate'])}",
        f"- Persona traits grounded in data: {_pct(res['grounding_coverage'])}",
        f"- Flags: {', '.join(FLAG_TEXT[f] for f in res['flags']) if res['flags'] else 'none'}",
        "",
        "## Grounding",
        "",
    ]
    lines += [f"- **{g['id']}** {g['summary']} ({g.get('source', '')})" for g in panel.get("grounding", [])] or [NO_GROUNDING]
    lines += ["", "## Findings", ""]
    lines += [f"- **[{f['confidence']}]** {f['text']} ({f['evidence']})" for f in nar["findings"]]
    lines += ["", f"**Minority view:** {nar.get('minority_view', '')}", "", "## Top objections", ""]
    lines += [f"- {o}" for o in nar.get("objections", [])]
    lines += ["", "## Live test to settle it", "", nar["live_test"], "", "## Panel", ""]
    lines += ["| ID | Persona | Traits | Picked | Quote |", "|---|---|---|---|---|"]
    lines += [
        f"| {p['id']} | {p['name']}: {p['summary']} | {_basis(p)} | {p['response']['choice']} | \"{p['response']['quote']}\" |"
        for p in panel["personas"]
    ]
    lines += ["", "## Caveats", ""]
    lines += [f"- {c}" for c in nar.get("caveats", [])]
    lines += [
        "- Synthetic personas predict; they do not measure. Log the real outcome with "
        f"`calibration.py record {panel['run_id']} <winner>` to score this panel.",
        "",
    ]
    return "\n".join(lines)


def to_html(panel, res):
    e = html.escape
    nar = panel["narrative"]
    conf = res["confidence"]
    win = ' class="win"'
    rows = "".join(
        f"<tr{win if a == res['winner'] else ''}><td>{e(a)}</td><td>{e(b)}</td>"
        f'<td><div class="bar"><span style="width:{c}"></span></div>{e(c)}</td><td>{e(d)}</td></tr>'
        for a, b, c, d in _rows(panel, res)
    )
    checks = [
        ("Decoy share", _pct(res["decoy_share"]), "sycophancy" in res["flags"]),
        ("Decoy mean intent (1-7)", _intent(res["decoy_intent"]), "weak_decoy" in res["flags"]),
        ("Largest single answer, incl. none", _pct(max(res["shares"].values())), "homogeneity" in res["flags"]),
        ("First-shown picks", _pct(res["first_pick_rate"]), "position_bias" in res["flags"]),
        ("Traits grounded", _pct(res["grounding_coverage"]), res["grounding_coverage"] < aggregate.LOW_COVERAGE),
    ]
    check_html = "".join(
        f"<div class=\"check{' bad' if bad else ''}\"><b>{e(v)}</b><span>{e(k)}</span></div>" for k, v, bad in checks
    )
    findings = "".join(
        f"<li><span class=\"tag {e(f['confidence'].lower())}\">{e(f['confidence'])}</span>{e(f['text'])}"
        f" <em>({e(f['evidence'])})</em></li>"
        for f in nar["findings"]
    )
    people = "".join(
        f"<tr><td>{e(p['id'])}</td><td><b>{e(p['name'])}</b><br><small>{e(p['summary'])}</small></td>"
        f"<td>{e(_basis(p))}</td><td>{e(p['response']['choice'])}</td><td>&ldquo;{e(p['response']['quote'])}&rdquo;</td></tr>"
        for p in panel["personas"]
    )
    grounding = "".join(
        f"<li><b>{e(g['id'])}</b> {e(g['summary'])} <em>({e(g.get('source', ''))})</em></li>"
        for g in panel.get("grounding", [])
    ) or f"<li>{e(NO_GROUNDING)}</li>"
    body = f"""
<header><p class="eyebrow">Synthetic panel &middot; {e(panel.get('date', ''))} &middot; {res['n']} personas</p>
<h1>{e(panel['question'])}</h1>
<p class="meta"><b>Segment:</b> {e(panel['segment'])}<br><b>Decision:</b> {e(panel.get('decision', ''))}</p></header>
<section class="verdict"><div><p class="eyebrow">Predicted winner</p><p class="big">{e(res['winner'])}</p>
<p>leads by {_pct(res['margin'])}</p></div><div><p class="eyebrow">Confidence</p>
<p class="big tag {conf.lower()}">{conf}</p></div><div class="headline"><h2>{e(nar['headline'])}</h2>
<ul>{''.join(f'<li>{e(r)}</li>' for r in res['confidence_reasons'])}</ul></div></section>
<section><h3>Results</h3><table><tr><th>ID</th><th>Option</th><th>Picked by</th><th>Intent</th></tr>{rows}</table></section>
<section><h3>Quality checks</h3><div class="checks">{check_html}</div></section>
<section><h3>Grounding</h3><ul class="grounding">{grounding}</ul></section>
<section><h3>Findings</h3><ul class="findings">{findings}</ul>
<p><b>Minority view:</b> {e(nar.get('minority_view', ''))}</p>
<p><b>Top objections:</b></p><ul class="findings">{''.join(f'<li>{e(o)}</li>' for o in nar.get('objections', []))}</ul></section>
<section class="live"><h3>Live test to settle it</h3><p>{e(nar['live_test'])}</p></section>
<section><h3>Panel</h3><table class="panel"><tr><th>ID</th><th>Persona</th><th>Traits</th><th>Pick</th><th>Quote</th></tr>{people}</table></section>
<footer>{''.join(f'<p>{e(c)}</p>' for c in nar.get('caveats', []))}
<p>Run <code>{e(panel['run_id'])}</code>. Synthetic personas predict; they do not measure.</p></footer>"""
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    return template.replace("{{TITLE}}", e(panel["question"])).replace("{{BODY}}", body)


def _browser():
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    found = [c for c in candidates if os.path.exists(c)]
    found += [w for w in (shutil.which(n) for n in ("google-chrome", "chromium", "chrome")) if w]
    return found[0] if found else None


def _headless(html_path, out_path, flags, what):
    browser = _browser()
    if not browser:
        raise RuntimeError(f"Chrome or Edge not found; open the HTML to check the {what} by hand.")
    uri = "file:///" + os.path.abspath(html_path).replace("\\", "/").lstrip("/")
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000", *flags, uri],
                   check=False, capture_output=True, timeout=120)
    if not os.path.exists(out_path):
        raise RuntimeError(f"{what} export failed.")


def to_pdf(html_path, pdf_path):
    _headless(html_path, pdf_path, ["--no-pdf-header-footer", f"--print-to-pdf={os.path.abspath(pdf_path)}"], "PDF")


def to_png(html_path, png_path, width=1000, height=3200):
    _headless(html_path, png_path, ["--hide-scrollbars", f"--window-size={width},{height}",
                                    f"--screenshot={os.path.abspath(png_path)}"], "PNG")


def render(panel, out_dir, name, pdf=False, png=False):
    if not panel.get("narrative"):
        raise ValueError("panel.json needs a 'narrative' block before rendering")
    res = aggregate.summarise(panel)
    os.makedirs(out_dir, exist_ok=True)
    paths = {"md": os.path.join(out_dir, f"{name}_synthetic-panel.md"),
             "html": os.path.join(out_dir, f"{name}_synthetic-panel.html")}
    with open(paths["md"], "w", encoding="utf-8") as f:
        f.write(to_markdown(panel, res))
    with open(paths["html"], "w", encoding="utf-8") as f:
        f.write(to_html(panel, res))
    if pdf:
        paths["pdf"] = os.path.join(out_dir, f"{name}_synthetic-panel.pdf")
        to_pdf(paths["html"], paths["pdf"])
    if png:
        paths["png"] = os.path.join(out_dir, f"{name}_synthetic-panel.png")
        to_png(paths["html"], paths["png"])
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("panel")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--name", required=True)
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()
    with open(args.panel, encoding="utf-8") as f:
        panel = json.load(f)
    for kind, path in render(panel, args.out_dir, args.name, args.pdf, args.png).items():
        print(f"{kind.upper()}: {os.path.abspath(path)}")


if __name__ == "__main__":
    main()
