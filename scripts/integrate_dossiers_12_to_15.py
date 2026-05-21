"""Integrate findings from dossiers 12-15 into people.json + research_center.json.

- Dossier 12: Eric Griffel ADST oral history, Pinkas Nadwórna, Tzvi Hirsh Filip
- Dossier 13: Foresta, Glesinger, Achwa Beitar hachshara, Theodor Herzl voyage details
- Dossier 14: Wahl-Katzenellenbogen ancestry through Chawa Wahl
- Dossier 15: Chanan Rapaport deceased 2022, Haifa Chevra Kadisha leads

Tree additions:
- R. Tzvi Hirsh Filip of Nadworna (1737-1802) — founding Nadwórna Hasidic Rebbe
- Saul Wahl Katzenellenbogen (1541-1617)
- R. Meir Katzenellenbogen "MaHaRaM Padua" (1482-1565)
- R. Samuel Judah Katzenellenbogen (1521-1597)
- R. Meir Wahl Katzenellenbogen "MaHaRaSH" (c.1565-1631)
- Shulim Wahl of Tarnobrzeg (Chawa's father)
- Sarah Safier of Tarnobrzeg (Chawa's mother)
- Reb Chaim Hager of Ottynia (1863-1931) — the Ottynia rebbe Eliezer Griffel followed

Corrections:
- Dr Chanan Rapaport — deceased 2022-01-02 (was listed living)
- Diana Margaret Griffel — deceased mid-1960s of cancer per Eric Griffel's oral history
- Update Chawa Wahl entry with parents + Saul Wahl descent

Research Center additions:
- Eric Griffel ADST oral history confirmation card
- Achwa Kibbutz Beitar hachshara card (1929-1936+, the kibbutz name was Achwa)
- Foresta confirmation in 3 sources
- Glesinger NOT same as Foresta — separate clarification card
- Theodor Herzl voyage details (Sète 2 April 1947, 2641 passengers, 3 killed)
- JDC Cyprus name index — most actionable database
- Wahl-Katzenellenbogen ancestry — Saul Wahl 1541-1617
- Haifa Chevra Kadisha leads
- Two new places: Tarnobrzeg, Padua
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE_PATH = REPO / 'platform' / 'data' / 'people.json'
PLACES_PATH = REPO / 'platform' / 'data' / 'places.json'
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'

# ============================================================
# 1. PEOPLE.JSON updates
# ============================================================
pdata = json.loads(PEOPLE_PATH.read_text(encoding='utf-8'))
people = pdata['people']
by_id = {p['id']: p for p in people}

SRC_GELLES = "src_gelles_griffel_nadworna_pdf"
SRC_ERIC_ADST = "src_eric_griffel_adst_oral_history_2015"
SRC_PINKAS = "src_pinkas_hakehillot_nadwirna"
SRC_JGB = "src_jewish_galicia_bukovina"
SRC_WIKIPEDIA = "src_wikipedia"
SRC_YAD_VASHEM = "src_yad_vashem"

# Correction: Chanan Rapaport DECEASED 2022-01-02
chanan = by_id.get('p_dr_chanan_rapaport_living')
if chanan:
    chanan['id'] = 'p_dr_chanan_rapaport'
    chanan['role'] = 'rapaport_genealogist_deceased'
    chanan['birth'] = {
        "date": "1928-09-08", "date_precision": "day", "place_id": "pl_stanislawow",
        "confidence": "documented", "sources": ["src_nli_authority_record"]
    }
    chanan['death'] = {
        "date": "2022-01-02", "date_precision": "day",
        "confidence": "documented", "sources": ["src_nli_authority_record"]
    }
    chanan['note_en'] = (
        "Dr Chanan Rapaport (1928-09-08 Stanisławów, Poland – 2022-01-02 Israel). Director General of "
        "The Center for the Study of the Rapaport Family (founded 1990); board member of the "
        "International Institute for Jewish Genealogy at the National Library Jerusalem. Born in "
        "Stanisławów — same Galician region as Nadwórna (~50 km away). Commander in the Haganah "
        "Underground and IDF. Scientific Director of the Szold Institute 1965-1982. Adviser to PMs "
        "Golda Meir and Yitzhak Rabin. Author of the foundational 2018 paper establishing the Sephardic "
        "origin of the Rapaport family. THE leading authority on Rapaport family genealogy until his death."
    )

# Correction: Diana Griffel deceased mid-1960s
diana = by_id.get('p_diana_griffel_living')
if diana:
    diana['id'] = 'p_diana_griffel'
    diana['role'] = 'first_cousin_deceased'
    diana['death'] = {
        "date": "1965", "date_precision": "year_approx",
        "confidence": "documented", "sources": [SRC_ERIC_ADST],
        "note_en": "Died of cancer in mid-sixties per Eric Griffel's 2015 ADST oral history."
    }
    diana['note_en'] = (
        "Diana Margaret Griffel (born London 27 October 1943, died mid-1960s of cancer). Daughter of "
        "Edward Griffel + Susan Manson. 2nd cousin of David Memek. Confirmed deceased in her brother "
        "Eric Griffel's 2015 ADST oral history."
    )

def new_p(pid, **kw):
    return {"id": pid, "primary_name": {}, "aliases": [], "facts": [], **kw}

new_ancestors = []

# Tzvi Hirsh Filip of Nadwórna (1737-1802) — founding Hasidic rabbi
filip = new_p(
    "p_tzvi_hirsh_filip_nadwirna",
    primary_name={
        "en": "R. Tzvi Hirsh Filip of Nadworna",
        "he": "ר' צבי הירש פיליפ מנדבורנה",
        "pl": "Rabbi Tzvi Hirsh Filip z Nadwórnej",
        "fr": "R. Tzvi Hirsh Filip de Nadworna"
    },
    birth={"date": "1737", "date_precision": "year", "place_id": "pl_nadworna",
           "confidence": "documented", "sources": [SRC_JGB]},
    death={"date": "1802", "date_precision": "year", "place_id": "pl_nadworna",
           "confidence": "documented", "sources": [SRC_JGB]},
    role="rabbinic_context_ancestor",
    note_en=(
        "Founding Hasidic rabbi of Nadwórna. From ~1786 served as Maggid Meisharim and Hasidic Rebbe. "
        "Father: Shalom Zelig. Author of important rabbinical works: Tsemah Hashem Le-tsvi, Siftei "
        "Kdoshim, Mili De-Avot. His pupil was R. Menachem Mendel of Kosov (founder of the Kosov "
        "Dynasty, parent of the Vizhnitz dynasty whose Ottynia branch Eliezer Griffel and Berisz "
        "Rapaport followed). Succeeded by his son David Arie Leib Filip and son-in-law R. Yitshak of "
        "Radzivil (son of the Maggid of Zlochev). Documented in Jewish Galicia & Bukovina person record; "
        "cited in Wunder's Meorei Galicia 4:40."
    )
)
new_ancestors.append(filip)

# Reb Chaim Hager of Ottynia (1863-1931)
chaim_hager = new_p(
    "p_chaim_hager_ottynia",
    primary_name={
        "en": "Reb Chaim Hager of Ottynia",
        "he": "הרב חיים הגר מאוטיניה",
        "pl": "Rabbi Chaim Hager z Otynia",
        "fr": "R. Chaim Hager d'Otynia"
    },
    birth={"date": "1863", "date_precision": "year", "place_id": "pl_kosov",
           "confidence": "documented", "sources": [SRC_WIKIPEDIA]},
    death={"date": "1931", "date_precision": "year", "place_id": "pl_ottynia",
           "confidence": "documented", "sources": [SRC_WIKIPEDIA]},
    role="rabbinic_context_ancestor",
    note_en=(
        "Reb Chaim Hager of Ottynia (1863-1931), author of 'Tal Chaim'. Son of Menachem Mendel Hager "
        "(1830-1884), founder of the Vizhnitz Hasidic dynasty. Reb Chaim was the Ottynia branch rebbe. "
        "Eliezer 'Zeida' Griffel and his sons + sons-in-law (including Berisz Rapaport) prayed at "
        "Reb Chaim's Ottynia synagogue. The Nadwórna Hasidic kloiz list confirmed in Pinkas Hakehillot "
        "Polin includes Ottynia: 'Hassidim of Kosow, Wiznitz, Czortkow, Ottynia and Belz.'"
    )
)
new_ancestors.append(chaim_hager)

# Wahl-Katzenellenbogen line for Chawa Wahl
ancestor_chain = [
    ("p_meir_katzenellenbogen_padua",
     {"en": "R. Meir Katzenellenbogen 'MaHaRaM Padua'",
      "he": "ר' מאיר קצנלנבוגן 'מהר\"ם פדואה'",
      "pl": "Rabbi Meir Katzenellenbogen z Padwy",
      "fr": "R. Meir Katzenellenbogen de Padoue"},
     "c.1482", "1565-01-12", "pl_padua",
     ("Chief Rabbi of Padua. Born in Katzenelnbogen, Germany. Mother Julia-Malka Luria "
      "descended from Rashi via daughter Miriam. Studied under Jacob Pollak in Prague. Married "
      "Hannah, granddaughter of Judah Minz. Succeeded father-in-law Abraham Minz in the chief "
      "rabbinate of Padua. Author of 'She'elot u-Teshuvot Maharam Padua'. Founder of the "
      "Katzenellenbogen rabbinical dynasty.")),
    ("p_samuel_judah_katzenellenbogen",
     {"en": "R. Samuel Judah Katzenellenbogen",
      "he": "ר' שמואל יהודה קצנלנבוגן",
      "pl": "Rabbi Samuel Judah Katzenellenbogen",
      "fr": "R. Samuel Judah Katzenellenbogen"},
     "1521", "1597-03-25", "pl_padua",
     ("Italian rabbi born in Padua 1521. Chief Rabbi of Venice from 1565. Twelve of his "
      "derashot published in Venice 1594. Father of Saul Wahl. Died 25 March 1597. According to "
      "the Jewish Encyclopedia: 'received Prince Radziwill with marked respect and treated him "
      "very kindly. The rabbi gave the prince a picture of his son Saul, who years before had "
      "left for Poland.'")),
    ("p_saul_wahl_katzenellenbogen",
     {"en": "Saul Wahl Katzenellenbogen",
      "he": "שאול ואהל קצנלנבוגן",
      "pl": "Saul Wahl Katzenellenbogen",
      "fr": "Saul Wahl Katzenellenbogen"},
     "1541", "1617", "pl_brest",
     ("Polish-Jewish merchant. Married Deborah Rivkah Drucker. According to Jewish legend "
      "served as 'rex pro tempore' of Poland on 18 August 1587 between Stefan Báthory's death "
      "and Sigismund III Vasa's election (some traditions say one night, others a few days). "
      "The surname 'Wahl' comes from German 'wahl' = election. 13 children. Y-DNA-confirmed "
      "ancestor of multiple modern descendants including our cousin Edward Gelles (via Chawa Wahl).")),
    ("p_meir_wahl_maharash",
     {"en": "R. Meir Wahl Katzenellenbogen 'MaHaRaSH'",
      "he": "ר' מאיר ואהל קצנלנבוגן 'מהר\"ש'",
      "pl": "Rabbi Meir Wahl",
      "fr": "R. Meir Wahl"},
     "c.1565", "1631", "pl_brest",
     ("ABD (Av Beit Din) of Brest, Lithuania. Married Hinde, daughter of Pinchas Halevi Horowitz "
      "of Cracow. This is the documented bridge from the Lithuanian Wahls into the Galician "
      "Horowitz orbit. Son of Saul Wahl. From him descends the Galician Wahl line reaching "
      "Tarnobrzeg and (via Chawa) our family.")),
    ("p_shulim_wahl_tarnobrzeg",
     {"en": "Shulim Wahl of Tarnobrzeg",
      "he": "שולים ואהל מטרנוברז'ג",
      "pl": "Szulim Wahl z Tarnobrzega",
      "fr": "Shulim Wahl de Tarnobrzeg"},
     None, None, "pl_tarnobrzeg",
     ("Father of Chawa Wahl (1877-1941). Galician Wahl line carrying documented descent from Saul "
      "Wahl Katzenellenbogen. Married Sarah Safier of Tarnobrzeg. Documented in Edward Gelles's "
      "'WAHL of Tarnobrzeg and WOHL of Cracow' (Balliol College Oxford archives).")),
    ("p_sarah_safier_tarnobrzeg",
     {"en": "Sarah Wahl (née Safier) of Tarnobrzeg",
      "he": "שרה ואהל (לבית ספיר) מטרנוברז'ג",
      "pl": "Sara Wahl (z domu Safier) z Tarnobrzega",
      "fr": "Sarah Wahl (née Safier) de Tarnobrzeg"},
     None, None, "pl_tarnobrzeg",
     ("Mother of Chawa Wahl (1877-1941). Of the Safier family of Tarnobrzeg. Documented in Edward "
      "Gelles's 'WAHL of Tarnobrzeg and WOHL of Cracow' (Balliol).")),
]

for pid, name, b, d, place, note in ancestor_chain:
    p = new_p(pid, primary_name=name, role="rabbinical_dynasty_ancestor", note_en=note)
    if b:
        prec = "day" if "-" in b and len(b) > 7 else "circa" if b.startswith("c.") else "year"
        date = b[2:] if b.startswith("c.") else b
        p['birth'] = {"date": date, "date_precision": prec, "place_id": place,
                      "confidence": "documented", "sources": [SRC_WIKIPEDIA, SRC_GELLES]}
    if d:
        p['death'] = {"date": d, "date_precision": "day" if "-" in d and len(d) > 7 else "year",
                      "confidence": "documented", "sources": [SRC_WIKIPEDIA, SRC_GELLES]}
    new_ancestors.append(p)

# Wire up the Wahl chain parent-child relationships
by_id_after = {p['id']: p for p in people + new_ancestors}
by_id_after['p_meir_katzenellenbogen_padua']['children_ids'] = ['p_samuel_judah_katzenellenbogen']
by_id_after['p_samuel_judah_katzenellenbogen']['father_id'] = 'p_meir_katzenellenbogen_padua'
by_id_after['p_samuel_judah_katzenellenbogen']['children_ids'] = ['p_saul_wahl_katzenellenbogen']
by_id_after['p_saul_wahl_katzenellenbogen']['father_id'] = 'p_samuel_judah_katzenellenbogen'
by_id_after['p_saul_wahl_katzenellenbogen']['children_ids'] = ['p_meir_wahl_maharash']
by_id_after['p_meir_wahl_maharash']['father_id'] = 'p_saul_wahl_katzenellenbogen'
# Shulim & Sarah → Chawa
by_id_after['p_shulim_wahl_tarnobrzeg']['spouse_id'] = 'p_sarah_safier_tarnobrzeg'
by_id_after['p_sarah_safier_tarnobrzeg']['spouse_id'] = 'p_shulim_wahl_tarnobrzeg'
by_id_after['p_shulim_wahl_tarnobrzeg']['children_ids'] = ['p_chawa_wahl']
by_id_after['p_sarah_safier_tarnobrzeg']['children_ids'] = ['p_chawa_wahl']
# Chawa now has parents
chawa = by_id_after.get('p_chawa_wahl')
if chawa:
    chawa['father_id'] = 'p_shulim_wahl_tarnobrzeg'
    chawa['mother_id'] = 'p_sarah_safier_tarnobrzeg'
    chawa['facts'] = chawa.get('facts', []) + [
        {"key": "wahl_ancestry",
         "value": "Descendant of Saul Wahl Katzenellenbogen (1541-1617) via the Tarnobrzeg Wahl line, documented by Edward Gelles in 'WAHL of Tarnobrzeg and WOHL of Cracow' (Balliol). Y-DNA confirmed Avotaynu 2016.",
         "confidence": "documented", "sources": [SRC_GELLES]},
    ]

# Append all new ancestors
existing_ids = {p['id'] for p in people}
added = 0
for rec in new_ancestors:
    if rec['id'] not in existing_ids:
        people.append(rec)
        added += 1

PEOPLE_PATH.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] Added {added} new ancestors. Tree now {len(people)} people.")
print(f"[OK] Corrected: Dr Chanan Rapaport (deceased 2022-01-02), Diana Griffel (deceased mid-1960s).")

# ============================================================
# 2. PLACES.JSON updates
# ============================================================
placesdata = json.loads(PLACES_PATH.read_text(encoding='utf-8'))
NEW_PLACES = [
    {"id": "pl_padua",
     "names": {"en": "Padua, Italy", "he": "פדואה", "pl": "Padwa", "fr": "Padoue", "it": "Padova"},
     "coords": [45.4064, 11.8768],
     "era_context": {"15th_16th_century": "Major Renaissance Italian Jewish centre. Birthplace of R. Meir Katzenellenbogen 'MaHaRaM Padua' (1482-1565) and his son R. Samuel Judah Katzenellenbogen (1521-1597), founders of the Katzenellenbogen rabbinical dynasty that ultimately reached our family via Chawa Wahl.",
                     "now": "Comune in Veneto, Italy"},
     "note_en": "Where the Katzenellenbogen rabbinical dynasty was founded. MaHaRaM Padua served as Chief Rabbi of Padua until 1565."},
    {"id": "pl_brest",
     "names": {"en": "Brest (Brest-Litovsk)", "he": "בריסק (ברסט-ליטובסק)", "pl": "Brześć Litewski", "fr": "Brest", "be": "Брэст"},
     "coords": [52.0976, 23.7341],
     "era_context": {"16th_17th_century": "Major Polish-Lithuanian Jewish centre. Saul Wahl Katzenellenbogen and his son R. Meir Wahl 'MaHaRaSH' lived here.",
                     "now": "City in Belarus"},
     "note_en": "Home of Saul Wahl Katzenellenbogen (the legendary 'King for one night' of Poland) and his rabbinical descendants."},
    {"id": "pl_tarnobrzeg",
     "names": {"en": "Tarnobrzeg, Poland", "he": "טרנוברז'ג", "pl": "Tarnobrzeg", "fr": "Tarnobrzeg"},
     "coords": [50.5739, 21.6791],
     "era_context": {"19th_century": "Galician Jewish town. Birthplace of Shulim Wahl and Sarah Safier — Chawa Wahl Griffel's parents.",
                     "now": "Town in Subcarpathian Voivodeship, Poland"},
     "note_en": "Where Chawa Wahl (1877-1941), David Mendel Griffel's wife, was born — into the Tarnobrzeg Wahl line documented as descending from Saul Wahl Katzenellenbogen."},
    {"id": "pl_stanislawow",
     "names": {"en": "Stanisławów (now Ivano-Frankivsk)", "he": "סטניסלבוב", "pl": "Stanisławów", "fr": "Stanisławów", "uk": "Івано-Франківськ"},
     "coords": [48.9226, 24.7111],
     "era_context": {"1918_1939": "Regional capital of Stanisławów Voivodeship (containing Nadwórna).",
                     "now": "Ivano-Frankivsk, Ukraine"},
     "note_en": "Birthplace of Dr Chanan Rapaport (1928-2022), the Rapaport family genealogist. Regional capital of the voivodeship containing Nadwórna."},
    {"id": "pl_kosov",
     "names": {"en": "Kosov (Kosiv)", "he": "קוסוב", "pl": "Kosów", "fr": "Kosov", "uk": "Косів"},
     "coords": [48.3, 25.1],
     "era_context": {"19th_century": "Founding seat of the Kosov Hasidic dynasty.",
                     "now": "Kosiv, Ivano-Frankivsk Oblast, Ukraine"},
     "note_en": "Founding seat of the Hager Kosov-Vizhnitz Hasidic dynasty. Birthplace of Reb Chaim Hager of Ottynia (1863-1931)."},
    {"id": "pl_ottynia",
     "names": {"en": "Ottynia", "he": "אוטיניה", "pl": "Otynia", "fr": "Otynia", "uk": "Отинія"},
     "coords": [48.7367, 24.86],
     "era_context": {"19th_20th_century": "Seat of the Ottynia branch of the Hager Hasidic dynasty.",
                     "now": "Otynia, Ivano-Frankivsk Oblast, Ukraine"},
     "note_en": "Where Reb Chaim Hager (1863-1931) was rebbe. Eliezer Griffel and Berisz Rapaport prayed at the Ottynia kloiz."},
]
existing_place_ids = {p['id'] for p in placesdata['places']}
places_added = 0
for np in NEW_PLACES:
    if np['id'] not in existing_place_ids:
        placesdata['places'].append(np)
        places_added += 1
PLACES_PATH.write_text(json.dumps(placesdata, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] Added {places_added} new places. Total: {len(placesdata['places'])}.")

# ============================================================
# 3. RESEARCH_CENTER.JSON updates
# ============================================================
rc = json.loads(RC_PATH.read_text(encoding='utf-8'))

# Add Wahl-Katzenellenbogen as new section
wahl_section = {
    "id": "wahl_katzenellenbogen",
    "title_en": "👑 Wahl-Katzenellenbogen Ancestry (via Chawa Wahl)",
    "title_he": "👑 שושלת ואהל-קצנלנבוגן (דרך חוה ואהל)",
    "intro_en": (
        "Through the Griffel-Wahl marriage (David Mendel Griffel + Chawa Wahl ~1896), the documented "
        "Katzenellenbogen rabbinical dynasty of Padua-Venice entered the family tree. Chawa Wahl "
        "(1877-1941, perished Holocaust Nadwórna) was a direct descendant of Saul Wahl Katzenellenbogen "
        "(1541-1617) — the Polish-Jewish merchant whom legend remembers as 'King of Poland for one "
        "night' between Stefan Báthory's death and Sigismund III Vasa's election. This connection runs "
        "through the cousin line (Edward Gelles, Steven Lamm, Andrew Griffel, the Nirs, Pinhas Heyn, "
        "Boruch Griffel etc.) — all carry both the Chajes pedigree (David Memek's maternal grandmother) "
        "and Wahl-Katzenellenbogen pedigree (David Mendel Griffel's wife Chawa)."
    ),
    "cards": [
        {
            "id": "saul_wahl_king_for_a_night",
            "title_en": "Saul Wahl Katzenellenbogen (1541-1617) — 'King of Poland for one night'",
            "status": "confirmed",
            "summary_en": (
                "Polish-Jewish merchant. Married Deborah Rivkah Drucker (a relative of Moses Isserles). "
                "According to Jewish legend served as 'rex pro tempore' of Poland on 18 August 1587 "
                "between Stefan Báthory's death and Sigismund III Vasa's election. Some traditions say "
                "he ruled one night only; others a few days. The surname 'Wahl' comes from German "
                "'wahl' = 'election'. 13 children. Y-DNA-confirmed ancestor of multiple modern "
                "descendants including Edward Gelles."
            ),
            "source": "Wikipedia + Jewish Encyclopedia + Edward Gelles 'WAHL of Tarnobrzeg' (Balliol)",
            "urls": [
                "https://en.wikipedia.org/wiki/Saul_Wahl",
                "https://www.jewishencyclopedia.com/articles/14751-wahl-saul",
                "https://encyclopedia.yivo.org/article.aspx/Wahl_Shaul"
            ]
        },
        {
            "id": "katzenellenbogen_padua_venice",
            "title_en": "The Katzenellenbogen Padua-Venice dynasty (1482-1597)",
            "status": "confirmed",
            "summary_en": (
                "R. Meir Katzenellenbogen 'MaHaRaM Padua' (c.1482-1565) — Chief Rabbi of Padua; mother "
                "Julia-Malka Luria descended from Rashi via daughter Miriam; married Hannah granddaughter "
                "of Judah Minz. His son R. Samuel Judah Katzenellenbogen (1521-1597) became Chief Rabbi "
                "of Venice. Samuel's son was Saul Wahl. Three documented generations of Italian rabbinical "
                "leadership before the family moved into Polish-Lithuanian Jewry."
            ),
            "source": "Wikipedia + Jewish Encyclopedia",
            "urls": [
                "https://en.wikipedia.org/wiki/Meir_Katzenellenbogen",
                "https://en.wikipedia.org/wiki/Samuel_Judah_Katzenellenbogen"
            ]
        },
        {
            "id": "tarnobrzeg_wahl_to_chawa",
            "title_en": "Tarnobrzeg Wahls → Shulim Wahl → Chawa Wahl Griffel (1877-1941)",
            "status": "confirmed",
            "summary_en": (
                "The chain from Meir Wahl 'MaHaRaSH' (c.1565-1631, ABD Brest, m. Hinde Horowitz of Cracow) "
                "down through 17th-19th-century Galician Wahl/Wohl families in Cracow + Tarnobrzeg → "
                "Shulim Wahl + Sarah Safier of Tarnobrzeg → Chawa Wahl (1877-1941) who married David "
                "Mendel Griffel of Nadwórna in ~1896. Children: Zygmunt (1897-1951), Regina (1900-1954, "
                "mother of Edward Gelles), Edward (1904-1959). Documented by Edward Gelles in 'WAHL of "
                "Tarnobrzeg and WOHL of Cracow' (Balliol)."
            ),
            "source": "Edward Gelles, 'WAHL of Tarnobrzeg and WOHL of Cracow' (Balliol College Oxford archives)",
            "urls": [
                "https://archives.balliol.ox.ac.uk/Modern%20Papers/gelles/WAHL%20of%20Tarnobrzeg%20and%20WOHL%20of%20Cracow.pdf",
                "https://archives.balliol.ox.ac.uk/Modern%20Papers/gelles/GellesWahlDescent.pdf"
            ]
        },
        {
            "id": "ydna_katzenellenbogen_avotaynu",
            "title_en": "🧬 Y-DNA confirmation — Katzenellenbogen rabbinical lineage (Avotaynu 2016)",
            "status": "confirmed",
            "summary_en": (
                "Avotaynu Online published 'The Y-DNA Genetic Signature and Ethnic Origin of the "
                "Katzenellenbogen Rabbinical Lineage' (2016). Confirms the Saul Wahl line has documented "
                "Y-DNA. Edward Gelles tested his own DNA — the result connects him to both the Wahl-"
                "Katzenellenbogen line and Sephardic Benveniste descendants."
            ),
            "source": "Avotaynu Online 2016",
            "urls": ["https://avotaynuonline.com/2016/03/y-dna-genetic-signature-ethnic-origin-katzenellenbogen-rabbinical-lineage/"]
        }
    ]
}
rc['sections'].insert(4, wahl_section)  # After rabbinical_pedigree

# Add new headline finds
hf = next(s for s in rc['sections'] if s['id'] == 'headline_finds')

# Eric Griffel ADST card
hf['cards'].append({
    "id": "eric_griffel_adst_oral_history",
    "title_en": "📜 Eric Griffel ADST Oral History (2015) confirms Griffel-Nadwórna timber dynasty",
    "title_he": "📜 היסטוריה בעל-פה של אריק גריפל (2015) — מאשרת את שושלת העץ של משפחת גריפל מנדבורנה",
    "status": "confirmed",
    "summary_en": (
        "Eric Griffel (1930 Krakow – 2020 Rockville MD), David Memek Rapaport's first cousin, gave a "
        "205-page oral history to ADST (Association for Diplomatic Studies and Training) in 2015. "
        "He directly confirms: (a) his father Zygmunt Griffel was born near Nadwórna and is buried "
        "on Staten Island in the Nadwórna Jewish émigré community organization plot; (b) Zygmunt's "
        "timber business — developing tracts of forest and exporting product mainly to England; "
        "(c) his uncle Edward Griffel set up business in England before WWII; (d) Eric's mother "
        "Maryla née Susser was from a Krakow rabbinical-banking-jewelry family. Holocaust loss "
        "anchor: 'Maryla's mother and sister were shot by the Nazis in our apartment in Lwów.' "
        "Post-war Polish Government claims: 'three houses in Krakow and an interest in a bank on "
        "the central square in Krakow.' Zygmunt also had German reparation claims for 'confiscation "
        "of specialized timber in Poland.'"
    ),
    "source": "Eric Griffel, ADST Oral History 'A Non-Forgiving Life', 2015. PDF cached locally at docs/research/family_documents/eric_griffel_adst_oral_history_2015.pdf",
    "urls": ["https://adst.org/OH%20TOCs/Griffel.Eric.pdf"]
})

# Achwa Hachshara card
hf['cards'].append({
    "id": "achwa_beitar_hachshara",
    "title_en": "🏕️ The Nadwórna Beitar hachshara was called 'Kibbutz Achwa' (אחווה / fraternity)",
    "title_he": "🏕️ הכשרת בית\"ר הראשונה בפולין נקראה 'קיבוץ אחווה' בנדבורנה",
    "status": "confirmed",
    "summary_en": (
        "Yad Vashem photo archive 9933470 — a 1936 photograph of Leksio Hoffmann at 'Achwa' Hachshara "
        "Kibbutz in Nadwórna — confirms the kibbutz name. Dedication on back: 'as eternal souvenir "
        "from our short stay in the Kibbutz, from me, Leksio Hoffmann, Nadworna, August 9, 1936.' "
        "The 1929-founded first Polish Beitar hachshara was still operating in August 1936 as "
        "'Kibbutz Achwa'. David Rapaport was 17-18 in 1929 (founding year) and 24-25 in 1936 — "
        "very likely appears in any Achwa group photograph."
    ),
    "source": "Yad Vashem photo archive 9933470",
    "urls": ["https://collections.yadvashem.org/en/photos/9933470"]
})

# Theodor Herzl voyage details
hf['cards'].append({
    "id": "theodor_herzl_voyage_details",
    "title_en": "🚢 Theodor Herzl voyage details — Sète 2 April 1947, 2,641 passengers, 3 killed",
    "status": "confirmed",
    "summary_en": (
        "Confirmed via Palmach/Palyam ship history: Sailed from Sète, France, on 2 April 1947 "
        "carrying 2,641 Ma'apilim drawn from camps in France and Belgium. Commander Mecca Limon; "
        "officers Yosh Halvei, Betzalel 'Tzolo' Feldman, Chaim Wineshelboim; Gideoni Nachman 'Bob' "
        "Burstein. Intercepted 13 April 1947 by HMS Haydon and HMS St Brides Bay. Three Ma'apilim "
        "killed by British gunfire: Aharon Dov, Pinchas Weiss, Menachem Samet. 27 wounded. "
        "Passengers sent to Cyprus detention camps (Karaolos near Famagusta) for 8 months. "
        "Note: William Bernstein, sometimes confused with the Herzl, was killed on the SS Exodus "
        "— NOT the Theodor Herzl."
    ),
    "quote_en": "On 13 April 1947, the Theodor Herzl (2,641 passengers) was intercepted by HMS Haydon and HMS St Brides Bay. Passengers resisted heavily; three were killed and 27 were injured.",
    "source": "Palmach/Palyam — 'The Voyage of the Theodor Herzl'",
    "urls": ["https://www.palyam.org/English/Hahapala/hf/hf_Theodor_Herzl.pdf"]
})

# JDC Cyprus name index card
ndocs = next(s for s in rc['sections'] if s['id'] == 'next_documents')
ndocs['cards'].insert(0, {
    "id": "jdc_cyprus_name_index",
    "title_en": "🎯 JDC Cyprus name index — single most actionable database (16,667 pages indexed)",
    "title_he": "🎯 אינדקס שמות JDC קפריסין — המסד הזמין ביותר לפעולה",
    "status": "lead",
    "summary_en": (
        "The Joint Distribution Committee (JDC) Cyprus Collection is the single most actionable "
        "online database for finding our family. It consists of 16,667 pages of textual files "
        "digitized from 19 microfilm reels. Quote from JDC topic guide: 'births to Cyprus detainees "
        "from 1948-1949 are documented, and there are indexed lists that reveal genealogical "
        "information such as names, age, date of birth, place of birth, nationality, group "
        "affiliation, family status, and even weight.' A family of three with David b.1911-12-25, "
        "Lusia b.1913-04-08, Shimon b.1937-06-22 should be locatable via DOB cross-match alone."
    ),
    "source": "JDC Archives",
    "urls": [
        "https://archives.jdc.org/topic-guides/detained-in-cyprus/",
        "https://archives.jdc.org/project/cyprus-detention-camps/"
    ]
})

# Haifa Chevra Kadisha leads
ndocs['cards'].insert(1, {
    "id": "haifa_chevra_kadisha_david_rapaport",
    "title_en": "🎯 Haifa Chevra Kadisha — 2 entries for 'דוד רפפורט' may include David Memek",
    "title_he": "🎯 חברה קדישא חיפה — 2 רישומים ל'דוד רפפורט', אולי דוד ממק",
    "status": "lead",
    "summary_en": (
        "The Haifa Chevra Kadisha (Jewish burial society) has indexable entries for at least two "
        "'דוד רפפורט'. Their entries typically list Hebrew date of death + birth year + parents' "
        "names — the single most likely place to nail David Memek's exact death date. The two "
        "URLs to check manually: deceased ID 10700 (memorial info page) + deceased ID 148324 "
        "(funeral info page)."
    ),
    "source": "Haifa Chevra Kadisha (kdh.org.il)",
    "urls": [
        "https://kdh.org.il/memorial-info-dates-full/memorial-info-expanded/?deceased=10700",
        "http://kdh.org.il/funeral-info-dates-full/funeral-info-expanded/?deceased=148324"
    ]
})

# Foresta confirmation card
ndocs['cards'].append({
    "id": "foresta_company_verified",
    "title_en": "🌲 Foresta company — David Memek's wartime sawmill (Jewish-owned + Aryanised 1941)",
    "status": "confirmed",
    "summary_en": (
        "Foresta is confirmed in three independent sources (Yad Vashem, Pinkas Hakehillot Polin, "
        "Jewish Galicia & Bukovina) as the Jewish-owned, Jewish-managed Nadwórna timber operation. "
        "Leased state woodlands from the Polish authorities, exported timber. Contract cancelled "
        "1937 under antisemitic pressure. Nationalised by Soviets after September 1939 — Jews "
        "retained managerial positions. Under German occupation 1941-42, approximately 600 Jews "
        "worked daily at the sawmill (= Foresta) to obtain 'essential worker' permits. David Memek "
        "Rapaport's wartime work permit was for this operation. Owners' individual names are NOT "
        "on the public web — they're in the full Hebrew Pinkas Hakehillot Polin text and likely "
        "in the 1975 Carmi Nadwórna Yizkor book."
    ),
    "source": "Yad Vashem + Pinkas Polin + JGB",
    "urls": [
        "https://www.yadvashem.org/communities/nadworna/before-holocaust.html",
        "https://www.yadvashem.org/communities/nadworna/german-occupation.html",
        "https://www.jewishgen.org/yizkor/pinkas_poland/pol2_00328.html"
    ]
})

# Save
RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] Research Center now {len(rc['sections'])} sections, {sum(len(s['cards']) for s in rc['sections'])} cards.")
print("[OK] Wahl-Katzenellenbogen section added; Eric Griffel, Achwa, Theodor Herzl, JDC, Haifa Kadisha, Foresta cards added.")
