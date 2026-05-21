"""Add the additional living cousins discovered in round 2 + correct Edward Gelles."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
REPO = Path(__file__).resolve().parent.parent

d = json.loads((REPO / 'platform' / 'data' / 'people.json').read_text(encoding='utf-8'))
people = d['people']
by_id = {p['id']: p for p in people}

# CORRECT Edward Gelles: ALIVE, 98, London (not deceased 2023 as previously)
gelles = by_id['p_edward_gelles_cousin']
gelles['birth'] = {
    "date": "1927-11-24", "date_precision": "day", "place_id": "pl_vienna",
    "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]
}
gelles['death'] = None
gelles['role'] = 'living_cousin'
gelles['note_en'] = (
    "LIVING — age 98, London. 2nd cousin once removed of David Memek Rapaport. Born Vienna 24 November 1927. "
    "Published genealogist whose work at Balliol College Oxford documents the entire Griffel-Chajes-Wahl-Gelles "
    "dynasty of Galicia. Authored 'An Ancient Lineage: European Roots of a Jewish Family' (Vallentine Mitchell, 2006). "
    "His mother Regina Gelles née Griffel (1900-1954) was David Memek's first cousin. "
    "Senior living expert on our maternal line — knows everyone, holds Reb Eliezer's archive notes. "
    "Contact via Balliol Modern Papers archivist: archivist@balliol.ox.ac.uk"
)
gelles['facts'] = [
    {"key": "contact", "value": "archivist@balliol.ox.ac.uk (Balliol Modern Papers will forward)",
     "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]},
    {"key": "books", "value": "An Ancient Lineage: European Roots of a Jewish Family (Vallentine Mitchell, 2006); 50+ research papers at Balliol archives",
     "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]},
]

NEW = [
    {
        "id": "p_tali_griffel_ginsburg",
        "primary_name": {"en": "Tali Griffel Ginsburg", "he": "טלי גריפל גינסבורג",
                          "pl": "Tali Griffel Ginsburg", "fr": "Tali Griffel Ginsburg"},
        "role": "living_cousin",
        "note_en": (
            "LIVING — NYC. 3rd cousin of David Memek Rapaport. Daughter of Andrew Griffel. "
            "Survivor of the Ras Burqa terror attack 5 October 1985 in Sinai — her mother "
            "Anita Spindel Griffel was murdered shielding 5-year-old Tali with her body. Andrew "
            "raised her in NYC. Now married, mother. Contributor to Tablet Magazine + Israel Story podcast."
        ),
        "father_id": "p_andrew_griffel_living",
        "facts": [
            {"key": "contact", "value": "Tablet Magazine; Israel Story podcast; Instagram @ourfamilybikes",
             "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]},
        ],
        "aliases": ["Tali Griffel", "Tali Ginsburg"],
    },
    {
        "id": "p_joseph_griffel_living",
        "primary_name": {"en": "Joseph Griffel", "he": "יוסף גריפל",
                          "pl": "Joseph Griffel", "fr": "Joseph Griffel"},
        "role": "living_cousin",
        "birth": {"date": "1953", "date_precision": "year", "confidence": "documented",
                  "sources": ["src_gelles_griffel_nadworna_pdf"]},
        "note_en": (
            "LIVING — only surviving child of Dr Jacob Griffel (1900-1962, the Vaad ha-Hatzala Istanbul "
            "rescuer). Jacob's first wife and children perished in the Warsaw blitzkrieg; Joseph from "
            "Jacob's second marriage to Miriam Rottenberg (1914-1998). 2nd cousin once removed of David Memek."
        ),
        "father_id": "p_dr_jacob_griffel",
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_sarah_nir_living",
        "primary_name": {"en": "Sarah Maslin Nir", "he": "שרה מסלין ניר",
                          "pl": "Sarah Maslin Nir", "fr": "Sarah Maslin Nir"},
        "role": "living_cousin",
        "note_en": (
            "LIVING — NYC. New York Times staff reporter (long-form features, equestrian, real estate). "
            "Daughter of Yehuda Nir + Bonnie Maslin. 2nd cousin once removed of David Memek."
        ),
        "facts": [
            {"key": "contact", "value": "https://www.nytimes.com/by/sarah-maslin-nir",
             "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]},
        ],
        "aliases": [],
    },
    {
        "id": "p_david_nir_living",
        "primary_name": {"en": "David Nir", "he": "דוד ניר",
                          "pl": "David Nir", "fr": "David Nir"},
        "role": "living_cousin",
        "note_en": (
            "LIVING — NYC. Political Director of Daily Kos. Son of Yehuda Nir + Bonnie Maslin. "
            "2nd cousin once removed of David Memek. Contact: davidnir@dailykos.com / @DavidNir on Twitter."
        ),
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_daniel_nir_living",
        "primary_name": {"en": "Daniel Nir", "he": "דניאל ניר",
                          "pl": "Daniel Nir", "fr": "Daniel Nir"},
        "role": "living_cousin",
        "note_en": (
            "LIVING — NYC. Private investor. Son of Yehuda Nir (first marriage). "
            "2nd cousin once removed of David Memek."
        ),
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_aaron_nir_living",
        "primary_name": {"en": "Aaron Nir", "he": "אהרן ניר",
                          "pl": "Aaron Nir", "fr": "Aaron Nir"},
        "role": "living_cousin",
        "note_en": (
            "LIVING — NYC. Fashion executive. Son of Yehuda Nir (first marriage). "
            "2nd cousin once removed of David Memek."
        ),
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_bonnie_maslin_living",
        "primary_name": {"en": "Bonnie Maslin", "he": "בוני מסלין",
                          "pl": "Bonnie Maslin", "fr": "Bonnie Maslin"},
        "role": "living_cousin_in_law",
        "note_en": (
            "LIVING — NYC. Widow of Yehuda Nir (d.2014). Psychiatrist/author (books on relationships). "
            "Likely warmest first-contact point for reaching the four Nir children."
        ),
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_jackie_griffel_living",
        "primary_name": {"en": "Jackie Boehme Griffel", "he": "ג'קי גריפל",
                          "pl": "Jackie Griffel", "fr": "Jackie Griffel"},
        "role": "living_cousin_in_law",
        "note_en": (
            "LIVING — Rockville MD area. Widow of Eric Griffel (1930-2020, Edward Gelles's first cousin, "
            "USAID Pakistan Station Chief who signed the Blood Telegram). Contact via USAID Alumni Association."
        ),
        "aliases": [],
        "facts": [],
    },
    {
        "id": "p_diana_griffel_living",
        "primary_name": {"en": "Diana Margaret Griffel", "he": "דיאנה גריפל",
                          "pl": "Diana Griffel", "fr": "Diana Griffel"},
        "birth": {"date": "1943-10-27", "date_precision": "day", "place_id": "pl_london",
                  "confidence": "documented", "sources": ["src_gelles_griffel_nadworna_pdf"]},
        "role": "living_cousin",
        "note_en": (
            "Born London 27 Oct 1943. Daughter of Edward Griffel (uncle of David Memek) + Susan Manson. "
            "Status uncertain — would be 82. 2nd cousin of David Memek. Worth a targeted search."
        ),
        "father_id": "p_edward_griffel_uncle",
        "aliases": [],
        "facts": [],
    },
]

existing_ids = {p['id'] for p in people}
added = 0
for n in NEW:
    if n['id'] in existing_ids:
        continue
    people.append(n)
    added += 1

# Andrew → Tali link
andrew = by_id['p_andrew_griffel_living']
andrew['children_ids'] = ['p_tali_griffel_ginsburg']

# Add London place
places = json.loads((REPO / 'platform' / 'data' / 'places.json').read_text(encoding='utf-8'))
if not any(p['id'] == 'pl_london' for p in places['places']):
    places['places'].append({
        "id": "pl_london",
        "names": {"en": "London", "he": "לונדון", "pl": "Londyn", "fr": "Londres"},
        "coords": [51.5074, -0.1278],
        "era_context": {"now": "Capital of the United Kingdom"},
        "note_en": "Home of cousin Edward Gelles (b.1927), the published genealogist of our maternal Griffel-Nadwórna dynasty."
    })
    (REPO / 'platform' / 'data' / 'places.json').write_text(json.dumps(places, ensure_ascii=False, indent=2), encoding='utf-8')

(REPO / 'platform' / 'data' / 'people.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Added {added} new living cousins. Total people now: {len(people)}.")
print("Edward Gelles status corrected: LIVING, 98, London.")
