"""Layer 2 verification — calls Gemini 2.5 Flash (free tier) on each queued event.

Reads:  docs/research/memoir_verify_queue.json
Writes: docs/research/memoir_verify_gemini_results.json
        platform/data/memoir_timeline_verified.json  (updated in place)

Doctrine:
- One short prompt per event, asks Gemini to classify the claim against
  the historical record (CORROBORATED / PLAUSIBLE / UNVERIFIABLE / CONTRADICTED).
- Gemini paraphrases — never quote verbatim. Keeps cost at $0 (free tier).
- Sleeps 4s between calls to stay under 15 RPM free-tier ceiling.
"""
import json
import sys
import time
from pathlib import Path

import google.generativeai as genai

REPO       = Path(__file__).resolve().parent.parent
KEY_PATH   = Path(r"C:\Users\User\AppData\Local\Temp\_gk.txt")
QUEUE_IN   = REPO / "docs" / "research" / "memoir_verify_queue.json"
TIMELINE   = REPO / "platform" / "data" / "memoir_timeline_verified.json"
RESULTS    = REPO / "docs" / "research" / "memoir_verify_gemini_results.json"

if not KEY_PATH.exists():
    print(f"[ERR] {KEY_PATH} missing", file=sys.stderr); sys.exit(1)

genai.configure(api_key=KEY_PATH.read_text(encoding="utf-8").strip())
model = genai.GenerativeModel("gemini-2.5-flash")

queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))["queued_events"]
timeline_doc = json.loads(TIMELINE.read_text(encoding="utf-8"))

PROMPT = """You are fact-checking a claim from a Holocaust-survivor memoir against the general historical record. Lusia (Leah) Rapaport née Weitzner survived Nazi-occupied Galicia (Nadwórna, Bolechów, Lwów). You are NOT verifying personal details about Lusia herself — only whether the claim is consistent with documented history of that time and place.

CLAIM TO ASSESS:
- Memoir page: {page}
- Date in memoir: {date}
- Title: {title}
- Description: {desc}

Reply ONLY with valid JSON in this exact shape (no markdown, no prose):
{{
  "category": "CORROBORATED" | "PLAUSIBLE" | "UNVERIFIABLE" | "CONTRADICTED",
  "reasoning": "<one or two sentences, your OWN words, max 40 words. Never quote sources verbatim>",
  "historical_context": "<one sentence of broader context if relevant, your own words, max 30 words. Empty string if none>"
}}

Category meanings:
- CORROBORATED: the claim names a well-documented event/person/place that aligns with history.
- PLAUSIBLE: the claim is consistent with what we know of that time/place but cannot be independently verified (most personal events).
- UNVERIFIABLE: insufficient public-record detail to assess.
- CONTRADICTED: the claim conflicts with documented history."""

results = []
print(f"[Gemini] verifying {len(queue)} events…")
for i, ev in enumerate(queue, 1):
    prompt = PROMPT.format(
        page=ev.get("event_page", "?"),
        date=ev.get("event_date") or "undated",
        title=ev.get("event_title", ""),
        desc=ev.get("event_description", "")[:600],
    )
    try:
        resp = model.generate_content(prompt, generation_config={"temperature": 0.2})
        raw = (resp.text or "").strip()
        if raw.startswith("```"):
            raw = raw.strip("`").lstrip("json").strip()
        parsed = json.loads(raw)
        category = parsed.get("category", "UNVERIFIABLE")
        reasoning = parsed.get("reasoning", "")
        context = parsed.get("historical_context", "")
    except Exception as e:
        category, reasoning, context = "ERROR", f"Gemini call failed: {e.__class__.__name__}", ""

    results.append({
        "event_page": ev.get("event_page"),
        "event_title": ev.get("event_title"),
        "event_date": ev.get("event_date"),
        "category": category,
        "reasoning": reasoning,
        "historical_context": context,
    })
    print(f"  [{i}/{len(queue)}] p.{ev.get('event_page')} — {category}")
    if i < len(queue):
        time.sleep(4)  # stay under 15 RPM

RESULTS.write_text(json.dumps({
    "model": "gemini-2.5-flash",
    "cost_usd": 0.0,
    "events_assessed": len(results),
    "results": results,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] Gemini results -> {RESULTS}")

# Merge back into memoir_timeline_verified.json
by_key = {(r["event_page"], r["event_title"]): r for r in results}
updated = 0
for ev in timeline_doc["events"]:
    k = (ev.get("page"), ev.get("title", ""))
    if k in by_key and ev.get("verification", {}).get("method") == "needs_lookup":
        r = by_key[k]
        ev["verification"]["method"] = "gemini_2.5_flash"
        ev["verification"]["verified"] = r["category"] in ("CORROBORATED", "PLAUSIBLE")
        ev["verification"]["confidence"] = r["category"].lower()
        ev["verification"]["side_note"] = r["reasoning"]
        ev["verification"]["historical_context"] = r["historical_context"]
        updated += 1

# Recompute cost summary
free_verified = sum(1 for e in timeline_doc["events"] if e["verification"]["verified"])
needs = sum(1 for e in timeline_doc["events"] if not e["verification"]["verified"])
timeline_doc["cost_summary"] = {
    "events_total": len(timeline_doc["events"]),
    "free_verified": free_verified,
    "need_further_check": needs,
    "method_breakdown": {
        m: sum(1 for e in timeline_doc["events"] if e["verification"]["method"] == m)
        for m in {e["verification"]["method"] for e in timeline_doc["events"]}
    },
    "total_cost_usd": 0.0,
}
TIMELINE.write_text(json.dumps(timeline_doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] enriched {updated} events -> {TIMELINE}")
print()
print(f"=== SUMMARY ===")
print(f"Verified (regex + gemini): {free_verified}/{len(timeline_doc['events'])}")
print(f"Still open: {needs}")
print(f"Cost: $0.00")
