"""Generate two exports of Lusia's memoir for downstream use:

1. memoir.xml — structured XML with per-page hebrew + en + pl + ocr meta + extracted entities.
   Useful for cross-checking, XSLT pipelines, archival.

2. memoir_notebook.txt — single plain-text export with structured headings,
   designed to be uploaded to Google NotebookLM, Claude Projects, or any LLM.
   Includes Hebrew + English side by side per page, plus a structured summary.

3. memoir_facts.json — every Hebrew entity extracted by hebrew_regex.py
   (dates, places, people, addresses) with page references and surrounding context.

Run:  python scripts/export_memoir.py
"""
from __future__ import annotations
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hebrew_regex import HebrewExtractor, facts_to_dict

REPO = Path(__file__).resolve().parent.parent
PAGES_JSON = REPO / "platform" / "data" / "memoir_pages.json"
META_JSON  = REPO / "platform" / "data" / "memoir.json"
TIMELINE_JSON = REPO / "platform" / "data" / "memoir_timeline_verified.json"
OUT_XML    = REPO / "platform" / "data" / "memoir.xml"
OUT_NB     = REPO / "platform" / "data" / "memoir_notebook.txt"
OUT_FACTS  = REPO / "platform" / "data" / "memoir_facts.json"
OUT_REPORT = REPO / "docs" / "research" / "memoir_extraction_2026-05-20.md"

if not PAGES_JSON.exists():
    print(f"[ERR] {PAGES_JSON} missing — run OCR first", file=sys.stderr)
    sys.exit(1)

meta = json.loads(META_JSON.read_text(encoding="utf-8")) if META_JSON.exists() else {}
pages = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
pages.sort(key=lambda p: p.get("page", 0))

# ── 1) XML export ──────────────────────────────────────────────────
root = ET.Element("memoir", attrib={
    "title-he": meta.get("title_he", ""),
    "title-en": meta.get("title_en", ""),
    "title-pl": meta.get("title_pl", ""),
    "author": meta.get("author", ""),
    "pages": str(meta.get("pages", len(pages))),
    "ocr-method": meta.get("ocr_method", ""),
})
for p in pages:
    page_el = ET.SubElement(root, "page", attrib={
        "n": str(p.get("page", "")),
        "kind": p.get("page_kind", ""),
        "ocr-confidence": p.get("ocr_confidence", ""),
        "claude-review-needed": "true" if p.get("claude_review_needed") else "false",
    })
    he = ET.SubElement(page_el, "hebrew"); he.text = p.get("hebrew", "")
    en = ET.SubElement(page_el, "english"); en.text = p.get("english", "")
    pl = ET.SubElement(page_el, "polish"); pl.text = p.get("polish", "")
    if p.get("ocr_notes"):
        notes = ET.SubElement(page_el, "ocr-notes"); notes.text = p["ocr_notes"]
    cs = p.get("ocr_consensus") or {}
    if cs:
        consensus = ET.SubElement(page_el, "ocr-consensus", attrib={
            "avg-similarity": str(cs.get("avg_similarity", "")),
        })
        for engine in (cs.get("engines_used") or []):
            e_el = ET.SubElement(consensus, "engine")
            e_el.text = engine

# Embed verified timeline into XML
if TIMELINE_JSON.exists():
    tl = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
    tl_el = ET.SubElement(root, "verified-timeline", attrib={
        "events-total": str(len(tl.get("events", []))),
        "verification-method": tl.get("verification_method", ""),
    })
    cs = tl.get("cost_summary", {})
    cost_el = ET.SubElement(tl_el, "cost-summary")
    for k, v in cs.items():
        ET.SubElement(cost_el, "item", attrib={"key": str(k)}).text = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    for ev in tl.get("events", []):
        v = ev.get("verification", {})
        ev_el = ET.SubElement(tl_el, "event", attrib={
            "page": str(ev.get("page", "")),
            "date": str(ev.get("date") or ""),
            "verified": str(v.get("verified", False)).lower(),
            "confidence": str(v.get("confidence", "")),
            "method": str(v.get("method", "")),
        })
        ET.SubElement(ev_el, "title").text = ev.get("title", "")
        ET.SubElement(ev_el, "description").text = ev.get("description", "")
        if v.get("side_note"):
            ET.SubElement(ev_el, "side-note").text = v["side_note"]
        if v.get("historical_context"):
            ET.SubElement(ev_el, "historical-context").text = v["historical_context"]
        for aid in (v.get("anchor_ids") or []):
            ET.SubElement(ev_el, "anchor", attrib={"id": aid})

tree = ET.ElementTree(root)
ET.indent(tree, space="  ")
tree.write(str(OUT_XML), encoding="utf-8", xml_declaration=True)
print(f"[ok] wrote {OUT_XML}")

# ── 2) LLM-notebook export ──────────────────────────────────────────
lines = [
    "=" * 78,
    "THE STORY OF LUSIA (סיפורה של לוסיה)",
    f"Author: {meta.get('author','')}",
    f"Pages: {meta.get('pages',len(pages))}",
    f"OCR method: {meta.get('ocr_method','')}",
    "Compiled for the Rapaport family tree archive.",
    "Source PDF: platform/assets/documents/lusia_memoir.pdf",
    "",
    "This document is the OCR'd and translated text of a Hebrew Holocaust-survivor memoir.",
    "Hebrew is the original; English and Polish are AI translations cross-checked with multi-engine OCR.",
    "Marks: [?] = single illegible character; [illegible] = unclear passage.",
    "=" * 78,
    "",
]
for p in pages:
    pn = p.get("page", "?")
    kind = p.get("page_kind", "")
    lines += [
        "",
        f"--- PAGE {pn} {'(' + kind + ')' if kind else ''} " + "-" * (60 - len(str(pn)) - len(kind)),
        "",
        f"HEBREW (original):",
        p.get("hebrew", "") or "(no Hebrew text on this page)",
        "",
        f"ENGLISH translation:",
        p.get("english", "") or "(no translation)",
        "",
        f"POLISH translation:",
        p.get("polish", "") or "(brak tłumaczenia)",
    ]
    if p.get("ocr_notes"):
        lines.append(f"OCR notes: {p['ocr_notes']}")
    if p.get("claude_review_needed"):
        lines.append("⚠ Page flagged for Claude review — Hebrew OCR engines disagreed.")
# Append verified timeline section
if TIMELINE_JSON.exists():
    tl = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
    cs = tl.get("cost_summary", {})
    lines += [
        "",
        "=" * 78,
        "VERIFIED TIMELINE — 63 events extracted and cross-checked",
        "=" * 78,
        f"Verification method: regex anchors (free) → Claude Sonnet 4.5 (paid, ${cs.get('total_cost_usd', 0):.4f} total)",
        f"Verified: {cs.get('verified', '?')}/{cs.get('events_total', '?')}",
        f"Open questions: {cs.get('needs_followup', '?')}",
        f"Categories: {cs.get('category_breakdown', {})}",
        "",
        "Each event has: page, date, title, description, verification verdict + reasoning.",
        "Categories: CORROBORATED (matches documented history) / PLAUSIBLE (consistent with",
        "era but personal detail) / PLACE_KNOWN (location in our gazetteer) / HIGH (regex anchor",
        "match) / MEMOIR_FACTUAL_ANOMALY (historical record contradicts — preserved as testimony).",
        "",
    ]
    by_year = sorted(tl.get("events", []), key=lambda e: (str(e.get("date") or "9999"), e.get("page") or 999))
    for ev in by_year:
        v = ev.get("verification", {})
        lines += [
            "-" * 78,
            f"[{ev.get('date') or 'undated'}] p.{ev.get('page','?')} — {ev.get('title','')}",
            f"  Description: {ev.get('description','')}",
            f"  Verification: {v.get('confidence','?').upper()} (via {v.get('method','?')})",
            f"  Note: {v.get('side_note','')}",
        ]
        if v.get("historical_context"):
            lines.append(f"  Context: {v['historical_context']}")
        if v.get("preserve_as_testimony"):
            lines.append(f"  ⚠ PRESERVED AS LUSIA'S TESTIMONY despite historical anomaly.")
        lines.append("")

OUT_NB.write_text("\n".join(lines), encoding="utf-8")
print(f"[ok] wrote {OUT_NB} ({len(lines)} lines, {OUT_NB.stat().st_size:,} bytes)")

# ── 3) Hebrew regex entity extraction ───────────────────────────────
ext = HebrewExtractor()
all_facts = {"dates": [], "years": [], "ages": [], "places": [], "people": [], "addresses": []}
for p in pages:
    he = p.get("hebrew", "") or ""
    if not he:
        continue
    facts = ext.extract(he)
    for cat, items in facts.items():
        for f in items:
            d = {"page": p.get("page"), "text": f.text, "type": f.type, "value": f.value,
                 "id_ref": f.id_ref, "context_before": f.context_before, "context_after": f.context_after}
            all_facts[cat].append(d)

OUT_FACTS.write_text(json.dumps(all_facts, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[ok] wrote {OUT_FACTS}")

# ── 4) Quick research report skeleton (Claude will fill it in next session) ──
unique_places = sorted({f["text"]: f["id_ref"] for f in all_facts["places"]}.items())
unique_people = sorted({f["text"]: f["id_ref"] for f in all_facts["people"]}.items())
years_sorted = sorted({int(f["value"]) for f in all_facts["years"] if isinstance(f["value"], int)})
diverged_pages = [p["page"] for p in pages if p.get("claude_review_needed")]

OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
OUT_REPORT.write_text(f"""# Memoir extraction — round 1 (2026-05-20)

**Source**: Lusia (Leah) Rapaport née Weitzner, *סיפורה של לוסיה*, {meta.get('pages', '?')} pages, OCR'd via {meta.get('ocr_method', 'multi-engine')}.

## Summary

- **Total Hebrew chars OCR'd**: {sum(len(p.get('hebrew','') or '') for p in pages):,}
- **Pages with content**: {sum(1 for p in pages if p.get('hebrew',''))}
- **Pages flagged for Claude review** (OCR engines diverged): {len(diverged_pages)} → {diverged_pages[:20]}{'…' if len(diverged_pages) > 20 else ''}

## Entities extracted (Hebrew regex toolkit)

- **Unique places mentioned**: {len(unique_places)} → see `platform/data/memoir_facts.json`
- **Unique people mentioned**: {len(unique_people)}
- **Year span**: {years_sorted[0] if years_sorted else '?'} – {years_sorted[-1] if years_sorted else '?'}
- **Dated events**: {len(all_facts['dates'])}
- **Addresses**: {len(all_facts['addresses'])}

## Places that map to our existing places.json (auto-linked)

| Hebrew | place_id |
|---|---|
{chr(10).join(f'| {he} | `{pid}` |' for he, pid in unique_places if pid)}

## Places mentioned but not yet in places.json (NEW — may need adding)

{chr(10).join(f'- {he}' for he, pid in unique_places if pid is None)}

## People that map to our existing people.json (auto-linked)

| Hebrew | person_id |
|---|---|
{chr(10).join(f'| {he} | `{pid}` |' for he, pid in unique_people if pid)}

## People mentioned but not yet in people.json (NEW — may need adding)

{chr(10).join(f'- {he}' for he, pid in unique_people if pid is None)}

## Next steps

1. **Claude reviews flagged pages** ({len(diverged_pages)}) for OCR fidelity
2. **Cross-reference dated events** against `platform/data/events.json` — propose new events where the memoir adds dates
3. **Cross-reference addresses** (e.g. Legionów 24 Lwów) against family memory in people.json
4. **Update `h_leah_shimon_survival` hypothesis** with memoir-confirmed details (move from `family_oral` to `documented`)

*Generated by `scripts/export_memoir.py`.*
""", encoding="utf-8")
print(f"[ok] wrote {OUT_REPORT}")
print()
print(f"=== SUMMARY ===")
print(f"Pages OCR'd: {len(pages)} (of {meta.get('pages','?')})")
print(f"Pages flagged for review: {len(diverged_pages)}")
print(f"Unique places: {len(unique_places)} ({sum(1 for _, pid in unique_places if pid)} linked)")
print(f"Unique people: {len(unique_people)} ({sum(1 for _, pid in unique_people if pid)} linked)")
print(f"Year span: {years_sorted[0] if years_sorted else '?'} – {years_sorted[-1] if years_sorted else '?'}")
