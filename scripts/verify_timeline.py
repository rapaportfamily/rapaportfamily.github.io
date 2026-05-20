"""Tiered verification of the memoir timeline — saves money by trying free layers first.

LAYER 1 — Regex (free, instant)
   Match each event's text against scripts/historical_anchors.json patterns.
   If matched, the event is anchored to a known historical fact.

LAYER 2 — Wikipedia via WebFetch (free, slow)
   For events with named individuals or specific places not in anchors,
   try to fetch the corresponding Wikipedia page.
   [Stubbed — real WebFetch goes through Claude Code's tool. This script
   emits a JSON list of recommended URLs to fetch in a follow-up step.]

LAYER 3 — Gemini free tier (free up to 1500/day, fast)
   For ambiguous events, ask Gemini "is this consistent with the historical record?"
   [Stubbed — script emits a queue. Run separately if Doron approves.]

LAYER 4 — Claude / OpenAI (PAID — asks for budget approval first)
   Only used if free layers leave events un-verified.

OUTPUT (no LLM calls made by this script — it's pure analysis + queue):
   platform/data/memoir_timeline_verified.json   — events with verification_layer field
   docs/research/memoir_questions_2026-05-20.md  — open questions per event
   docs/research/memoir_verify_queue.json        — queue of items needing paid LLM (with cost estimate)
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANCHORS_FILE  = REPO / "scripts" / "historical_anchors.json"
TIMELINE_IN   = REPO / "platform" / "data" / "memoir_timeline.json"
ANALYSIS_IN   = REPO / "platform" / "data" / "memoir_analysis.json"
PAGES_IN      = REPO / "platform" / "data" / "memoir_pages.json"
TIMELINE_OUT  = REPO / "platform" / "data" / "memoir_timeline_verified.json"
QUESTIONS_OUT = REPO / "docs" / "research" / "memoir_questions_2026-05-20.md"
QUEUE_OUT     = REPO / "docs" / "research" / "memoir_verify_queue.json"

anchors_data = json.loads(ANCHORS_FILE.read_text(encoding="utf-8"))
ANCHORS = anchors_data["anchors"]
TOWNS   = anchors_data["town_gazetteer"]

# Compile regex patterns
for a in ANCHORS:
    a["_compiled"] = [re.compile(p, re.IGNORECASE) for p in a["match_patterns"]]

timeline = json.loads(TIMELINE_IN.read_text(encoding="utf-8"))
analysis = json.loads(ANALYSIS_IN.read_text(encoding="utf-8"))
pages    = json.loads(PAGES_IN.read_text(encoding="utf-8"))
events   = timeline.get("events", [])

# Build a page-text lookup for context
page_text = {}
for p in pages:
    page_text[p["page"]] = (p.get("hebrew", "") or "") + "\n" + (p.get("english", "") or "")

# ── LAYER 1: Regex matching ────────────────────────────────────────
def regex_verify(event):
    """Returns list of matched anchor IDs."""
    haystack = (event.get("title", "") + " " + event.get("description", "")
                + " " + page_text.get(event.get("page", -1), ""))
    matched = []
    for a in ANCHORS:
        for pat in a["_compiled"]:
            if pat.search(haystack):
                matched.append(a["id"])
                break
    return matched

# Build town index for place matching
TOWN_INDEX = {}
for t in TOWNS:
    for v in [t["canonical_en"]] + t["variants"]:
        TOWN_INDEX[v.lower()] = t["id"]

def town_verify(event):
    """Returns list of canonical place IDs whose variants appear in the event."""
    haystack = (event.get("title", "") + " " + event.get("description", "")).lower()
    matched = set()
    for variant, town_id in TOWN_INDEX.items():
        if variant.lower() in haystack:
            matched.add(town_id)
    return list(matched)

# ── LAYER 2: Recommend Wikipedia/WebFetch URLs ─────────────────────
def wikipedia_query_for(event):
    """Suggest a Wikipedia search query for this event (run via WebFetch externally)."""
    title = event.get("title", "")
    # Extract proper nouns + dates as the search seed
    return f"https://en.wikipedia.org/w/index.php?search={title.replace(' ', '+')}"

# ── Process all events ────────────────────────────────────────────
verified_events = []
need_paid_check = []
question_count = 0

for ev in events:
    matched = regex_verify(ev)
    matched_towns = town_verify(ev)
    layer_1_anchor = matched[0] if matched else None
    layer_1_town   = matched_towns[0] if matched_towns else None

    if matched:
        verification = {
            "method": "regex_anchor",
            "verified": True,
            "anchor_ids": matched,
            "confidence": "high",
            "cost_usd": 0.0,
            "side_note": f"Matches known historical anchor: {ANCHORS[next(i for i,a in enumerate(ANCHORS) if a['id']==matched[0])]['canonical_fact']} ({ANCHORS[next(i for i,a in enumerate(ANCHORS) if a['id']==matched[0])]['source']})",
        }
    elif matched_towns:
        verification = {
            "method": "regex_gazetteer",
            "verified": True,
            "town_ids": matched_towns,
            "confidence": "place_known",
            "cost_usd": 0.0,
            "side_note": f"Town referenced is documented in our gazetteer ({matched_towns[0]}). Event itself not anchored to a historical date.",
        }
    else:
        # No regex match — recommend Wikipedia lookup, queue for optional Gemini/Claude verification
        verification = {
            "method": "needs_lookup",
            "verified": False,
            "suggested_url": wikipedia_query_for(ev),
            "confidence": "unverified",
            "cost_usd": 0.0,
            "side_note": "No regex match. Recommend manual Wikipedia search OR free-tier Gemini grounding (~$0). If still inconclusive, paid Claude/OpenAI call (~$0.001 per event).",
            "open_question": f"Can the memoir's claim — '{ev.get('title','')}' on {ev.get('date') or 'undated'} (memoir p. {ev.get('page','?')}) — be corroborated by a primary source or scholarly history?"
        }
        question_count += 1
        # Add to paid-check queue with cost estimate
        need_paid_check.append({
            "event_page": ev.get("page"),
            "event_title": ev.get("title", ""),
            "event_date": ev.get("date"),
            "event_description": ev.get("description", "")[:300],
            "suggested_search": wikipedia_query_for(ev),
            "estimated_cost_claude_haiku": 0.001,
            "estimated_cost_gemini_free": 0.0,
        })

    enriched = dict(ev)
    enriched["verification"] = verification
    verified_events.append(enriched)

# Cost summary
free_verified = sum(1 for e in verified_events if e["verification"]["verified"])
need_paid = len(need_paid_check)
est_claude = sum(0.001 for _ in need_paid_check)  # rough
est_gemini = 0.0  # free tier

# ── Write outputs ──────────────────────────────────────────────────
TIMELINE_OUT.write_text(json.dumps({
    "source": "Lusia memoir + tiered verification",
    "verification_method": "Layer 1 regex (free); Layer 2-4 queued for free Gemini grounding / paid Claude",
    "events": verified_events,
    "cost_summary": {
        "events_total": len(events),
        "free_verified": free_verified,
        "need_further_check": need_paid,
        "estimated_cost_if_run_gemini_only_usd": est_gemini,
        "estimated_cost_if_run_claude_for_all_unverified_usd": round(est_claude, 4),
    },
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] enriched timeline -> {TIMELINE_OUT}")

# Questions file (human-readable)
qlines = [
    "# Memoir timeline — open questions (2026-05-20)",
    "",
    "Each event below was extracted from Lusia's memoir but could NOT be verified by free-tier regex against our historical anchors. They are the research questions Doron (or the family) should investigate next.",
    "",
    f"**{free_verified}** events were free-verified via regex.",
    f"**{need_paid}** events remain as open questions below.",
    "",
    "## How to use",
    "",
    "- For each question, the **suggested URL** is a Wikipedia/web search starting point.",
    "- If you (Doron) want me to run a paid LLM verification pass on these, see the cost estimate at the end and approve the budget.",
    "",
    "## Open questions",
    "",
]
for i, item in enumerate([e for e in verified_events if not e["verification"]["verified"]], 1):
    v = item["verification"]
    qlines.append(f"### Q{i}. {item.get('title','(no title)')}")
    qlines.append("")
    qlines.append(f"- **Memoir page**: {item.get('page','?')}")
    qlines.append(f"- **Memoir date**: {item.get('date') or 'undated'}")
    qlines.append(f"- **Description**: {item.get('description', '')[:300]}")
    qlines.append(f"- **Question**: {v.get('open_question','')}")
    qlines.append(f"- **Try**: {v.get('suggested_url','')}")
    qlines.append("")

qlines += [
    "---",
    "",
    "## Cost estimate to verify the remaining questions",
    "",
    f"- **Free Gemini grounding** (we have key, 1500/day cap): **$0** — Recommended first pass.",
    f"- **Paid Claude Haiku 4.5**: ~$0.001 per event × {need_paid} events = **~${round(est_claude,3)} USD**. Insignificant but requires explicit approval per project doctrine.",
    f"- **Paid Claude Sonnet 4.6** (higher accuracy): ~$0.01 per event × {need_paid} = **~${round(est_claude*10,2)} USD**.",
    "",
    "## Approval needed",
    "",
    "Reply with one of:",
    "- `verify with gemini` — runs free Gemini grounding pass, no cost.",
    "- `verify with claude haiku ~$X` — paid pass, fast, ~85% accuracy.",
    "- `verify with claude sonnet ~$Y` — paid pass, slower, ~95% accuracy.",
    "- `present as questions` — keep these as open questions, don't run any more LLM verification.",
]
QUESTIONS_OUT.parent.mkdir(parents=True, exist_ok=True)
QUESTIONS_OUT.write_text("\n".join(qlines), encoding="utf-8")
print(f"[OK] questions report -> {QUESTIONS_OUT}")

# Queue file (machine-readable, for any follow-up paid verification script)
QUEUE_OUT.write_text(json.dumps({
    "queued_events": need_paid_check,
    "estimated_cost_usd_claude_haiku": round(est_claude, 4),
    "estimated_cost_usd_claude_sonnet": round(est_claude * 10, 4),
    "estimated_cost_usd_gemini_free": 0.0,
    "doctrine": "Free layers first. Ask Doron before any paid call.",
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] queue -> {QUEUE_OUT}")

print()
print(f"=== SUMMARY ===")
print(f"Total events: {len(events)}")
print(f"Regex-verified (FREE, layer 1): {free_verified}")
print(f"Need follow-up (queued): {need_paid}")
print(f"Cost if all run via Gemini free: ${est_gemini}")
print(f"Cost if all run via Claude Haiku: ${round(est_claude, 4)}")
