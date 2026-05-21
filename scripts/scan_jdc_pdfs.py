"""Scan JDC NY Office remittance PDFs (from OneDrive/Desktop/R.P.A.PORT LTD)
for any mention of the Rapaport / Weitzner / Goldfischer / Griffel families
or their hometowns (Nadwórna, Bolechów, Skole).

Output: research_cache/jdc_pdf_scan_results.json
"""
import json
import re
import sys
from pathlib import Path
import pdfplumber

REPO = Path(__file__).resolve().parent.parent
OUTDIR = REPO / "research_cache"
OUTDIR.mkdir(exist_ok=True)

PDF_DIR = Path("C:/Users/User/OneDrive/Desktop/R.P.A.PORT LTD")
PDFS = [
    "Complete_Poland_Remittances1_NY_AR1418_02446.pdf",
    "Complete_Poland Remittances 2 NY_AR1418_00090.pdf",
    "Complete_Poland_Remittances3_NYAR1921.pdf",
    "Complete_PalRemittances_July.pdf",
    "Complete_PalAugustNY_AR1418_00536.pdf",
    "Completed_Palestine Remittances NY_AR1418_00298.pdf",
    "Completed_Rem_SaffedPal_NY_AR1418_04946.pdf",
    "Complete_RomanianRem_NY_AR1418_00067.pdf",
    "Complete_RussianRemNY_AR1418.pdf",
]

# Surname patterns (case-insensitive, word-boundary)
PATTERNS = {
    # FUZZY surname matches — OCR scrambles characters frequently in old scans.
    # Allow 1-2 letter substitutions on the discriminating syllables.
    "Rap[aeo]p?ort": re.compile(r"R[aeo].{0,1}p[aeo].?ort", re.IGNORECASE),  # Rapaport / Rapoport
    "Weitzner":     re.compile(r"W[aeio]?[ie]t[cz][hn]?n?[ei]?r", re.IGNORECASE),
    "Goldfischer":  re.compile(r"Goldfi(?:s|sch|sh)[ehrz]+", re.IGNORECASE),
    "Griffel":      re.compile(r"Gr[aeio]+f+el", re.IGNORECASE),
    "Nadworna":     re.compile(r"Nad[wv][oó0]?rna|Nadv[oó]rna|Nadwornaya|Nadwirna", re.IGNORECASE),
    "Bolechow":     re.compile(r"Bolech[oó0]w|Bolekhiv|Bolechow", re.IGNORECASE),
    "Skole":        re.compile(r"\bSkole\b", re.IGNORECASE),
    "Memek":        re.compile(r"\bM[ey]m[ei]k\b", re.IGNORECASE),
    "Berisz":       re.compile(r"\bBer[aiy]s[zh]?\b", re.IGNORECASE),
    "Lusia":        re.compile(r"\b(Lusia|Lucia|Łucja|Lutsia|Leah)\b", re.IGNORECASE),
    # Geography that COULD validate the dataset's relevance to our family
    "Galicia":      re.compile(r"\bGalicia\b|\bGalicien\b", re.IGNORECASE),
    "Stanislawow":  re.compile(r"\bStanisla(?:u|w)[oó]w\b|\bStanislaw[oó]w\b", re.IGNORECASE),
    "Stryj":        re.compile(r"\bStr[yi]j\b", re.IGNORECASE),
    "Lwow":         re.compile(r"\bLw[oó]w\b|\bLemberg\b|\bL'?viv\b", re.IGNORECASE),
    "Tarnobrzeg":   re.compile(r"\bTarnobrzeg\b", re.IGNORECASE),
    "Muszyna":      re.compile(r"\bMuszyna\b|\bMosina\b", re.IGNORECASE),
}

def scan_pdf(path):
    name = path.name
    print(f"\n[{name}] opening (size: {path.stat().st_size//1024} KB)…", flush=True)
    matches = {k: [] for k in PATTERNS}
    pages_searched = 0
    pages_no_text = 0
    try:
        with pdfplumber.open(str(path)) as pdf:
            total = len(pdf.pages)
            print(f"  {total} pages", flush=True)
            for i, page in enumerate(pdf.pages, start=1):
                try:
                    txt = page.extract_text() or ""
                except Exception:
                    txt = ""
                if not txt.strip():
                    pages_no_text += 1
                    continue
                pages_searched += 1
                for label, rx in PATTERNS.items():
                    for m in rx.finditer(txt):
                        start = max(0, m.start() - 100)
                        end = min(len(txt), m.end() + 150)
                        snippet = txt[start:end].replace("\n", " ").strip()
                        matches[label].append({"page": i, "snippet": snippet[:400]})
                if i % 50 == 0:
                    print(f"  …scanned p.{i}/{total}", flush=True)
    except Exception as e:
        return {"file": name, "error": str(e)}
    nonzero = {k: v for k, v in matches.items() if v}
    return {
        "file": name,
        "pages_total": total if 'total' in locals() else 0,
        "pages_with_text": pages_searched,
        "pages_no_text": pages_no_text,
        "matches": nonzero,
        "match_counts": {k: len(v) for k, v in nonzero.items()},
    }

results = []
for fname in PDFS:
    p = PDF_DIR / fname
    if not p.exists():
        print(f"MISSING: {p}", flush=True)
        continue
    results.append(scan_pdf(p))

out = OUTDIR / "jdc_pdf_scan_results.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n=== DONE ===")
print(f"Results: {out.relative_to(REPO)}")
print()
# Summary
total_hits = 0
for r in results:
    counts = r.get("match_counts", {})
    if counts:
        print(f"{r['file']}: {dict(counts)}")
        total_hits += sum(counts.values())
print(f"\nTotal hits across all files: {total_hits}")
