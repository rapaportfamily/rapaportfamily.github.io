"""Dossier-20 integration + audit fixes (2026-05-21 round T10).

What this script does:
1. Update trip_sete_theodor_herzl Trip card:
   - Add 2 PD ship photos (Haifa 1947 + naval-corps view)
   - Add verified ship-history paragraph (ex-HMS "Guardian", 1907 Newcastle,
     Swan Hunter & Wigham Richardson, 1,768 tons) — explicitly disambiguated
     from SS Exodus 1947 (= ex-President Warfield).
2. Update trip_cyprus_karaolos Trip card:
   - Camp numbers 55, 60, 61, 62, 63 = summer tent camps at Caraolos.
   - Dekhelia/Decauville = winter Nissen-hut camps near Larnaca (~50km).
   - Pointer to JDC birth-list + Yad Vashem/USHMM name databases.
3. Wire up orphan images:
     mallorca_lead.jpg            → vidal_rapapa_1305
     portobuffole_lead.jpg        → rapa_porto_isaac_hamoel
     verona_lead.jpg              → verona_1594_family_emblem
     padua_lead.jpg               → katzenellenbogen_padua_venice
     tarnobrzeg_lead.jpg          → tarnobrzeg_wahl_to_chawa
     staten_island_baron_hirsch.jpg → burial_records_baron_hirsch_zygmunt
4. Fix Balliol http→https.
5. Bump build_version to 2026-05-21-T10-dossier20-audit-fixes.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'

rc = json.loads(RC_PATH.read_text(encoding='utf-8'))


def find_card(section_id, card_id):
    for s in rc['sections']:
        if s['id'] == section_id:
            for c in s['cards']:
                if c['id'] == card_id:
                    return c
    raise KeyError(f"{section_id}/{card_id}")


# ── 1) Theodor Herzl Trip card ───────────────────────────────────────
herzl = find_card('virtual_trip', 'trip_sete_theodor_herzl')
herzl['ship_history_en'] = (
    "The Theodor Herzl was NOT the famous Exodus 1947 (which was ex-SS "
    "President Warfield). The Theodor Herzl was the ex-British cable-laying "
    "ship HMS/SS \"Guardian\", built in 1907 by Swan Hunter & Wigham Richardson "
    "in Newcastle, England — 1,768 tons, triple-expansion steam engine, ~10 "
    "knots. Acquired by Mossad LeAliyah Bet in 1946 and refitted at Marseille "
    "to carry roughly 2,600 passengers in standing-only deck space."
)
herzl['ship_history_he'] = (
    "אוניית תיאודור הרצל אינה אוניית אקסודוס 1947 המפורסמת (שהייתה ה-SS פרסידנט "
    "וורפילד לשעבר). תיאודור הרצל הייתה ספינת הנחת-כבלים בריטית בשם HMS/SS "
    "\"גארדיאן\", שנבנתה ב-1907 על-ידי Swan Hunter & Wigham Richardson בניוקאסל, "
    "אנגליה — 1,768 טון, מנוע קיטור, מהירות כ-10 קשר. נרכשה ב-1946 על-ידי המוסד "
    "לעלייה ב' ושופצה במרסיי לנשיאת כ-2,600 מעפילים בעמידה על הסיפון."
)
herzl['urls'] = [
    "https://www.palyam.org/English/Hahapala/hf/hf_Theodor_Herzl.pdf",
    "http://paulsilverstone.com/ship/theodor-herzl/",
    "https://en.wikipedia.org/wiki/SS_Exodus"
]
herzl['images'] = [
    {
        "src": "assets/research_images/trip/sete_lead.jpg",
        "caption_en": "The French port of Sète — where the Theodor Herzl sailed from on 2 April 1947 with 2,641 Ma'apilim including David, Lusia, Shimon and infant Dov.",
        "caption_he": "נמל סט בצרפת — שממנו הפליגה תיאודור הרצל ב-2 באפריל 1947 עם 2,641 מעפילים, ובהם דוד, לושה, שמעון ודב התינוק.",
        "credit": "Wikipedia Commons (CC-BY-SA)"
    },
    {
        "src": "assets/research_images/trip/theodor_herzl_haifa_1947.png",
        "caption_en": "The Aliyah Bet ship Theodor Herzl in Haifa, April 1947 — black-stained 'NEVER DIE!' banner painted by the ma'apilim after the British boarding that killed three.",
        "caption_he": "תיאודור הרצל בנמל חיפה, אפריל 1947 — שלט מצוייר ביד 'NEVER DIE!' שצבעו המעפילים לאחר שלוש ההריגות בהשתלטות הבריטית.",
        "credit": "Public domain — pre-1948 photograph"
    },
    {
        "src": "assets/research_images/trip/theodor_herzl_ship_naval_corps.jpg",
        "caption_en": "Side-view of the Theodor Herzl from naval records — built 1907 in Newcastle as the cable ship HMS Guardian, 1,768 tons.",
        "caption_he": "מבט-צד של תיאודור הרצל מתוך תיעוד חיל הים — נבנתה ב-1907 בניוקאסל כספינת כבלים HMS Guardian, 1,768 טון.",
        "credit": "Public domain — naval-corps archive"
    }
]

# ── 2) Cyprus Karaolos Trip card ─────────────────────────────────────
karaolos = find_card('virtual_trip', 'trip_cyprus_karaolos')
karaolos['summary_en'] = (
    "After British interception, the ship's passengers were taken to the Cyprus "
    "internment camps. The British ran two camp clusters: SUMMER tent camps "
    "numbered 55, 60, 61, 62 and 63 at Caraolos/Karaolos (north of Famagusta), "
    "and WINTER Nissen-hut camps at Dekhelia/Decauville (near Larnaca, ~50km "
    "away). Nine camps at peak; 53,510 Jews held 1946-1949; ~2,200 children "
    "born in captivity. David's family was held ~8 months. Wounded passengers "
    "and unaccompanied minors were diverted to Atlit camp in British Mandate "
    "Palestine instead of Cyprus."
)
karaolos['summary_he'] = (
    "לאחר השתלטות הבריטים, נוסעי האוניה הובלו למחנות המעצר בקפריסין. הבריטים "
    "ניהלו שני אשכולות מחנות: מחנות אוהלים קיציים במספרים 55, 60, 61, 62 ו-63 "
    "בקראולוס (צפונית לפמגוסטה), ומחנות חורף עם צריפי ניסן בדכליה/דקוויל "
    "(ליד לרנקה, כ-50 ק\"מ משם). 9 מחנות בשיא; 53,510 יהודים נעצרו 1946-1949; "
    "כ-2,200 ילדים נולדו במעצר. משפחת רפפורט הוחזקה כ-8 חודשים. הפצועים "
    "והקטינים ללא מלווים הופנו למחנה עתלית בארץ ישראל המנדטורית במקום לקפריסין."
)
karaolos['search_tips_en'] = (
    "There is NO single public detainee index for the Cyprus camps. To search "
    "for relatives by name use: Yad Vashem Central Database of Shoah Victims "
    "and Survivors (collections.yadvashem.org/en/names) and the USHMM Holocaust "
    "Survivors and Victims Database. JDC Archives holds only the Aug-1948 to "
    "Feb-1949 birth lists (>500 entries, with camp number)."
)
karaolos['urls'] = [
    "https://en.wikipedia.org/wiki/Cyprus_internment_camps",
    "https://en.wikipedia.org/wiki/Karaolos_prisoner_of_war_camp",
    "https://www.palyam.org/English/Arrests/hfCyprus.php",
    "https://archives.jdc.org/topic-guides/detained-in-cyprus/",
    "https://collections.yadvashem.org/en/names",
    "https://www.ushmm.org/online/hsv/person_advance_search.php"
]

# ── 3) Wire up orphan images to natural cards ────────────────────────
ORPHAN_WIRINGS = [
    # (section_id, card_id, image_filename, caption_en, caption_he, credit)
    ("sephardic_origin", "vidal_rapapa_1305",
     "mallorca_lead.jpg",
     "Palma, Mallorca — where Dr Vidal Rapapa practiced medicine in 1305, the earliest documented Rapaport ancestor.",
     "פלמה דה מיורקה — בה נהג ד\"ר וידאל רפפא ברפואה ב-1305, אבי המשפחה הקדמון המתועד המוקדם ביותר.",
     "Wikipedia Commons (CC-BY-SA)"),
    ("sephardic_origin", "rapa_porto_isaac_hamoel",
     "portobuffole_lead.jpg",
     "Portobuffolè, Italy — the small Treviso-province town whose name was added to 'Rapa' to create the surname 'Rapa-Porto' c. 1550.",
     "פורטובופולה, איטליה — העיירה הקטנה במחוז טרוויסו ששמה צורף ל-'רפא' ויצר את שם המשפחה 'רפא-פורטו' (~1550).",
     "Wikipedia Commons (CC-BY-SA)"),
    ("sephardic_origin", "verona_1594_family_emblem",
     "verona_lead.jpg",
     "Verona, Italy — where R. Avraham Menachem ha-Kohen Rapa-Porto published 'Mincha Belulah' (1594) bearing the raven+priestly-blessing family emblem.",
     "ורונה, איטליה — בה פרסם רבי אברהם מנחם הכהן רפא-פורטו את 'מנחה בלולה' (1594) ובו סמל המשפחה: עורב ותחתיו ברכת כהנים.",
     "Wikipedia Commons (CC-BY-SA)"),
    ("wahl_katzenellenbogen", "katzenellenbogen_padua_venice",
     "padua_lead.jpg",
     "Padua, Italy — seat of R. Meir Katzenellenbogen 'MaHaRaM Padua' (1482-1565), Chief Rabbi of Padua, three generations before Saul Wahl.",
     "פאדובה, איטליה — מקום מושבו של רבי מאיר קצנלנבוגן 'מהר\"ם מפדואה' (1482-1565), רבה הראשי של פדואה.",
     "Wikipedia Commons (CC-BY-SA)"),
    ("wahl_katzenellenbogen", "tarnobrzeg_wahl_to_chawa",
     "tarnobrzeg_lead.jpg",
     "Tarnobrzeg, Poland — Galician town of the Wahl family that produced Chawa Wahl (1877-1941), great-grandmother of Dalia, Dana, Doron and Daniel Rapaport.",
     "טרנוברז'ג, פולין — עיירה גליציאנית של משפחת וואהל שממנה יצאה חוה וואהל (1877-1941), סבתא-רבא של דליה, דנה, דורון ודניאל רפפורט.",
     "Wikipedia Commons (CC-BY-SA)"),
    ("next_documents", "burial_records_baron_hirsch_zygmunt",
     "staten_island_baron_hirsch.jpg",
     "Baron Hirsch Cemetery, Staten Island NY — where Zygmunt Griffel (1897-1951) is buried in the Nadworner Young Men's Benevolent Association plot, Section I Gate 51.",
     "בית הקברות באראן הירש, סטטן איילנד — בו קבור זיגמונט גריפל (1897-1951), בחלקת אגודת בני הנעורים הנדבורנים, סקטור I, שער 51.",
     "Wikipedia Commons (CC-BY-SA)"),
]

wired = []
for sec, cid, fname, cap_en, cap_he, credit in ORPHAN_WIRINGS:
    card = find_card(sec, cid)
    img = {
        "src": f"assets/research_images/trip/{fname}",
        "caption_en": cap_en,
        "caption_he": cap_he,
        "credit": credit
    }
    if 'images' not in card:
        card['images'] = []
    # avoid duplicating if already wired in a prior run
    if not any(i.get('src') == img['src'] for i in card['images']):
        card['images'].append(img)
        wired.append(f"{sec}/{cid} ← {fname}")
    else:
        wired.append(f"{sec}/{cid} ← {fname} (already wired)")

# bolechow image lives at the top level, not under trip/
bolechow_path = REPO / 'platform' / 'assets' / 'research_images' / 'bolechow_33-Halickaya-Strashman.jpg'
if bolechow_path.exists():
    bolechow_card = find_card('headline_finds', 'bolechow_yizkor_naming')
    bolechow_img = {
        "src": "assets/research_images/bolechow_33-Halickaya-Strashman.jpg",
        "caption_en": "Bolechów, 33 Halickaya street — Strashman family residence, contextual reference for Bolechów Jewish naming records.",
        "caption_he": "בולחוב, רחוב הלצקאיה 33 — בית משפחת שטראשמן, הקשר לרישומי שמות יהודיים בבולחוב.",
        "credit": "Family archive"
    }
    if 'images' not in bolechow_card:
        bolechow_card['images'] = []
    if not any(i.get('src') == bolechow_img['src'] for i in bolechow_card['images']):
        bolechow_card['images'].append(bolechow_img)
        wired.append("next_documents/bolechow_yizkor_naming ← bolechow_33-Halickaya-Strashman.jpg")

# ── 4) Fix Balliol http→https (idempotent) ───────────────────────────
def walk(obj, fn):
    if isinstance(obj, dict):
        return {k: walk(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(x, fn) for x in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj

http_fixes = {'count': 0}
def fix_http(s):
    if 'http://archives.balliol.ox.ac.uk' in s:
        new = s.replace('http://archives.balliol.ox.ac.uk', 'https://archives.balliol.ox.ac.uk')
        http_fixes['count'] += 1
        return new
    return s
rc = walk(rc, fix_http)

# ── 5) Bump build_version ─────────────────────────────────────────────
rc['build_version'] = "2026-05-21-T10-dossier20-audit-fixes"

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')

print("=== Theodor Herzl card ===")
print(f"  ship_history added, 3 images, 3 urls")
print("\n=== Cyprus Karaolos card ===")
print(f"  camp numbers 55/60/61/62/63 documented, search_tips added, 6 urls")
print("\n=== Orphan images wired ===")
for w in wired:
    print(f"  {w}")
print(f"\n=== http→https fixes: {http_fixes['count']} ===")
print(f"\n=== build_version: {rc['build_version']} ===")
