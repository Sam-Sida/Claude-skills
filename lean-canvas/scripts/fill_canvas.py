"""Fill the Lean Canvas PDF template with content from a JSON file.

Usage:
    python fill_canvas.py <content.json> <output.pdf> [--template <template.pdf>]

The JSON schema is documented in ../SKILL.md. Each section is a list of
strings; prefix an item with "[i] " to mark it as inferred (rendered in
italics). Text is auto-sized per box so everything fits.
"""
import argparse
import io
import json
import os
import sys
from xml.sax.saxutils import escape

try:
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph, Frame, KeepInFrame
except ImportError:
    sys.exit("Missing dependencies. Run: <python> -m pip install --user pypdf reportlab")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "..", "assets", "lean-canvas-template.pdf")
BLANK_PAGE_INDEX = 1  # page 2 of the template is the empty canvas
PAGE_W, PAGE_H = 780, 540

TEXT = HexColor("#333333")
INFERRED = HexColor("#555577")
MUTED = HexColor("#777777")

# Writable area of each box in PDF points: (x0, y_bottom, x1, y_top).
# Columns start at 19.25 / 167.25 / 315.375 / 463.375 / 611.875 (width ~148);
# the label + icon row takes the top ~28pt of every box.
BOXES = {
    "problem":               (24, 336, 163, 448),
    "existing_alternatives": (24, 184, 163, 300),
    "solution":              (172, 336, 311, 448),
    "key_metrics":           (172, 184, 311, 300),
    "unique_value_prop":     (320, 336, 459, 448),
    "high_level_concept":    (320, 184, 459, 300),
    "unfair_advantage":      (468, 336, 607, 448),
    "channels":              (468, 184, 607, 300),
    "customer_segments":     (616, 336, 755, 448),
    "early_adopters":        (616, 184, 755, 300),
    "cost_structure":        (24, 40, 386, 150),
    "revenue_streams":       (395, 40, 755, 150),
}

# White header fields: (x0, y_bottom, x1, y_top)
HEADER = {
    "designed_for": (311.8, 492, 422.6, 510.4),
    "designed_by":  (447.5, 492, 558.3, 510.4),
    "date":         (611.0, 492, 702.4, 510.4),
    "version":      (727.8, 492, 760.5, 510.4),
}

FONT, FONT_I, FONT_B = "Helvetica", "Helvetica-Oblique", "Helvetica-Bold"


def register_fonts():
    """Prefer Arial (wide Unicode coverage) when available; else Helvetica."""
    global FONT, FONT_I, FONT_B
    candidates = [
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
        "/Library/Fonts", "/System/Library/Fonts/Supplemental",
        "/usr/share/fonts/truetype/msttcorefonts",
    ]
    for d in candidates:
        files = {k: os.path.join(d, f) for k, f in
                 (("r", "arial.ttf"), ("i", "ariali.ttf"), ("b", "arialbd.ttf"))}
        if all(os.path.exists(p) for p in files.values()):
            pdfmetrics.registerFont(TTFont("Arial", files["r"]))
            pdfmetrics.registerFont(TTFont("Arial-Italic", files["i"]))
            pdfmetrics.registerFont(TTFont("Arial-Bold", files["b"]))
            from reportlab.lib.fonts import addMapping
            addMapping("Arial", 0, 0, "Arial")
            addMapping("Arial", 0, 1, "Arial-Italic")
            addMapping("Arial", 1, 0, "Arial-Bold")
            addMapping("Arial", 1, 1, "Arial-Bold")
            FONT, FONT_I, FONT_B = "Arial", "Arial-Italic", "Arial-Bold"
            return


def item_markup(item):
    """Convert one list item to Paragraph markup. Supports **bold** and [i] prefix."""
    inferred = item.startswith("[i] ")
    if inferred:
        item = item[4:]
    text = escape(item)
    # **bold** segments
    parts = text.split("**")
    text = "".join(f"<b>{p}</b>" if i % 2 else p for i, p in enumerate(parts))
    if inferred:
        text = f'<i><font color="#555577">{text}</font></i>'
    return text


def build_paragraphs(items, size, bullets=True):
    style = ParagraphStyle(
        "c", fontName=FONT, fontSize=size, leading=size * 1.22, textColor=TEXT,
        leftIndent=size * 0.9 if bullets else 0,
        bulletIndent=0, bulletFontName=FONT, bulletFontSize=size,
        spaceAfter=size * 0.35,
    )
    paras = []
    for it in items:
        if bullets:
            paras.append(Paragraph(item_markup(it), style, bulletText="\u2022"))
        else:
            paras.append(Paragraph(item_markup(it), style))
    return paras


def fits(items, size, w, h, bullets):
    total = 0
    for p in build_paragraphs(items, size, bullets):
        _, ph = p.wrap(w, h)
        total += ph + p.style.spaceAfter
    return total - (size * 0.35) <= h


def draw_box(c, items, rect, max_size=8.5, min_size=4.5):
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    if isinstance(items, str):
        items = [items]
    items = [i for i in items if i and i.strip()]
    if not items:
        return
    bullets = len(items) > 1
    size = max_size
    while size > min_size and not fits(items, size, w, h, bullets):
        size -= 0.25
    paras = build_paragraphs(items, size, bullets)
    if not fits(items, size, w, h, bullets):
        print(f"warning: content shrunk to fit box at {rect}; consider shortening it",
              file=sys.stderr)
        paras = [KeepInFrame(w, h, paras, mode="shrink")]
    f = Frame(x0, y0, w, h, leftPadding=0, rightPadding=0, topPadding=0,
              bottomPadding=0, showBoundary=0)
    f.addFromList(paras, c)


def draw_header_field(c, text, rect):
    if not text:
        return
    x0, y0, x1, y1 = rect
    w = x1 - x0 - 6
    size = 8.5
    while size > 4.5 and pdfmetrics.stringWidth(text, FONT, size) > w:
        size -= 0.25
    c.setFont(FONT, size)
    c.setFillColor(TEXT)
    c.drawString(x0 + 3, y0 + (y1 - y0 - size) / 2 + 1.5, text)


def make_overlay(data):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    for key, rect in HEADER.items():
        draw_header_field(c, str(data.get(key, "") or ""), rect)
    sections = data.get("sections", {})
    for key, rect in BOXES.items():
        draw_box(c, sections.get(key, []), rect)
    # Legend just above the footer credit line
    legend = data.get("legend",
                      "Italic = inferred from public signals; regular = publicly reported. "
                      "Sources on page 2.")
    if legend:
        c.setFont(FONT_I, 5.5)
        c.setFillColor(MUTED)
        c.drawRightString(760, 30, legend)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def make_sources_page(data):
    sources = data.get("sources", [])
    notes = data.get("notes", [])
    if not sources and not notes:
        return []
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    title = ParagraphStyle("t", fontName=FONT_B, fontSize=16, leading=20, textColor=TEXT)
    h2 = ParagraphStyle("h", fontName=FONT_B, fontSize=10, leading=14, textColor=TEXT,
                        spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("b", fontName=FONT, fontSize=7.5, leading=9.5, textColor=TEXT,
                          leftIndent=10, bulletIndent=0, spaceAfter=2)
    story = [Paragraph(escape(f"Lean Canvas: {data.get('designed_for', '')} - "
                              "Research notes & sources"), title)]
    if notes:
        story.append(Paragraph("Methodology & assumptions", h2))
        story += [Paragraph(escape(n), body, bulletText="\u2022") for n in notes]
    if sources:
        story.append(Paragraph("Sources", h2))
        for i, s in enumerate(sources, 1):
            if isinstance(s, dict):
                t, u = escape(s.get("title", "")), escape(s.get("url", ""))
                txt = f'{t} - <link href="{u}" color="blue">{u}</link>' if u else t
            else:
                txt = escape(str(s))
            story.append(Paragraph(txt, body, bulletText=f"{i}."))
    pages = []
    remaining = story
    while remaining:
        f = Frame(30, 30, PAGE_W - 60, PAGE_H - 60, showBoundary=0)
        before = len(remaining)
        f.addFromList(remaining, c)
        c.showPage()
        if len(remaining) == before:
            break
    c.save()
    buf.seek(0)
    return list(PdfReader(buf).pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("output")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    args = ap.parse_args()

    with open(args.content, encoding="utf-8") as fh:
        data = json.load(fh)

    register_fonts()
    template = PdfReader(args.template)
    page = template.pages[BLANK_PAGE_INDEX]
    page.merge_page(make_overlay(data))

    writer = PdfWriter()
    writer.add_page(page)
    for p in make_sources_page(data):
        writer.add_page(p)
    writer.add_metadata({"/Title": f"Lean Canvas - {data.get('designed_for', '')}",
                         "/Author": data.get("designed_by", "")})
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "wb") as fh:
        writer.write(fh)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
