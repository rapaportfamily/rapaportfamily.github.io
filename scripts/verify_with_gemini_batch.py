"""Layer 2 verification (batched) — single Gemini call for all 35 queued events.

Free-tier friendly: 1 request total instead of 35.
"""
import json
import sys
from pathlib import Path

import google.generativeai as genai

REPO       = Path(__file__).resolve().parent.parent
KEY_PATH   = Path(r"C:\Users\User\AppData\Local\Temp\_gk.txt")
QUEUE_IN   = REPO / "docs" / "research" / "memoir_verify_queue.json"
TIMELINE   = REPO / "platform" / "data" / "memoir_timeline_verified.json"
RESULTS    = REPO / "docs" / "research" / "memoir_verify_gemini_results.json"

genai.configure(api_key=KEY_PATH.read_text(encoding="utf-8").strip())
# Use a model with generous free quota
model = genai.GenerativeModel("gemini-2.0-flash")

queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))["queued_events"]

# Compact event list for the prompt
event_list = []
for i, ev in enumerate(queue):
    event_list.append({
        "i": i,
        "page": ev.get("event_page"),
        "date": ev.get("event_date"),
        "title": ev.get("event_title", ""),
        "desc": (ev.get("event_description") or "")[:400],
    })

PROMPT = """You are fact-checking claims from a Holocaust-survivor memoir against the general historical record. Lusia (Leah) Rapaport née Weitzner survived Nazi-occupied Galicia (Nadwórna, Bolechów, Lwów). You are NOT verifying personal details about Lusia herself — only whether each claim is consistent with documented history of that time and place.

CLAIMS (each indexed by `i`):
""" + json.dumps(event_list, ensure_ascii=False, indent=2) + """

Reply ONLY with valid JSON (no markdown fences). A JSON object:
{
  "verdicts": [
    {"i": 0, "category": "...", "reasoning": "...", "historical_context": "..."},
    {"i": 1, ...},
    ...
  ]
}

For each event, fill in:
- category: one of CORROBORATED | PLAUSIBLE | UNVERIFIABLE | CONTRADICTED
- reasoning: 1–2 sentences in your OWN words, max 40 words. NEVER quote sources verbatim.
- historical_context: 1 sentence, max 30 words, your own words. Empty string if none.

Category meanings:
- CORROBORATED: claim names a well-documented event/person/place that aligns with history.
- PLAUSIBLE: consistent with what we know of that time/place but not independently verifiable (most personal events).
- UNVERIFIABLE: insufficient public-record detail.
- CONTRADICTED: conflicts with documented history.

Include ALL """ + str(len(queue)) + """ verdicts. Do not skip any."""

print(f"[Gemini] batch-verifying {len(queue)} events in one call…")
resp = model.generate_content(PROMPT, generation_config={"temperature": 0.2, "max_output_tokens": 8192})
raw = (resp.text or "").strip()
if raw.startswith("```"):
    raw = raw.strip("`")
    if raw.lower().startswith("json"):
        raw = raw[4:].strip()

try:
    parsed = json.loads(raw)
    verdicts = parsed.get("verdicts", [])
except json.JSONDecodeError as e:
    print(f"[ERR] couldn't parse JSON: {e}", file=sys.stderr)
    print("=== raw response ===", file=sys.stderr)
    print(raw[:2000], file=sys.stderr)
    sys.exit(1)

print(f"[Gemini] got {len(verdicts)} verdicts back")

# Map back to original events
results = []
for v in verdicts:
    idx = v.get("i")
    if idx is None or idx >= len(queue):
        continue
    ev = queue[idx]
    results.append({
        "event_page": ev.get("event_page"),
        "event_title": ev.get("event_title"),
        "event_date": ev.get("event_date"),
        "category": v.get("category", "UNVERIFIABLE"),
        "reasoning": v.get("reasoning", ""),
        "historical_context": v.get("historical_context", ""),
    })

RESULTS.write_text(json.dumps({
    "model": "gemini-2.0-flash",
    "cost_usd": 0.0,
    "events_assessed": len(results),
    "results": results,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] Gemini results -> {RESULTS}")

# Merge back
timeline_doc = json.loads(TIMELINE.read_text(encoding="utf-8"))
by_key = {(r["event_page"], r["event_title"]): r for r in results}
updated = 0
for ev in timeline_doc["events"]:
    k = (ev.get("page"), ev.get("title", ""))
    if k in by_key:
        r = by_key[k]
        # Reset whatever was in there from the failed earlier pass
        ev["verification"]["method"] = "gemini_2.0_flash"
        ev["verification"]["verified"] = r["category"] in ("CORROBORATED", "PLAUSIBLE")
        ev["verification"]["confidence"] = r["category"].lower()
        ev["verification"]["side_note"] = r["reasoning"]
        ev["verification"]["historical_context"] = r["historical_context"]
        ev["verification"]["cost_usd"] = 0.0
        # Drop the stale "needs_lookup" fields if present
        ev["verification"].pop("open_question", None)
        ev["verification"].pop("suggested_url", None)
        updated += 1

# Cost summary
free_verified = sum(1 for e in timeline_doc["events"] if e["verification"]["verified"])
needs = sum(1 for e in timeline_doc["events"] if not e["verification"]["verified"])
method_breakdown = {}
for e in timeline_doc["events"]:
    m = e["verification"]["method"]
    method_breakdown[m] = method_breakdown.get(m, 0) + 1
timeline_doc["cost_summary"] = {
    "events_total": len(timeline_doc["events"]),
    "verified": free_verified,
    "needs_followup": needs,
    "method_breakdown": method_breakdown,
    "total_cost_usd": 0.0,
}
TIMELINE.write_text(json.dumps(timeline_doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] enriched {updated} events -> {TIMELINE}")
print()
print(f"=== SUMMARY ===")
print(f"Verified (regex + gemini): {free_verified}/{len(timeline_doc['events'])}")
print(f"Still open: {needs}")
print(f"Method breakdown: {method_breakdown}")
print(f"Cost: $0.00")
