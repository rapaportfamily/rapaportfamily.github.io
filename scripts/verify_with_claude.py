"""Layer 4 verification — Claude Sonnet 4.6, batched.

Doron approved the budget (~$0.35 for all 35 events). Single batch call:
sends all events at once, gets verdicts back in one JSON object.

Reads:  docs/research/memoir_verify_queue.json
Writes: docs/research/memoir_verify_claude_results.json
        platform/data/memoir_timeline_verified.json (updated in place)
"""
import json
import sys
from pathlib import Path

import anthropic

REPO     = Path(__file__).resolve().parent.parent
KEY_PATH = Path(r"C:\Users\User\AppData\Local\Temp\_ak.txt")
QUEUE_IN = REPO / "docs" / "research" / "memoir_verify_queue.json"
TIMELINE = REPO / "platform" / "data" / "memoir_timeline_verified.json"
RESULTS  = REPO / "docs" / "research" / "memoir_verify_claude_results.json"

client = anthropic.Anthropic(api_key=KEY_PATH.read_text(encoding="utf-8").strip())
MODEL  = "claude-sonnet-4-5-20250929"  # Sonnet 4.5/4.6 family

queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))["queued_events"]

event_list = []
for i, ev in enumerate(queue):
    event_list.append({
        "i": i,
        "page": ev.get("event_page"),
        "date": ev.get("event_date"),
        "title": ev.get("event_title", ""),
        "desc": (ev.get("event_description") or "")[:500],
    })

SYSTEM = """You are a careful historian fact-checking claims from a Holocaust-survivor memoir against the documented historical record.

The memoir is by Lusia (Leah) Rapaport née Weitzner, born in Nadwórna (Galicia, then Poland, now Ukraine), survived Nazi occupation, escaped to Brussels in 1946, settled in Israel. Her family helpers included documented Gentile rescuers (Pietrozycki, Ivanov, Hormak family, Maria Ciccelik).

You are NOT verifying intimate personal details about Lusia herself. You ARE assessing whether each claim is consistent with documented history of that time, place, and political context.

For each event return EXACTLY ONE of these categories:
- CORROBORATED — claim names a well-documented event/person/place that aligns with established history (e.g., Operation Barbarossa, Nadwórna ghetto liquidation, Cyprus detention camps).
- PLAUSIBLE — consistent with what we know of that time/place/community but is a personal/family detail not independently verifiable in public sources. (Most memoir events.)
- UNVERIFIABLE — insufficient public-record detail to assess.
- CONTRADICTED — conflicts with documented history. Use sparingly and only with high confidence.

Reasoning must be IN YOUR OWN WORDS, 1-2 sentences, max 50 words. NEVER quote sources verbatim. Include a brief historical_context (max 30 words) where it adds value."""

USER = """Assess the following claims. Reply ONLY with valid JSON in this exact shape (no markdown, no prose, no code fences):

{"verdicts": [{"i": 0, "category": "...", "reasoning": "...", "historical_context": "..."}, ...]}

Include ALL """ + str(len(queue)) + """ verdicts.

CLAIMS:
""" + json.dumps(event_list, ensure_ascii=False, indent=2)

print(f"[Claude {MODEL}] batch-verifying {len(queue)} events…")
resp = client.messages.create(
    model=MODEL,
    max_tokens=16000,
    system=SYSTEM,
    messages=[{"role": "user", "content": USER}],
)

raw = resp.content[0].text.strip()
if raw.startswith("```"):
    raw = raw.strip("`")
    if raw.lower().startswith("json"):
        raw = raw[4:].strip()

try:
    parsed = json.loads(raw)
    verdicts = parsed.get("verdicts", [])
except json.JSONDecodeError as e:
    print(f"[ERR] couldn't parse JSON: {e}", file=sys.stderr)
    print("=== raw response (first 3000) ===", file=sys.stderr)
    print(raw[:3000], file=sys.stderr)
    sys.exit(1)

# Track usage / cost
usage = resp.usage
input_tokens = getattr(usage, "input_tokens", 0)
output_tokens = getattr(usage, "output_tokens", 0)
# Sonnet 4.5 pricing: $3/MTok input, $15/MTok output
cost = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0
print(f"[usage] input={input_tokens} tok, output={output_tokens} tok, cost=${cost:.4f}")
print(f"[Claude] got {len(verdicts)} verdicts")

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
    "model": MODEL,
    "cost_usd": round(cost, 4),
    "input_tokens": input_tokens,
    "output_tokens": output_tokens,
    "events_assessed": len(results),
    "results": results,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] Claude results -> {RESULTS}")

# Merge back into timeline
timeline_doc = json.loads(TIMELINE.read_text(encoding="utf-8"))
by_key = {(r["event_page"], r["event_title"]): r for r in results}
updated = 0
for ev in timeline_doc["events"]:
    k = (ev.get("page"), ev.get("title", ""))
    if k in by_key:
        r = by_key[k]
        ev["verification"]["method"] = "claude_sonnet_4_5"
        ev["verification"]["verified"] = r["category"] in ("CORROBORATED", "PLAUSIBLE")
        ev["verification"]["confidence"] = r["category"].lower()
        ev["verification"]["side_note"] = r["reasoning"]
        ev["verification"]["historical_context"] = r["historical_context"]
        ev["verification"]["cost_usd"] = round(cost / len(results), 6) if results else 0
        ev["verification"].pop("open_question", None)
        ev["verification"].pop("suggested_url", None)
        updated += 1

verified_n = sum(1 for e in timeline_doc["events"] if e["verification"]["verified"])
needs = sum(1 for e in timeline_doc["events"] if not e["verification"]["verified"])
method_breakdown = {}
category_breakdown = {}
for e in timeline_doc["events"]:
    m = e["verification"]["method"]
    method_breakdown[m] = method_breakdown.get(m, 0) + 1
    c = e["verification"].get("confidence", "unknown")
    category_breakdown[c] = category_breakdown.get(c, 0) + 1

timeline_doc["cost_summary"] = {
    "events_total": len(timeline_doc["events"]),
    "verified": verified_n,
    "needs_followup": needs,
    "method_breakdown": method_breakdown,
    "category_breakdown": category_breakdown,
    "total_cost_usd": round(cost, 4),
    "model_paid": MODEL,
}
TIMELINE.write_text(json.dumps(timeline_doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] enriched {updated} events -> {TIMELINE}")
print()
print(f"=== SUMMARY ===")
print(f"Verified: {verified_n}/{len(timeline_doc['events'])}")
print(f"Still open: {needs}")
print(f"Method breakdown: {method_breakdown}")
print(f"Category breakdown: {category_breakdown}")
print(f"Total cost: ${cost:.4f}")
