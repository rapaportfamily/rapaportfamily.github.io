"""Re-translate critical pages with Claude Sonnet 4.5 and compare against
Claude Haiku 4.5's earlier translations. Surfaces translation deltas so we can
catch missed proper-noun spellings, work-permit details, place names, etc.

Critical pages = those mentioning David's wartime work, family businesses,
proper nouns, and the few anomalies we've flagged.

Reads:  platform/data/memoir_pages.json (existing Haiku translations)
Writes: platform/data/memoir_pages_sonnet_diff.json (Sonnet output + diff)
"""
import json
import sys
from pathlib import Path
from difflib import SequenceMatcher

import anthropic

REPO = Path(__file__).resolve().parent.parent
KEY_PATH = Path(r"C:\Users\User\AppData\Local\Temp\_ak.txt")
PAGES_IN = REPO / "platform" / "data" / "memoir_pages.json"
DIFF_OUT = REPO / "platform" / "data" / "memoir_pages_sonnet_diff.json"

# Pages with high information density / proper nouns / wartime work details
CRITICAL_PAGES = [
    3, 7, 12, 13, 17, 24, 25, 27, 28, 32, 33, 37, 41, 42, 43, 44, 45, 48, 50, 51,
    56, 62, 63, 64, 65, 78
]

client = anthropic.Anthropic(api_key=KEY_PATH.read_text(encoding="utf-8").strip())
MODEL = "claude-sonnet-4-5-20250929"

pages = json.loads(PAGES_IN.read_text(encoding="utf-8"))
critical = [p for p in pages if p.get("page") in CRITICAL_PAGES and (p.get("hebrew") or "").strip()]
print(f"[Sonnet] re-translating {len(critical)} critical pages")

SYSTEM = """You are translating a Hebrew Holocaust-survivor memoir into English with the utmost care for proper nouns, dates, and historical accuracy.

THE MEMOIR is "סיפורה של לוסיה" (The Story of Lusia) by Leah/Lusia Rapaport née Weitzner.

CONTEXT THAT MATTERS:
- Lusia's husband is David Mendel "Memek" Rapaport, born 1911 Nadwórna (Polish: Nadwórna; Ukrainian: Надвірна; in Galicia). Forestry engineer.
- Lusia herself born 1913 in Bolechów (Polish; Ukrainian: Болехів) Ruski.
- They lived in Lwów (Polish; Ukrainian: Львів; English often "Lvov" or "Lviv") during 1940-1944.
- During Nazi occupation, David worked at a SAWMILL in Nadwórna. The Germans issued him an Arbeitskarte / Sonderausweis / "essential worker" badge that let him leave the ghetto.
- During the Nadwórna ghetto liquidation (October 1942), David and 17 other Jews escaped by hiding in train wagons full of wood that he had drilled escape-holes in.
- David's sister Lota perished in the Lwów ghetto after buying forged US emigration documents from sellers who betrayed her to the Gestapo.
- Lusia's family (Weitzner): father Elias was a CATTLE DEALER then owned a TANNERY in Bolechów. Mother Matel née Weinreb from Dolina. Sister Tzipora/Feige emigrated to Palestine 1932.
- Polish woman Maria Ciccelik gave Lusia her birth certificate, which Lusia used as her false identity during the war ("Maria Cizlik" in Hebrew text).
- Place names — render in BOTH Polish and Ukrainian where useful: Lwów (now Lviv), Bolechów (now Bolekhiv), Nadwórna (now Nadvirna), Stanisławów (now Ivano-Frankivsk).

TRANSLATION RULES:
- Preserve proper nouns EXACTLY as they appear in the Hebrew. If you see בעלעצוואק spell out as "Bel(e)tsv(o)ak" or whatever the Hebrew suggests, NOT what you think the place should be.
- Translate Hebrew month names + dates literally.
- DO NOT add interpretation or context inside the translation — keep that for the notes field.
- If you spot a clear OCR error in the Hebrew (e.g. a single letter looks wrong), translate what's there but flag it in notes.

OUTPUT format (JSON only, no markdown):
{
  "english": "<the translation, full text>",
  "translator_notes": "<bullet points of: proper nouns identified, OCR concerns, ambiguous passages, any historical context flags you'd attach>"
}"""

results = []
total_in, total_out = 0, 0
for p in critical:
    pn = p.get("page")
    he = p.get("hebrew", "")
    haiku_en = p.get("english", "")
    print(f"  [Sonnet] re-translating page {pn} ({len(he)} chars Hebrew)…")
    user = f"Page {pn} of the memoir. Hebrew source:\n\n{he}\n\nReturn JSON only."
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user}],
    )
    total_in += resp.usage.input_tokens
    total_out += resp.usage.output_tokens
    raw = resp.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    try:
        parsed = json.loads(raw)
        sonnet_en = parsed.get("english", "")
        notes = parsed.get("translator_notes", "")
    except json.JSONDecodeError as e:
        print(f"    [WARN] couldn't parse JSON for page {pn}: {e}")
        sonnet_en = raw
        notes = "(JSON parse error)"

    similarity = SequenceMatcher(None, haiku_en, sonnet_en).ratio()
    results.append({
        "page": pn,
        "page_kind": p.get("page_kind", ""),
        "haiku_translation": haiku_en,
        "sonnet_translation": sonnet_en,
        "translator_notes": notes,
        "similarity": round(similarity, 3),
        "haiku_len": len(haiku_en),
        "sonnet_len": len(sonnet_en),
    })

cost = (total_in / 1_000_000) * 3.0 + (total_out / 1_000_000) * 15.0
print(f"\n[usage] input={total_in} tok, output={total_out} tok, cost=${cost:.4f}")

DIFF_OUT.write_text(json.dumps({
    "model": MODEL,
    "pages_assessed": len(results),
    "total_cost_usd": round(cost, 4),
    "input_tokens": total_in,
    "output_tokens": total_out,
    "results": results,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] diff -> {DIFF_OUT}")

# Print biggest-divergence pages
results.sort(key=lambda r: r["similarity"])
print(f"\n=== TOP 10 MOST-DIVERGENT PAGES (Sonnet vs Haiku) ===")
for r in results[:10]:
    print(f"  p.{r['page']:>3} — similarity {r['similarity']:.2f} — len Haiku {r['haiku_len']} → Sonnet {r['sonnet_len']}")
    if r.get("translator_notes"):
        notes_short = r["translator_notes"][:200] if isinstance(r["translator_notes"], str) else json.dumps(r["translator_notes"])[:200]
        print(f"       notes: {notes_short}")
