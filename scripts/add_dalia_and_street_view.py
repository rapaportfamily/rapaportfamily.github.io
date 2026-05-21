"""1) Add Dalia to all attribution phrases:
     'Dana, Doron and Daniel' --> 'Dalia, Dana, Doron and Daniel'
   (per Dov 21 May 2026 — mother Dalia is an equal partner with her children)

2) Add a Google Maps Street View embed (no API key) to every Virtual Trip
   card so the user can see the CURRENT looks of each address inline.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / 'platform' / 'data'

# --- 1) Add Dalia to attribution phrases ---
REPLACEMENTS = [
    # Possessive: "Dana, Doron and Daniel's" -> "Dalia, Dana, Doron and Daniel's"
    # Multi-language. Match only the partner-list form (not other lists).
    (r"Dana, Doron and Daniel's", "Dalia, Dana, Doron and Daniel's"),
    (r"\bDana, Doron and Daniel(?!')", "Dalia, Dana, Doron and Daniel"),
    # Hebrew
    (r"דנה, דורון ודניאל", "דליה, דנה, דורון ודניאל"),
    # Polish
    (r"\bDanę, Dorona i Daniela", "Dalię, Danę, Dorona i Daniela"),
    (r"\bDana, Doron i Daniel(?!a)", "Dalia, Dana, Doron i Daniel"),
    # French
    (r"\bDana, Doron et Daniel", "Dalia, Dana, Doron et Daniel"),
]

TARGETS = [
    DATA / 'events.json', DATA / 'people.json', DATA / 'places.json',
    DATA / 'documents.json', DATA / 'hypotheses.json',
    DATA / 'research_center.json', DATA / 'ancestry.json',
    DATA / 'i18n' / 'en.json', DATA / 'i18n' / 'he.json',
    DATA / 'i18n' / 'pl.json', DATA / 'i18n' / 'fr.json',
]

def walk_strings(obj, fn):
    if isinstance(obj, dict):
        return {k: walk_strings(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_strings(x, fn) for x in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj

changes = {}
def apply_repl(s):
    new_s = s
    for pat, repl in REPLACEMENTS:
        new_s = re.sub(pat, repl, new_s)
    if new_s != s:
        changes[current] = changes.get(current, 0) + 1
    return new_s

for path in TARGETS:
    if not path.exists(): continue
    current = path.name
    data = json.loads(path.read_text(encoding='utf-8'))
    data = walk_strings(data, apply_repl)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

print("=== Dalia added to attribution ===")
for f, n in changes.items():
    print(f"  {f:30} {n} string(s)")
if not changes:
    print("  (no matches — already updated)")

# --- 2) Add Google Maps Street View embed (no API key) to every Trip card ---
RC = DATA / 'research_center.json'
rc = json.loads(RC.read_text(encoding='utf-8'))
trip = next(s for s in rc['sections'] if s['id'] == 'virtual_trip')

added_sv = 0
for card in trip['cards']:
    mp = card.get('map')
    if not mp or not mp.get('coords'):
        continue
    lat, lng = mp['coords']
    # The "&output=embed" + "&layer=c&cbll=" trick opens Google Maps with Street
    # View overlay enabled at the given coordinates, no API key required.
    # Falls back to satellite/map view if no Street View imagery available.
    mp['google_embed'] = (
        f"https://maps.google.com/maps?q={lat},{lng}"
        f"&t=k&z=18&ie=UTF8&iwloc=&output=embed"
    )
    mp['google_streetview_embed'] = (
        f"https://maps.google.com/maps?q=&layer=c&cbll={lat},{lng}"
        f"&cbp=11,0,0,0,0&output=embed"
    )
    added_sv += 1

rc['build_version'] = "2026-05-21-T9-dalia-streetview-embed"
RC.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"\n=== Street View embeds added ===")
print(f"  Added Google Maps + Street View embeds to {added_sv}/{len(trip['cards'])} Trip cards.")
