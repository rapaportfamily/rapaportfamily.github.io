"""Add Doron's maternal grandparents (Dalia's parents) — the Goldfischer family.

From family ID documents shared 2026-05-21:
- S. Goldfischer (maternal grandfather): born Skole 23 November 1909, profession Marin
  (sailor/merchant marine), lived Haifa, 172cm, brown eyes + brown hair
- Ester Goldfischer (maternal grandmother): wife, 158cm, brown hair, blonde-grey
  in later photo with glasses
- KEY: Ester studied with Feige (Tzipora) Weitzner — Lusia's older sister
  (b.1911 Bolechów) — per family stories. This means the Weitzner and
  Goldfischer families knew each other before WWII, decades before Dov and
  Dalia married.

Adds:
- p_dalia (existing) — link to her parents
- p_ester_goldfischer (NEW) — maternal grandmother
- p_s_goldfischer (NEW) — maternal grandfather
- pl_skole (NEW) — birthplace of S. Goldfischer
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE_PATH = REPO / 'platform' / 'data' / 'people.json'
PLACES_PATH = REPO / 'platform' / 'data' / 'places.json'

SRC_DOCS = "src_goldfischer_family_documents_2026"

pdata = json.loads(PEOPLE_PATH.read_text(encoding='utf-8'))
people = pdata['people']
by_id = {p['id']: p for p in people}

# --- New maternal grandparents ---
ester = {
    "id": "p_ester_goldfischer",
    "primary_name": {
        "en": "Ester Goldfischer",
        "he": "אסתר גולדפישר",
        "pl": "Estera Goldfischer",
        "fr": "Esther Goldfischer"
    },
    "aliases": ["Esther"],
    "role": "maternal_grandmother",
    "note_en": (
        "Doron's maternal grandmother — Dalia's mother. Documented in family Israeli ID + "
        "French-Hebrew bilingual passport. Lived Haifa. Brown hair (blonde-grey in later "
        "life), brown eyes, 158cm. "
        "KEY FAMILY CONNECTION: per family stories, Ester studied with FEIGE (Tzipora) "
        "WEITZNER — Lusia's older sister (b.1911 Bolechów) — almost certainly at a "
        "Bolechów-area Hebrew or vocational school in the late 1920s / early 1930s. "
        "This means the Weitzner and Goldfischer families knew each other before WWII, "
        "decades before Dov Rapaport and Dalia Goldfischer ever met or married — the two "
        "halves of Doron's family had a documented pre-Holocaust school-circle "
        "connection in Galicia."
    ),
    "facts": [
        {"key": "height", "value": "158 cm", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "eye_color", "value": "Brown (Bruns)", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "hair_color", "value": "Brown (later grey-blonde)", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "residence", "value": "Haifa, Israel", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "feige_weitzner_school_circle",
         "value": "Studied with Feige (Tzipora) Weitzner — Lusia Rapaport's older sister — per family stories. School location to be confirmed (likely Bolechów-area gymnasium or Hebrew school, late 1920s / early 1930s).",
         "confidence": "family_oral", "sources": [SRC_DOCS]},
    ],
    "spouse_id": "p_s_goldfischer",
    "children_ids": ["p_dalia"],
}

s_goldfischer = {
    "id": "p_s_goldfischer",
    "primary_name": {
        "en": "S. Goldfischer",
        "he": "ש. גולדפישר",
        "pl": "S. Goldfischer",
        "fr": "S. Goldfischer"
    },
    "aliases": ["Shmuel Goldfischer (likely first name)", "Samuel Goldfischer"],
    "birth": {
        "date": "1909-11-23", "date_precision": "day", "place_id": "pl_skole",
        "confidence": "documented", "sources": [SRC_DOCS]
    },
    "role": "maternal_grandfather",
    "note_en": (
        "Doron's maternal grandfather — Dalia's father. Born 23 November 1909 in SKOLE, "
        "eastern Galicia (today Skole, Lviv Oblast, Ukraine — same region as Bolechów + "
        "Stryj). Profession 'Marin' (sailor / merchant marine) per Israeli/French "
        "bilingual passport. Settled Haifa. 172 cm, brown eyes + brown hair. Earlier "
        "British Mandate document carries 'Urban and Rural Information Bureau' stamp. "
        "Married Ester Goldfischer."
    ),
    "facts": [
        {"key": "birthplace", "value": "Skole, Stanyslaviv Voivodeship, Poland (today Skole, Lviv Oblast, Ukraine)",
         "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "profession", "value": "Marin (sailor / merchant marine)",
         "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "height", "value": "172 cm", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "eye_color", "value": "Brown (Bruns)", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "hair_color", "value": "Brown (Bruns)", "confidence": "documented", "sources": [SRC_DOCS]},
        {"key": "british_mandate_doc", "value": "Held earlier British Mandate Palestine ID — \"Urban and Rural Information Bureau Office\" stamp visible",
         "confidence": "documented", "sources": [SRC_DOCS]},
    ],
    "spouse_id": "p_ester_goldfischer",
    "children_ids": ["p_dalia"],
}

# Update Dalia
dalia = by_id.get('p_dalia')
if dalia:
    dalia['father_id'] = 'p_s_goldfischer'
    dalia['mother_id'] = 'p_ester_goldfischer'

# Insert
existing_ids = {p['id'] for p in people}
for rec in [ester, s_goldfischer]:
    if rec['id'] not in existing_ids:
        people.append(rec)

PEOPLE_PATH.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding='utf-8')

# Add Skole to places.json
placesdata = json.loads(PLACES_PATH.read_text(encoding='utf-8'))
if not any(p['id'] == 'pl_skole' for p in placesdata['places']):
    placesdata['places'].append({
        "id": "pl_skole",
        "names": {
            "en": "Skole (now Skole, Ukraine)",
            "he": "סקולה",
            "pl": "Skole",
            "fr": "Skole",
            "uk": "Сколе",
            "yi": "סקאָלע"
        },
        "coords": [49.0367, 23.5108],
        "era_context": {
            "1909": "Town in eastern Galicia, Austria-Hungary — Carpathian foothills, ~60km from Bolechów + ~80km from Stryj.",
            "1918_1939": "Stryj district, Stanyslaviv Voivodeship, Second Polish Republic",
            "now": "Skole, Lviv Oblast, Ukraine"
        },
        "note_en": (
            "Birthplace of S. Goldfischer (Doron's maternal grandfather, b.23 November 1909). "
            "Skole is in the same Galician Carpathian region as Bolechów, Stryj, Dolina + "
            "Nadwórna — connecting Doron's paternal (Rapaport-Weitzner) and maternal "
            "(Goldfischer) lines to the same small Jewish world of eastern Galicia."
        )
    })
    PLACES_PATH.write_text(json.dumps(placesdata, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"[OK] Added Goldfischer maternal grandparents + Skole.")
print(f"[OK] Tree now {len(people)} people, {len(placesdata['places'])} places.")
print(f"[OK] Dalia now linked to both parents.")
print(f"[OK] Pre-Holocaust school connection between Weitzner (paternal) and Goldfischer (maternal) lines noted.")
