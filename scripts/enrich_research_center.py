"""Enrich research_center.json with:
- Direct quotes extracted from cached Yizkor / Gelles sources
- Embedded images downloaded into platform/assets/research_images/
- The 9 new living cousins discovered in round 2
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC = REPO / 'platform' / 'data' / 'research_center.json'

data = json.loads(RC.read_text(encoding='utf-8'))

# Helper: find a card by id across all sections
def get_card(sec_id, card_id):
    for s in data['sections']:
        if s['id'] == sec_id:
            for c in s['cards']:
                if c['id'] == card_id:
                    return c
    return None

def get_section(sec_id):
    return next((s for s in data['sections'] if s['id'] == sec_id), None)

# ---- Headline finds: embed actual quotes + images ----

# 1. Bolechów Yizkor — embed the full extracted quote
card = get_card('headline_finds', 'bolechow_yizkor_naming')
if card:
    card['quote_en'] = (
        "The Revisionist ranks were organized as follows: adults in \"Hatza'r\", "
        "the young workers and students in \"Massadah\". The youngest were sent to \"Betar\". "
        "Thanks to comrade D. Rapaport (Eli Weitzner's son-in-law) the movement grew. They had "
        "interesting programs and summer camps that were also used for military exercises (along "
        "the model of P. W.). Besides developing cultural activities, there were also Hebrew "
        "classes under the direction of Hinde Delman."
    )
    card['source'] = "Sefer ha-zikaron le-kedoshei Bolechow (Memorial Book of the Martyrs of Bolechow), Y. Eshel ed., 1957 — Yiddish page 278, \"Memories\" by Abraham Weber, translated by Judie Goldstein"
    card['extracted_from'] = "research_cache/bol278.html"

# 4. Foresta + Zetperol — embed Yad Vashem quote
card = get_card('headline_finds', 'foresta_zetperol')
if card:
    card['quote_en'] = (
        "The 'Foresta' company was active in the city, leasing woodlands from the Polish "
        "authorities in order to chop timber and prepare it for export. Both the managers of the "
        "company in the city and its workers were Jewish… In 1937, the government contract with "
        "the 'Foresta' company – whose owners and workers in Nadwórna were Jewish – was terminated, "
        "due to intervention by antisemitic Ukrainians and Poles. The company's Jewish employees "
        "were fired. … Some 600 Jews worked daily at the saw mill (during the German occupation)."
    )

# Bolechow synagogue image card
photo_section = get_section('photos_and_archives')

# Embed images in the photo cards
jgb_bol = get_card('photos_and_archives', 'jgb_bolechow')
if jgb_bol:
    jgb_bol['images'] = [
        {
            "src": "assets/research_images/bolechow_great_synagogue.jpg",
            "caption_en": "The Great Synagogue of Bolechów — northern side. Photo: Vladimir Levin (2009) for Jewish Galicia & Bukovina.",
            "caption_he": "בית הכנסת הגדול של בולחוב — צד צפוני. צילום: ולדימיר לוין (2009) עבור JGB.",
            "credit": "Jewish Galicia & Bukovina — jgaliciabukovina.net"
        },
        {
            "src": "assets/research_images/bolechow_1914_map.jpg",
            "caption_en": "Map of Bolechów 1914 — courtesy New York Public Library, hosted at JGB.",
            "caption_he": "מפת בולחוב 1914 — באדיבות הספרייה הציבורית של ניו יורק.",
            "credit": "New York Public Library / JGB"
        },
        {
            "src": "assets/research_images/bolechow_23-Rynek-North1.jpg",
            "caption_en": "Bolechów town square (Rynek), northern side — pre-war view.",
            "caption_he": "כיכר העיר של בולחוב, צד צפוני — מבט מלפני המלחמה.",
            "credit": "JGB"
        },
        {
            "src": "assets/research_images/bolechow_37-forest-lyc.jpg",
            "caption_en": "Bolechów Forestry Lyceum — relevant given the Weitzner-tannery / wood trade.",
            "caption_he": "בית הספר ליערנות של בולחוב — רלוונטי למשפחת וייצנר העוסקת בעיבוד עורות ובעץ.",
            "credit": "JGB"
        },
        {
            "src": "assets/research_images/bolechow_32-Halickaya1-tarbut.jpg",
            "caption_en": "Halicka Street — the Tarbut Hebrew school building. Hebrew-Zionist education in Bolechów.",
            "caption_he": "רחוב הליצקה — בניין בית הספר 'תרבות' לעברית. החינוך הציוני בבולחוב.",
            "credit": "JGB"
        },
        {
            "src": "assets/research_images/bolechow_39-School.jpg",
            "caption_en": "Bolechów Jewish school building.",
            "caption_he": "בניין בית הספר היהודי בבולחוב.",
            "credit": "JGB"
        },
    ]

jgb_nad = get_card('photos_and_archives', 'jgb_nadworna')
if jgb_nad:
    jgb_nad['images'] = [
        {
            "src": "assets/research_images/nadworna_town_hall.jpg",
            "caption_en": "Nadwórna — the old Town Hall on Hetman Mazepa Street. Public-domain photo (Wikipedia Commons).",
            "caption_he": "נדבורנה — בניין העירייה הישן ברחוב הטמן מזפה.",
            "credit": "Wikipedia Commons"
        },
        {
            "src": "assets/research_images/nadworna_hotel.jpg",
            "caption_en": "Nadwórna — historic hotel building. Public-domain photo (Wikipedia Commons).",
            "caption_he": "נדבורנה — בניין מלון היסטורי.",
            "credit": "Wikipedia Commons"
        },
    ]

# ---- Add Zaynvl + Zishe direct Yizkor quote to additional_relatives ----
card = get_card('additional_relatives', 'zaynvl_rapaport')
if card:
    card['quote_en'] = (
        "In the management of the big factories were Jews, who were doing their task their whole "
        "life, from their youth. They were engaged in the construction of the factory's building "
        "from the very beginning. In the surroundings they were well known as specialists in the "
        "wood-profession. The following should be mentioned: Mr. (Reb) Moyshe Bin, who emigrated "
        "to Israel and died here; Zaynvl Rapaport; Aharon Shor and the Shtrasman-brothers."
    )
    card['source'] = "Bolechów Yizkor 1957 — Wood and Other Industries by Abraham Weber, p.102"

card = get_card('additional_relatives', 'zishe_vaytsner')
if card:
    card['quote_en'] = (
        "Other industries, like the leather or candle industry were not less represented by "
        "business activities at the station. The latter was concentrated around two factories, "
        "one run by Yoel Halpern and the other run by Zishe Vaytsner."
    )
    card['source'] = "Bolechów Yizkor 1957 — Wood and Other Industries by Abraham Weber, p.102"

# ---- Add Hans Krueger / DAIFO R-432 / Glesinger as new high-value documents ----

next_docs = get_section('next_documents')
if next_docs:
    # Insert at front of cards
    new_docs = [
        {
            "id": "daifo_r432_krueger",
            "title_en": "🎯 DAIFO R-432/1/1 — Hans Krueger's Nadwórna execution orders Oct-Nov 1941",
            "title_he": "🎯 ДАІФО ר-432/1/1 — פקודות ההוצאה להורג של הנס קרוגר נדבורנה אוקטובר-נובמבר 1941",
            "status": "lead",
            "summary_en": (
                "Hans Krueger was the SD-Hauptsturmführer overseeing the destruction of Jewish life in "
                "Bezirk Stanislau (incl. Nadwórna). DAIFO fond R-432, opys 1, sprava 1 contains his execution "
                "orders for 13 October – 7 November 1941, the immediate aftermath of the 6 October 1941 great "
                "Aktion. The village Zelenoe (Зелена, near Nadwórna) is named. This fond may name Berisz "
                "Rapaport and Rebeka Griffel-Rapaport among the executed — the strongest hope of confirming "
                "their exact fate."
            ),
            "source": "DAIFO (State Archive of Ivano-Frankivsk Oblast) — Yad Vashem academic article on Krueger",
            "urls": ["https://www.yadvashem.org/articles/academic/hans-krueger-and-the-murder-of-the-jews-in-the-stanislawow-region.html"],
        },
        {
            "id": "brussels_aliens_police",
            "title_en": "🎯 Brussels Aliens Police dossier — David + Lusia + Shimon (guaranteed)",
            "title_he": "🎯 תיקי משטרת הזרים בבריסל — דוד, לוסיה ושמעון (מובטח)",
            "status": "lead",
            "summary_en": (
                "Archives générales du Royaume Brussels holds 2 million+ Aliens Police individual dossiers. "
                "David, Lusia and Shimon each have a dossier from their April 1946 Brussels arrival — guaranteed. "
                "Will contain photo, civil-status documents, employment declaration, addresses 1946-47, exit "
                "notice on departure via Sète April 1947. Expected to contain David's first written wartime "
                "narrative naming his murdered family."
            ),
            "urls": ["mailto:agr.searchdesk@arch.be", "https://search.arch.be"],
            "source": "Archives générales du Royaume, Bruxelles"
        },
        {
            "id": "berlin_beg",
            "title_en": "🎯 Landesarchiv Berlin — David's Wiedergutmachung file",
            "status": "lead",
            "summary_en": (
                "Berlin Senate decided early 2026 to transfer 250,000-280,000 BEG individual files (1953-1969) "
                "from LABO to the Landesarchiv. David almost certainly has a BEG file — the memoir explicitly "
                "states he and Lusia used the German reparations payments to buy their Haifa apartment on "
                "Moriah Street 93. Expected contents: persecution narrative (in David's hand, German or Hebrew), "
                "witness affidavits, photo, payment records."
            ),
            "urls": ["mailto:info@landesarchiv-berlin.de"],
            "source": "Landesarchiv Berlin / LABO"
        },
    ]
    next_docs['cards'] = new_docs + next_docs['cards']

# ---- Add Glesinger context card to headline_finds ----
hf = get_section('headline_finds')
if hf:
    hf['cards'].append({
        "id": "glesinger_timber_aryanised",
        "title_en": "The Nadwórna sawmill where David worked was likely Aryanised GLESINGER timber property",
        "title_he": "מנסרת נדבורנה שבה עבד דוד הייתה ככל הנראה רכוש משפחת גלסינגר שעוּבּר לארים",
        "status": "likely",
        "summary_en": (
            "Egon Glesinger (1905-1979) was a Galician Jewish forestry magnate (doctorate \"Le bois en Europe\" "
            "1931 Geneva, author of \"Nazis in the Woodpile\" 1942). His family conglomerate owned much of the "
            "Galician timber industry pre-war. The Nadwórna sawmill where David worked under Nazi occupation "
            "was very likely a Glesinger property Aryanised in 1941 under Treuhänder administration. "
            "Confirmable via Bundesarchiv R187 Treuhandstelle or Galizien Treuhand records at Bundesarchiv "
            "Berlin Lichterfelde R-series."
        ),
        "source": "WikiTree biography + Glesinger 1942 book \"Nazis in the Woodpile\"",
        "urls": ["https://www.wikitree.com/wiki/Glesinger-15"]
    })

# ---- Add NEW LIVING COUSINS round 2 to the living_cousins section ----
lc = get_section('living_cousins')
if lc:
    # Correct Edward Gelles status (he is ALIVE)
    for c in lc['cards']:
        if c['id'] == 'cousin_haim_gelles':
            c['title_en'] = "Haim Gelles + Avi Gelles — UK / Israel (son + grandson of Edward Gelles)"
    new_living = [
        {
            "id": "cousin_edward_gelles_alive",
            "title_en": "🟢 Edward Gelles — London (age 98, LIVING, the senior living expert on our family)",
            "title_he": "🟢 אדוארד גלס — לונדון (בן 98, חי, המומחה החי הבכיר על משפחתנו)",
            "status": "confirmed",
            "summary_en": (
                "Born Vienna 24 November 1927; lives in London. 2nd cousin once removed of David Memek Rapaport. "
                "The published genealogist whose Balliol College Oxford archive documents the entire Griffel-"
                "Chajes-Wahl-Gelles dynasty. His mother Regina Gelles née Griffel was David Memek's first cousin. "
                "Authored 'An Ancient Lineage: European Roots of a Jewish Family' (2006). Knows everyone on the "
                "maternal line personally. THE SINGLE MOST IMPORTANT CONTACT FOR DORON."
            ),
            "summary_he": (
                "נולד בווינה ב-24 בנובמבר 1927; חי בלונדון. בן הדוד פעם שנייה של דוד ממק רפפורט. הגנאלוג שפרסם "
                "את הארכיון של אוקספורד שמתעד את כל שושלת גריפל-חיות-וואהל-גלס. אמו רגינה גלס לבית גריפל הייתה "
                "בת דודתו הראשונה של דוד ממק. הכותרת החשובה ביותר ליצירת קשר."
            ),
            "source": "Edward Gelles, Griffel of Nadworna PDF + Balliol Archives",
            "urls": ["mailto:archivist@balliol.ox.ac.uk", "https://archives.balliol.ox.ac.uk/Modern%20Papers/gelles/"]
        },
        {
            "id": "cousin_tali_griffel_ginsburg",
            "title_en": "🟢 Tali Griffel Ginsburg — NYC (Ras Burqa attack survivor, 3rd cousin)",
            "status": "confirmed",
            "summary_en": (
                "LIVING — NYC. 3rd cousin of David Memek Rapaport. Daughter of Andrew Griffel. Survivor of the "
                "Ras Burqa terror attack 5 October 1985 in Sinai — her mother Anita Spindel Griffel was murdered "
                "shielding 5-year-old Tali with her body. Andrew raised her in NYC. Now married, mother. "
                "Contributor to Tablet Magazine and Israel Story podcast (episode 'Thicker Than Water')."
            ),
            "source": "Edward Gelles, Griffel of Nadworna + Tablet Magazine + Israel Story podcast",
            "urls": ["https://www.tabletmag.com/tags/tali-griffel", "https://www.israelstory.org/episode/thicker-than-water/"]
        },
        {
            "id": "cousin_nir_siblings",
            "title_en": "🟢 The 4 Nir siblings — NYC (Sarah, David, Daniel, Aaron; children of Yehuda Nir)",
            "status": "confirmed",
            "summary_en": (
                "All four children of Yehuda Nir (1930-2014, author of 'The Lost Childhood') are LIVING in NYC. "
                "Sarah Maslin Nir is a New York Times staff reporter. David Nir is Political Director of Daily "
                "Kos. Daniel and Aaron are private investor and fashion executive respectively (from Yehuda's "
                "first marriage). All 2nd cousins once removed of David Memek. Mother Bonnie Maslin is a "
                "psychiatrist/author — likely warmest first-contact point."
            ),
            "source": "Edward Gelles + NYT + Daily Kos public profiles",
            "urls": ["https://www.nytimes.com/by/sarah-maslin-nir", "mailto:davidnir@dailykos.com"]
        },
        {
            "id": "cousin_joseph_griffel",
            "title_en": "🟢 Joseph Griffel — only surviving child of Dr Jacob Griffel (Istanbul rescuer)",
            "status": "confirmed",
            "summary_en": (
                "Born 1953. LIVING. Only surviving child of Dr Jacob Griffel (1900-1962, the Vaad ha-Hatzala "
                "Istanbul rescuer of Polish Jews during WWII). Jacob's first wife and children perished in the "
                "Warsaw blitzkrieg; Joseph from Jacob's second marriage to Miriam Rottenberg (1914-1998). "
                "2nd cousin once removed of David Memek."
            ),
            "source": "Edward Gelles, Griffel of Nadworna"
        },
        {
            "id": "cousin_diana_griffel",
            "title_en": "Diana Margaret Griffel — London (b. 27 Oct 1943, status uncertain)",
            "status": "lead",
            "summary_en": (
                "Born London 27 October 1943. Daughter of Edward Griffel (David Memek's uncle) + Susan Manson. "
                "Status uncertain — would be 82. 2nd cousin of David Memek. Worth a targeted UK search."
            ),
            "source": "Edward Gelles, Griffel of Nadworna"
        },
        {
            "id": "cousin_jackie_griffel",
            "title_en": "🟢 Jackie Boehme Griffel — Rockville MD (Eric Griffel's widow)",
            "status": "confirmed",
            "summary_en": (
                "LIVING — Rockville Maryland area. Widow of Eric Griffel (1930-2020), Edward Gelles's first "
                "cousin and USAID Pakistan Station Chief who signed the famous 'Blood Telegram' protesting US "
                "policy during the 1971 Bangladesh genocide. Contact via USAID Alumni Association obituary page."
            ),
            "source": "USAID Alumni Association",
            "urls": ["https://usaidalumni.org/eric-griffel/"]
        },
        {
            "id": "cousin_tripcovich_trieste",
            "title_en": "🟢 The Tripcovich family of Trieste — Italian shipping aristocracy",
            "status": "likely",
            "summary_en": (
                "Branch via Rachel Griffel + Bonya Ohrenstein → Lucia Ohrenstein (1910-1988) who became "
                "Countess Tripcovich, marrying Italian shipping magnate Oliviero Tripcovich (later Romeo Puri "
                "Purini and Count Livio Tripcovich). Italian descendants in Trieste — Diodato Tripcovich named. "
                "Findable via Trieste Chamber of Commerce / Italian shipping history archives."
            ),
            "source": "Edward Gelles, Facets of My Family History Part 2, chapter 10"
        },
    ]
    lc['cards'] = lc['cards'] + new_living

# ---- Add a new "Test for Doron" card ----
hf['cards'].insert(0, {
    "id": "test_was_david_a_kohen",
    "title_en": "🧪 CRITICAL TEST FOR DOROD'S FAMILY — Was David Memek a Kohen?",
    "title_he": "🧪 מבחן קריטי למשפחת דורון — האם דוד ממק היה כהן?",
    "status": "lead",
    "summary_en": (
        "The 'Rapaport' surname has a famous rabbinical-dynasty origin (Italian Kohanim from R. Meshulam "
        "Jekuthiel HaKohen Rappa d.1450 Mainz → Porto → Mantua, Galician branch via R. Abraham Rapoport "
        "'Schrenzel' Lemberg 1584-1651). Even Edward Gelles after 25+ years of research couldn't determine "
        "whether OUR Berisz Rapaport line is a Galician offshoot of this dynasty. The diagnostic test is "
        "whether David was a KOHEN — was he called up first to Torah? Did he duchen (perform the priestly "
        "blessing)? Did he avoid funerals/entering cemeteries? If YES on any → 350-year Rapoport rabbinical "
        "dynasty descent confirmed. If NO → coincidental surname. ASK DOV."
    ),
    "summary_he": (
        "המבחן הקריטי שמשפחת דורון יכולה לענות עליו: האם דוד ממק היה כהן? אם כן — מאשר ירידה משושלת רפפורט "
        "הרבנית בת 600 שנים. שאלות לדוב: האם דוד עלה ראשון לתורה? האם דוכן? האם נמנע מבתי קברות? תשובת חיוב "
        "אחת — וקושר אותנו לשושלת. תשובת שלילה — שם משפחה במקרה בלבד."
    ),
    "source": "Edward Gelles + Wikipedia 'Rappaport family'"
})

RC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] research_center.json enriched.")
print(f"Sections: {len(data['sections'])}")
total_cards = sum(len(s['cards']) for s in data['sections'])
print(f"Total cards: {total_cards}")
print(f"Cards with quotes: {sum(1 for s in data['sections'] for c in s['cards'] if c.get('quote_en'))}")
print(f"Cards with images: {sum(1 for s in data['sections'] for c in s['cards'] if c.get('images'))}")
