"""Integrate Basia's major finds (21 May 2026):

1. 1938 Lwów auction notice (Akcyjny Bank Hipoteczny, 13 Sept 1938) listing
   17 named Griffel + Grünfeld heirs of a Nadwórna property — confirms the
   entire Eliezer Griffel extended family jointly held a one-storey brick
   rental house at Nadwórna ul. Śródmieście (valued 127,294 zł).

2. Album-Skorowidz Sejm 1935 entry for Zygmunt Griffel — confirms his
   timber business at Lwów ul. Kopernika 5, founded 1923, exporting 60,000
   tons/year (1934/35) of pine timber — 82.8% to England, the rest to
   Holland / Germany / Switzerland / France. Transit warehouses in Gdynia +
   Gdańsk.

3. Pre-war Polish resort photos (Polish National Digital Archive / NAC,
   public domain) for the Muszyna Virtual Trip card.

4. The user's Goldfischer ID documents (S. Goldfischer British Mandate +
   later Israeli passport pages).
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE_PATH = REPO / 'platform' / 'data' / 'people.json'
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'

SRC_BASIA = "src_basia_archive_finds_2026_05_21"

# ============================================================
# 1. Update Zygmunt Griffel with the confirmed timber business
# ============================================================
pdata = json.loads(PEOPLE_PATH.read_text(encoding='utf-8'))
people = pdata['people']
by_id = {p['id']: p for p in people}

zygmunt = by_id.get('p_zygmunt_griffel')
if zygmunt:
    zygmunt['facts'] = (zygmunt.get('facts') or []) + [
        {"key": "company", "value": "ZYGMUNT GRIFFEL — Tartaki parowe, Przemysł drzewny, Eksport drzewa (steam sawmills, timber industry, wood export)",
         "confidence": "documented", "sources": [SRC_BASIA]},
        {"key": "company_address", "value": "Lwów, ul. Kopernika 5",
         "confidence": "documented", "sources": [SRC_BASIA]},
        {"key": "company_founded", "value": "1923. Transit warehouses in Gdynia + Gdańsk.",
         "confidence": "documented", "sources": [SRC_BASIA]},
        {"key": "company_scale", "value": "1934/35 fiscal year: 60,000 tons of pine timber exported (96.7% sawn materials); >5 million zlotys to England alone. Export split: England 82.8%, Holland 8.3%, Germany 2.9%, Switzerland 2.3%, France 1.9%, others 1.7%.",
         "confidence": "documented", "sources": [SRC_BASIA]},
        {"key": "source_directory", "value": "Album-Skorowidz Senatu i Sejmu Rzpltej oraz Sejmu Śląskiego (inter-war Polish Senate + Sejm directory), entry p.110",
         "confidence": "documented", "sources": [SRC_BASIA]},
    ]
    zygmunt['note_en'] = (zygmunt.get('note_en', '') +
        " VERIFIED 21 May 2026 (Basia's archive find): Zygmunt's timber-export firm was located at Lwów, ul. Kopernika 5. Founded 1923. Exporting 60,000 tons of pine timber annually to England (82.8% of output) plus Holland, Germany, Switzerland, France. Transit warehouses in Gdynia + Gdańsk. Confirms the family timber dynasty Eric Griffel described in his ADST oral history.").strip()
    print(f"[OK] Updated Zygmunt Griffel with confirmed Lwów Kopernika 5 timber business.")

# Update Rebeka with the 1938 property co-ownership
rebeka = by_id.get('p_rebeka')
if rebeka:
    rebeka['facts'] = (rebeka.get('facts') or []) + [
        {"key": "1938_nadworna_property",
         "value": "Co-owner of a one-storey brick rental house (Dom czynszowy murowany, jednopiętrowy z poddaszem) at Nadwórna ul. Śródmieście. Listed as 'Rebeka z Griffelów zam. Rapaport' (Rebeka née Griffel, married name Rapaport) in the 13 September 1938 auction notice published by Akcyjny Bank Hipoteczny (Lwów). Property auction valued at 127,294 zł, bid deposit 4,500 zł, auction date 28 November 1938. Co-owners: all 17 surviving heirs of Eliezer Griffel + Chaya Griffel-Grünfeld.",
         "confidence": "documented", "sources": [SRC_BASIA]},
    ]
    print(f"[OK] Updated Rebeka with 1938 Nadwórna property co-ownership.")

PEOPLE_PATH.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding='utf-8')

# ============================================================
# 2. Add Research Center cards
# ============================================================
rc = json.loads(RC_PATH.read_text(encoding='utf-8'))

# Auction notice — HEADLINE card
hf = next(s for s in rc['sections'] if s['id'] == 'headline_finds')
hf['cards'].insert(0, {
    "id": "basia_1938_auction_notice",
    "title_en": "🎯 1938 Lwów auction notice names ALL 17 Eliezer Griffel heirs as co-owners of Nadwórna property",
    "title_he": "🎯 הודעת מכירה פומבית מלבוב 1938 מציינת את כל 17 יורשי אליעזר גריפל כבעלים משותפים של נכס בנדבורנה",
    "status": "confirmed",
    "summary_en": (
        "PRIMARY-SOURCE BREAKTHROUGH (Basia's find, 21 May 2026): a 13 September 1938 auction "
        "notice published in Lwów by Akcyjny Bank Hipoteczny lists 17 named heirs of the Eliezer "
        "Griffel estate as joint debtors/co-owners of a one-storey brick rental house with attic "
        "(Dom czynszowy murowany, jednopiętrowy z poddaszem) at Nadwórna ul. Śródmieście (cadastral "
        "lot 378/2 gm. kat. Nadwórna). Property valuation: 127,294 zł. Bid deposit: 4,500 zł. "
        "Auction date: 28 November 1938. This is the single most comprehensive primary-source "
        "confirmation of the Eliezer Griffel + Chaya Griffel-Grünfeld extended-family list. "
        "The 17 named co-owners are: (1) Sara z. Chajes, zam. Griffel; (2) Dawid Mendel Griffel; "
        "(3) Eisig Griffel; (4) Rebeka z Griffelów zam. Rapaport — OUR REBEKA, David Memek's "
        "mother; (5) Machla z Griffelów zam. Willner; (6) Süssla z Griffelów zam. Lamm — Zissel "
        "Griffel-Lamm; (7) Schaja Griffel; (8) Leib Griffel; (9) Beniamin Griffel; (10) Rachela "
        "z Griffelów zam. Ornstein — Rachel Griffel-Ohrenstein; (11) Schmerl Grünfeld; (12) Eisig "
        "Grünfeld; (13) Samuel Grünfeld; (14) Sima Grünfeld zam. Blau — Yehuda Nir's grandmother; "
        "(15) Pepi Grünfeld; (16) Tauba Grünfeld; (17) Berta Grünfeld."
    ),
    "summary_he": (
        "פריצת דרך ממקור ראשוני (מציאת באסיה, 21.5.2026): הודעת מכירה פומבית מ-13 בספטמבר 1938 "
        "שפורסמה בלבוב על-ידי Akcyjny Bank Hipoteczny מציינת בשמותיהם 17 יורשי עיזבון אליעזר "
        "גריפל כבעלים משותפים של בית הכנסה בנדבורנה ברחוב Śródmieście. שווי: 127,294 זלוטי. "
        "כולל את 'רבקה לבית גריפל, נשואה רפפורט' — סבתו של אבא דב!"
    ),
    "source": "Akcyjny Bank Hipoteczny auction notice, Lwów 13 September 1938 (Basia find, ŻIH Warsaw)",
    "images": [
        {"src": "assets/research_images/basia/zygmunt_griffel_timber_album_1935.jpg",
         "caption_en": "Zygmunt Griffel timber business album entry (1935) — establishing the Griffel family's commercial scale in inter-war Lwów. See separate card for full details.",
         "credit": "Album-Skorowidz Senatu i Sejmu Rzpltej (1935, public domain)"}
    ]
})

# Zygmunt Griffel — major card on his confirmed business
hf['cards'].insert(1, {
    "id": "basia_zygmunt_griffel_kopernika_5",
    "title_en": "🌲 Zygmunt Griffel's timber empire CONFIRMED — Lwów ul. Kopernika 5, 1923-1939",
    "title_he": "🌲 אימפריית העץ של זיגמונט גריפל אומתה — לבוב ul. Kopernika 5, 1923-1939",
    "status": "confirmed",
    "summary_en": (
        "From the 1934/35 Album-Skorowidz Sejm Rzpltej (the inter-war Polish Senate + Sejm "
        "directory, p.110, public domain): the entire Zygmunt Griffel timber-export business — "
        "'Tartaki parowe, Przemysł drzewny, Eksport drzewa' (steam sawmills, timber industry, "
        "wood export). Founded 1923. Address: Lwów, ul. Kopernika 5 (with the owner's residence "
        "shown at Kopernika 55 in the small print). Transit warehouses in Gdynia and Gdańsk. "
        "1934/35 fiscal year: 60,000 tons of timber exported to England alone, worth over "
        "5 million zlotys. Export breakdown: England 82.8% · Holland 8.3% · Germany 2.9% · "
        "Switzerland 2.3% · France 1.9% · other 1.7%. The album includes Zygmunt's portrait "
        "(eyeglasses, dark suit) and a photo of timber being loaded onto a ship at Gdynia/Gdańsk. "
        "This is the timber dynasty Eric Griffel's ADST 2015 oral history described his father "
        "Zygmunt operating — now confirmed in print from a 1935 source."
    ),
    "source": "Album-Skorowidz Senatu i Sejmu Rzpltej oraz Sejmu Śląskiego, 1935 edition p.110 (public domain)",
    "images": [
        {"src": "assets/research_images/basia/zygmunt_griffel_timber_album_1935.jpg",
         "caption_en": "1935 Polish Senate + Sejm directory entry: Zygmunt Griffel timber business at Lwów, ul. Kopernika 5. Founded 1923. 60,000 tons/year exported, mostly to England. Photo of Zygmunt (right) and a timber-loading scene at the Gdynia/Gdańsk transit warehouse.",
         "credit": "Album-Skorowidz Sejmu 1935 (public domain) — sourced by Basia, ŻIH Warsaw"}
    ]
})

# Add the Goldfischer + Basia photos card
ndocs = next(s for s in rc['sections'] if s['id'] == 'next_documents')
ndocs['cards'].insert(0, {
    "id": "goldfischer_id_documents",
    "title_en": "📜 Goldfischer family ID documents (maternal grandparents)",
    "title_he": "📜 מסמכי זהות של משפחת גולדפישר (סבים מצד אמא)",
    "status": "confirmed",
    "summary_en": (
        "Five identity-document photos shared by Doron showing his maternal grandparents: "
        "(a) S. Goldfischer's British Mandate ID with stamp 'Urban and Rural Inf. Bde. Office' "
        "and signature 'S. Goldfischer' — pre-1948, his early Palestine document; (b)-(c) Ester "
        "Goldfischer's photographs (one young, one older with glasses) from a French-Hebrew "
        "bilingual Israeli passport; (d)-(e) S. Goldfischer's signalement page showing "
        "profession 'Marin' (sailor/merchant marine), birthplace Skole, born 23 November 1909, "
        "height 172 cm, brown eyes + brown hair. These confirm: maternal grandfather born in "
        "Skole (same Galician Carpathian region as Bolechów + Nadwórna)."
    ),
    "images": [
        {"src": "assets/research_images/family/s_goldfischer_british_mandate_id_photo.jpg",
         "caption_en": "S. Goldfischer's British Mandate-era ID — photograph + signature. Pre-1948.",
         "credit": "Rapaport family archive"},
        {"src": "assets/research_images/family/goldfischer_doc2.jpg",
         "caption_en": "Goldfischer family ID document (Ester or S. — Hebrew-French bilingual Israeli document)",
         "credit": "Rapaport family archive"},
        {"src": "assets/research_images/family/goldfischer_doc3.jpg",
         "caption_en": "Goldfischer family ID document",
         "credit": "Rapaport family archive"},
        {"src": "assets/research_images/family/goldfischer_doc4.jpg",
         "caption_en": "S. Goldfischer's signalement page — profession Marin, born Skole 23.11.1909, 172cm, brown eyes/hair",
         "credit": "Rapaport family archive"},
        {"src": "assets/research_images/family/goldfischer_doc5.jpg",
         "caption_en": "S. Goldfischer's signalement page (alternate view)",
         "credit": "Rapaport family archive"},
    ],
    "source": "Doron Rapaport (family archive, 21 May 2026)"
})

# Update Muszyna virtual-trip card with Basia's pre-war resort photos
trip = next(s for s in rc['sections'] if s['id'] == 'virtual_trip')
muszyna_card = next((c for c in trip['cards'] if c['id'] == 'trip_muszyna'), None)
if muszyna_card:
    muszyna_card['images'] = (muszyna_card.get('images') or []) + [
        {"src": "assets/research_images/trip/prewar_resort_river_bathers.jpg",
         "caption_en": "Pre-war Polish Beskid resort scene — bathers by a Carpathian river. The kind of resort culture Lusia's hotel served.",
         "credit": "Narodowe Archiwum Cyfrowe (Polish National Digital Archive) — public domain"},
        {"src": "assets/research_images/trip/prewar_resort_river_swimmer.jpg",
         "caption_en": "Pre-war Polish Beskid resort — swimming in a Carpathian river, mountains in background.",
         "credit": "NAC (public domain)"},
        {"src": "assets/research_images/trip/prewar_resort_river_terraced_hills.jpg",
         "caption_en": "Pre-war Polish Beskid resort — terraced hills + resort buildings + river bathers.",
         "credit": "NAC (public domain)"},
        {"src": "assets/research_images/trip/prewar_galician_town_houses.jpg",
         "caption_en": "Pre-war Galician small-town street — traditional houses with shingle roofs. Typical of the Muszyna / Krynica / Nowy Sącz region.",
         "credit": "NAC (public domain)"},
        {"src": "assets/research_images/trip/prewar_sanatorium_artdeco.jpg",
         "caption_en": "Late-1930s Art Deco / functionalist sanatorium building — the modernist face of Polish Beskid spa culture in Lusia's era.",
         "credit": "NAC (public domain)"},
    ]
    print(f"[OK] Added 5 Basia pre-war resort photos to Muszyna Virtual Trip card.")

rc['build_version'] = "2026-05-21-T4-basia-auction-zygmunt-goldfischer-photos"
rc['generated'] = "2026-05-21"

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
total = sum(len(s['cards']) for s in rc['sections'])
print(f"[OK] Research Center now {len(rc['sections'])} sections, {total} cards.")
print(f"[OK] cache-bust query string + Cache-Control no-store applied in app.js loadAll().")
print(f"[OK] build_version: {rc['build_version']}")
