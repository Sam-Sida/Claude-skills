"""Render page 1 of a PDF to PNG so the filled canvas can be visually checked.

Usage: python render_preview.py <input.pdf> <output.png>
"""
import sys

import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(sys.argv[1])
pdf[0].render(scale=2).to_pil().save(sys.argv[2])
print(f"wrote {sys.argv[2]}")
