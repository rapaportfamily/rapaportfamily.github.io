"""Merge Sonnet retranslations + translator notes back into memoir_pages.json.

Strategy: keep the Haiku translation as `english_haiku` (for transparency/diffing),
overwrite `english` with Sonnet (higher quality), add `translator_notes` per page.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAGES_IN = REPO / "platform" / "data" / "memoir_pages.json"
DIFF = REPO / "platform" / "data" / "memoir_pages_sonnet_diff.json"

pages = json.loads(PAGES_IN.read_text(encoding="utf-8"))
diff = json.loads(DIFF.read_text(encoding="utf-8"))
by_page = {r["page"]: r for r in diff["results"]}

updated = 0
for p in pages:
    if p.get("page") in by_page:
        r = by_page[p["page"]]
        p["english_haiku"] = p.get("english", "")  # preserve original
        p["english"] = r["sonnet_translation"]
        p["english_translator"] = "claude-sonnet-4-5-20250929"
        p["translator_notes"] = r.get("translator_notes", "")
        updated += 1

PAGES_IN.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] merged Sonnet retranslations into {updated} pages")
print(f"[OK] kept Haiku original as 'english_haiku' field for the same pages")
