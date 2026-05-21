"""OCR the JDC Bricha PDFs (image-only scans 1946) for our family names.

PyMuPDF (fitz) extracts each page as an image; Tesseract OCRs to text;
we search for Rapaport / Weitzner / Goldfischer / Galician-town variants.

Output:
  - research_cache/jdc_bricha_ocr_results.json  (matches with page refs)
  - research_cache/jdc_bricha_ocr_pages/PAGE_NNN.txt  (full OCR text per page, for human review)

Page rendering: 200 DPI (balanced quality/speed). Tesseract --psm 6 (assume
uniform block of text) since the PDFs are mostly typewritten name lists.
"""
import json
import os
import re
import sys
from pathlib import Path

# Point pytesseract at the installed binary
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import fitz  # PyMuPDF
from PIL import Image
import io

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research_cache" / "jdc_bricha_ocr_results.json"
PAGE_DIR = REPO / "research_cache" / "jdc_bricha_ocr_pages"
PAGE_DIR.mkdir(parents=True, exist_ok=True)

PDF_DIR = Path("C:/Users/User/OneDrive/Desktop/R.P.A.PORT LTD")
PDFS = [
    "Complete_Bricha2.pdf",
    "Complete_Bricha3.pdf",
]

# Surname patterns — OCR-tolerant (allow common confusions)
PATTERNS = {
    "Rapaport":   re.compile(r"R[ae][ip]?[ae][p]?[oa]rt", re.IGNORECASE),
    "Rapoport":   re.compile(r"R[ae][ip]?[op]p?ort", re.IGNORECASE),
    "Weitzner":   re.compile(r"W[ae]i?t[czs]+n[eai]?r", re.IGNORECASE),
    "Goldfischer":re.compile(r"Goldfi[s]?[csh]+[eai]?[rh]+", re.IGNORECASE),
    "Griffel":    re.compile(r"Gr[aei]+f+[ea]l", re.IGNORECASE),
    "Nadworna":   re.compile(r"Nad[wv][o0óao]r?na|Nadvi[r]?na", re.IGNORECASE),
    "Bolechow":   re.compile(r"Bolech[oó0]w|Bolekhiv", re.IGNORECASE),
    "Skole":      re.compile(r"\bSkole\b", re.IGNORECASE),
    "Lwow":       re.compile(r"\bLw[oó0]w\b|\bLemberg\b|\bL[vV]iv\b", re.IGNORECASE),
    "Berisz":     re.compile(r"\bBer[aiy][ss][zh]?\b", re.IGNORECASE),
    "David":      re.compile(r"\bDav[ie]d\b|\bDawid\b", re.IGNORECASE),
    "Memek":      re.compile(r"\bM[ey]m[ei]k\b", re.IGNORECASE),
    "Lusia":      re.compile(r"\b(Lusia|Lusha|Lucia|Łucja|Lutsia|Leah\s+Weitzner|Leah\s+Rapaport)\b", re.IGNORECASE),
}


def ocr_pdf(path, save_pages=True):
    name = path.name
    print(f"\n[{name}] opening (size: {path.stat().st_size//1024//1024} MB)…", flush=True)
    doc = fitz.open(str(path))
    total = doc.page_count
    print(f"  {total} pages → OCR ~{total*2}s minimum", flush=True)
    matches = {k: [] for k in PATTERNS}
    pages_done = 0
    sub_dir = PAGE_DIR / name.replace(".pdf", "")
    sub_dir.mkdir(exist_ok=True)
    for i in range(total):
        page = doc[i]
        # Render at 200 DPI
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        try:
            text = pytesseract.image_to_string(img, config="--psm 6")
        except Exception as e:
            text = ""
            print(f"  p.{i+1} OCR error: {e}", flush=True)
        # Save page text for human review
        if save_pages and text.strip():
            (sub_dir / f"p_{i+1:04d}.txt").write_text(text, encoding="utf-8")
        pages_done += 1
        # Match patterns
        for label, rx in PATTERNS.items():
            for m in rx.finditer(text):
                start = max(0, m.start() - 100)
                end = min(len(text), m.end() + 200)
                snippet = text[start:end].replace("\n", " ").strip()
                matches[label].append({
                    "page": i + 1,
                    "snippet": snippet[:400],
                })
        if (i + 1) % 25 == 0:
            print(f"  …p.{i+1}/{total} (hits so far: {sum(len(v) for v in matches.values())})", flush=True)
    doc.close()
    nonzero = {k: v for k, v in matches.items() if v}
    return {
        "file": name,
        "pages_total": total,
        "pages_done": pages_done,
        "match_counts": {k: len(v) for k, v in nonzero.items()},
        "matches": nonzero,
    }


results = []
for fname in PDFS:
    p = PDF_DIR / fname
    if not p.exists():
        print(f"MISSING: {p}", flush=True)
        continue
    results.append(ocr_pdf(p))

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print()
print(f"=== DONE ===")
print(f"Results: {OUT.relative_to(REPO)}")
print(f"Page text dumps: {PAGE_DIR.relative_to(REPO)}")
print()
total_hits = 0
for r in results:
    counts = r.get("match_counts", {})
    if counts:
        print(f"{r['file']}: {counts}")
        total_hits += sum(counts.values())
print(f"\nTotal hits across all files: {total_hits}")
