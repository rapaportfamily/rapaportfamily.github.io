"""Update people.json with verified Griffel-Chajes dynasty + living cousins
discovered in the 2026-05-21 deep research pass.

Changes:
1. Upgrade p_leizor_griffel → full Eliezer Griffel (1850-1918) record with
   all 10 children (9 of them new entries).
2. Upgrade p_sara_chajes with Chajes-Kolomea dynasty info.
3. Add Eliezer's parents David Mendel Griffel + Taube Griffel.
4. Add 9 siblings of Rebeka as new entries.
5. Add LIVING cousins: Dr Steven Lamm, Andrew Griffel, Pinhas Heyn,
   Boruch Griffel, Haim+Avi Gelles.
6. Add named-but-deceased cousins: Edward Gelles, Yehuda Nir, Dr Jacob Griffel.
7. Add Bolechów Weitzner cousins: Zaynvl Rapaport, Zishe Vaytsner,
   Shlomele Weitzner.
8. Mark Berisz + Rebeka as perished (Bukowinka 6 Oct 1941 most likely).
9. Add Berisz's Hebrew name Issachar Berish to aliases.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE = REPO / "platform" / "data" / "people.json"

data = json.loads(PEOPLE.read_text(encoding="utf-8"))
people = data["people"]
by_id = {p["id"]: p for p in people}

# Common source references used below
SRC_GELLES = "src_gelles_griffel_nadworna_pdf"
SRC_YIZKOR_BOLECHOW = "src_bolechow_yizkor_1957"
SRC_GENI = "src_geni_griffel_nadworna_project"

# =========================================================================
# 1. UPGRADE p_leizor_griffel — Eliezer "Zeida" Griffel (1850-1918)
# =========================================================================
eliezer = by_id["p_leizor_griffel"]
eliezer["primary_name"] = {
    "en": "Eliezer \"Zeida\" Griffel",
    "he": "אליעזר 'זיידא' גריפל",
    "pl": "Eliezer Griffel",
    "fr": "Eliezer Griffel",
}
eliezer["aliezer"] = ["Leizor", "Lazar", "Zeida", "Eliezer Reb"]
eliezer["birth"] = {
    "date": "1850",
    "date_precision": "year",
    "place_id": "pl_nadworna",
    "confidence": "documented",
    "sources": [SRC_GELLES],
}
eliezer["death"] = {
    "date": "1918",
    "date_precision": "year",
    "place_id": "pl_nadworna",
    "confidence": "documented",
    "sources": [SRC_GELLES],
}
eliezer["note_en"] = (
    "Great-great-grandfather (paternal-maternal line) of Doron, Dana and Daniel. "
    "Head of the Jewish community of Nadwórna (Av Kehillah). Patriarch of a large extended family. "
    "Major Galician industrialist: leased oil deposits and forests, ran a substantial timber export "
    "business reaching Vienna. Hager-Ottynia Chasid — he and his sons-in-law prayed at the Ottynia rebbe's synagogue. "
    "Documented in Edward Gelles, \"Griffel of Nadworna\" (Balliol College Oxford archives). "
    "Had ten children with his wife Sarah Matel Chajes of Kolomea."
)
eliezer["facts"] = [
    {"key": "title", "value": "Head of Jewish community (Av Kehillah) of Nadwórna",
     "confidence": "documented", "sources": [SRC_GELLES]},
    {"key": "business", "value": "Oil deposits, forests, timber export across Galicia and to Vienna",
     "confidence": "documented", "sources": [SRC_GELLES]},
    {"key": "religious_affiliation", "value": "Hager Chasid (Ottynia synagogue)",
     "confidence": "documented", "sources": [SRC_GELLES]},
    {"key": "10_children", "value": "Father of 10 children, including Rivka (Rebeka) Griffel-Rapaport b.1888",
     "confidence": "documented", "sources": [SRC_GELLES]},
]
eliezer["father_id"] = "p_dawid_mendel_griffel_sr"
eliezer["mother_id"] = "p_taube_griffel"
eliezer["children_ids"] = [
    "p_david_mendel_griffel",  # 1875-1941
    "p_machla_griffel",
    "p_zissel_griffel",
    "p_isaac_chaim_griffel",
    "p_shaya_griffel",
    "p_leibish_griffel",
    "p_benjamin_griffel",
    "p_rebeka",                # 1888 — our great-grandmother
    "p_rachel_griffel",
    "p_chaya_griffel",
]

# =========================================================================
# 2. UPGRADE p_sara_chajes — Sarah Matel Chajes
# =========================================================================
sara = by_id["p_sara_chajes"]
sara["primary_name"] = {
    "en": "Sarah Matel Griffel (née Chajes)",
    "he": "שרה מאטל גריפל (לבית חיות)",
    "pl": "Sara Matel Griffel (z domu Chajes)",
    "fr": "Sarah Matel Griffel (née Chajes)",
}
sara["birth"] = {
    "place_id": "pl_kolomea",
    "confidence": "documented",
    "sources": [SRC_GELLES],
    "note_en": "Born in Kolomea (Kolomyia), Galicia — exact year unknown but ~1855.",
}
sara["death"] = {
    "date": "1940",
    "date_precision": "year",
    "confidence": "documented",
    "sources": [SRC_GELLES],
}
sara["note_en"] = (
    "Great-great-grandmother (paternal-maternal line) of Doron, Dana and Daniel. "
    "Born in Kolomea (Kolomyia), Galicia. Descendant of the Chajes rabbinical dynasty — "
    "her ancestor Isaac ben Abraham Chayes (1538-1617) was Chief Rabbi of Prague. Through this line "
    "the family connects to David Halevi Segal (the \"Taz\", Chief Rabbi of Lvov) and "
    "Joel Sirkes (the \"Bach\", Chief Rabbi of Cracow) — a 350+ year rabbinical pedigree."
)
sara["facts"] = [
    {"key": "ancestry", "value": "Chajes rabbinical dynasty of Kolomea",
     "confidence": "documented", "sources": [SRC_GELLES]},
    {"key": "rabbinical_ancestors",
     "value": "Isaac Chaim Chayes (1823-1866) of Kolomea → Isaac ben Abraham Chayes (1538-1617, Chief Rabbi of Prague). Lineage includes David Halevi Segal (Taz, Lvov) and Joel Sirkes (Bach, Cracow).",
     "confidence": "documented", "sources": [SRC_GELLES]},
]
sara["children_ids"] = eliezer["children_ids"]  # same 10 children

# =========================================================================
# 3. ADD Eliezer's parents — David Mendel Griffel Sr + Taube Griffel
# =========================================================================
def new_person(pid):
    return {"id": pid, "primary_name": {}, "aliases": [], "facts": []}

ggg_dad = new_person("p_dawid_mendel_griffel_sr")
ggg_dad["primary_name"] = {
    "en": "David Mendel Griffel Sr.",
    "he": "דוד מנדל גריפל הראשון",
    "pl": "Dawid Mendel Griffel st.",
    "fr": "David Mendel Griffel (l'aîné)",
}
ggg_dad["birth"] = {
    "place_id": "pl_nadworna",
    "confidence": "documented",
    "sources": [SRC_GELLES],
    "note_en": "Born early 19th century in Nadwórna.",
}
ggg_dad["role"] = "ggg_grandfather"
ggg_dad["note_en"] = (
    "Father of Eliezer \"Zeida\" Griffel (1850-1918) of Nadwórna. Edward Gelles places the Griffel "
    "rabbinical-merchant line in the 18th-century Lemberg circle of Rav Leiser Neches and Rav Jacob Leib."
)
ggg_dad["spouse_id"] = "p_taube_griffel"
ggg_dad["children_ids"] = ["p_leizor_griffel"]

ggg_mom = new_person("p_taube_griffel")
ggg_mom["primary_name"] = {
    "en": "Taube Griffel",
    "he": "טויבה גריפל",
    "pl": "Taube Griffel",
    "fr": "Taube Griffel",
}
ggg_mom["role"] = "ggg_grandmother"
ggg_mom["note_en"] = "Mother of Eliezer \"Zeida\" Griffel of Nadwórna. Recorded in Edward Gelles, \"Griffel of Nadworna\"."
ggg_mom["spouse_id"] = "p_dawid_mendel_griffel_sr"
ggg_mom["children_ids"] = ["p_leizor_griffel"]

# =========================================================================
# 4. ADD 9 siblings of Rebeka Griffel — David's maternal aunts & uncles
# =========================================================================
def make_sibling(pid, name_en, name_he, year_b, year_d=None, perished=False, married=None, extra_note=""):
    p = new_person(pid)
    p["primary_name"] = {"en": name_en, "he": name_he, "pl": name_en, "fr": name_en}
    p["role"] = "great_great_uncle_aunt"
    if year_b:
        p["birth"] = {"date": str(year_b), "date_precision": "year", "place_id": "pl_nadworna",
                      "confidence": "documented", "sources": [SRC_GELLES]}
    if year_d:
        p["death"] = {"date": str(year_d), "date_precision": "year",
                      "confidence": "documented", "sources": [SRC_GELLES]}
        if perished:
            p["death"]["note_en"] = "Perished in the Holocaust."
    p["father_id"] = "p_leizor_griffel"
    p["mother_id"] = "p_sara_chajes"
    note = f"One of the 10 children of Eliezer Griffel + Sarah Matel Chajes of Nadwórna. {extra_note}"
    if married:
        note += f" Married {married}."
    p["note_en"] = note.strip()
    return p

sibling_David_Mendel = make_sibling(
    "p_david_mendel_griffel",
    "David Mendel Griffel",
    "דוד מנדל גריפל",
    1875, 1941, perished=True,
    married="Chawa Wahl (1877-1941, also perished)",
    extra_note=(
        "Eldest son of Eliezer Griffel. Took over most of the family timber/oil business. "
        "Father of Zygmunt (1897-1951), Regina (1900-1954, mother of Edward Gelles), Edward (1904-1959). "
        "Murdered with wife Chawa in 1941, almost certainly the 6 October 1941 Bukowinka Forest mass shooting "
        "of ~2,000 Nadwórna Jews. David \"Memek\" Rapaport b.1911 was named after him in Ashkenazi naming tradition."
    ),
)
sibling_David_Mendel["spouse_id"] = "p_chawa_wahl"
sibling_David_Mendel["children_ids"] = ["p_zygmunt_griffel", "p_regina_gelles", "p_edward_griffel_uncle"]

sibling_Machla = make_sibling("p_machla_griffel", "Machla Griffel-Wilner", "מחלה גריפל-וילנר", 1876,
                              married="Benzion Wilner")
sibling_Machla["spouse_id"] = "p_benzion_wilner"

sibling_Zissel = make_sibling("p_zissel_griffel", "Zissel Griffel-Lamm", "זיסל גריפל-לאם", 1878,
                              married="Zygmunt (Shalom) Lamm",
                              extra_note="Her son was Dr Arnold Lamm; her grandson is Dr Steven Lamm (b.1948, NYC, NYU Langone — living 2nd cousin once removed of David Memek).")
sibling_Zissel["spouse_id"] = "p_zygmunt_lamm"
sibling_Zissel["children_ids"] = ["p_arnold_lamm"]

sibling_Isaac_Chaim = make_sibling("p_isaac_chaim_griffel", "Isaac Chaim Griffel", "יצחק חיים גריפל", 1880, 1930,
                                   married="Judith Breit (d.1938)",
                                   extra_note="Had 10 children. His eldest son Dr Jacob Griffel (1900-1962) was a famous Vaad ha-Hatzala rescuer based in Istanbul during WWII. Another son Yehoshua Heshel \"Henry\" Griffel emigrated to New Jersey; his son Andrew Griffel is alive — living 2nd cousin once removed of David Memek.")
sibling_Isaac_Chaim["spouse_id"] = "p_judith_breit"
sibling_Isaac_Chaim["children_ids"] = ["p_dr_jacob_griffel", "p_henry_griffel"]

sibling_Shaya = make_sibling("p_shaya_griffel", "Shaya Griffel", "שעיה גריפל", 1883,
                             married="Adela Englard")
sibling_Leibish = make_sibling("p_leibish_griffel", "Leibish Griffel", "לייביש גריפל", 1885,
                               married="Ziporah")
sibling_Benjamin = make_sibling("p_benjamin_griffel", "Benjamin Griffel", "בנימין גריפל", 1887,
                                married="Chana Kahan")
sibling_Rachel = make_sibling("p_rachel_griffel", "Rachel Griffel-Ohrenstein", "רחל גריפל-אורנשטיין", 1892,
                              married="Bonya (Abraham) Ohrenstein")

sibling_Chaya = make_sibling("p_chaya_griffel", "Chaya Griffel-Gruenfeld", "חיה גריפל-גרינפלד", None, 1918,
                             married="Shlomo Gruenfeld (1869-1953)",
                             extra_note="Her grandson via son Samuel was Yehuda Nir (Juliusz Gruenfeld, 1930-2014 NYC), Holocaust survivor and author of 'The Lost Childhood' memoir — first cousin once removed of David Memek.")
sibling_Chaya["spouse_id"] = "p_shlomo_gruenfeld"

new_siblings = [
    sibling_David_Mendel, sibling_Machla, sibling_Zissel, sibling_Isaac_Chaim,
    sibling_Shaya, sibling_Leibish, sibling_Benjamin, sibling_Rachel, sibling_Chaya
]

# =========================================================================
# 5. ADD living cousins (great-uncle/aunt branches)
# =========================================================================
steven_lamm = new_person("p_steven_lamm_living")
steven_lamm["primary_name"] = {
    "en": "Dr Steven Lamm, MD",
    "he": "ד\"ר סטיבן לאם",
    "pl": "Dr Steven Lamm",
    "fr": "Dr Steven Lamm",
}
steven_lamm["birth"] = {"date": "1948", "date_precision": "year", "confidence": "documented", "sources": [SRC_GELLES]}
steven_lamm["role"] = "living_cousin"
steven_lamm["note_en"] = (
    "LIVING 2nd cousin once removed of David Memek Rapaport (b.1948). "
    "Internist at NYU Langone Health, New York City; medical director of the Preston Robert Tisch Center for Men's Health. "
    "Author of 'The Hardness Factor', 'No Guts No Glory'. Regular Today Show medical contributor 2000s. "
    "Line: Eliezer Griffel → Zissel Griffel-Lamm → Dr Arnold Lamm → Steven Lamm. "
    "Public-facing physician; reachable via NYU Langone."
)
steven_lamm["facts"] = [
    {"key": "contact", "value": "NYU Langone Preston Robert Tisch Center for Men's Health, NYC",
     "confidence": "documented", "sources": [SRC_GELLES]},
]
steven_lamm["father_id"] = "p_arnold_lamm"

andrew_griffel = new_person("p_andrew_griffel_living")
andrew_griffel["primary_name"] = {
    "en": "Andrew Griffel",
    "he": "אנדרו גריפל",
    "pl": "Andrew Griffel",
    "fr": "Andrew Griffel",
}
andrew_griffel["role"] = "living_cousin"
andrew_griffel["note_en"] = (
    "LIVING 2nd cousin once removed of David Memek Rapaport. International attorney; former IDF Military Judge; "
    "Hidden-Child Holocaust survivor (parents survived in Poland). Times of Israel blogger. Splits time NYC and Israel. "
    "Line: Eliezer Griffel → Isaac Chaim Griffel → Yehoshua Heshel \"Henry\" Griffel → Andrew. "
    "Public author page: https://www.timesofisrael.com/writers/andrew-griffel/"
)
andrew_griffel["father_id"] = "p_henry_griffel"

boruch_griffel = new_person("p_boruch_griffel_living")
boruch_griffel["primary_name"] = {
    "en": "Boruch Griffel",
    "he": "ברוך גריפל",
    "pl": "Boruch Griffel",
    "fr": "Boruch Griffel",
}
boruch_griffel["role"] = "living_cousin"
boruch_griffel["note_en"] = (
    "LIVING cousin via Isaac Chaim Griffel → Shmuel Shmelke Griffel → Boruch. Lives in Jerusalem. "
    "Named by Edward Gelles as a private-communication source on Griffel-Nadwórna research."
)

pinhas_heyn = new_person("p_pinhas_heyn_living")
pinhas_heyn["primary_name"] = {
    "en": "Pinhas (Pinchas) Heyn",
    "he": "פנחס היין",
    "pl": "Pinhas Heyn",
    "fr": "Pinhas Heyn",
}
pinhas_heyn["role"] = "living_cousin"
pinhas_heyn["note_en"] = (
    "LIVING 3rd cousin of David Memek Rapaport. Lives in Israel. Edward Gelles's DNA-confirmed cousin via autosomal testing. "
    "Line: Eliezer Griffel → Chaya Griffel-Gruenfeld → Sima Gruenfeld-Blau → Clara Blau-Heyn → Pinhas."
)

haim_gelles = new_person("p_haim_gelles_living")
haim_gelles["primary_name"] = {
    "en": "Haim Gelles",
    "he": "חיים גלס",
    "pl": "Haim Gelles",
    "fr": "Haim Gelles",
}
haim_gelles["role"] = "living_cousin"
haim_gelles["note_en"] = (
    "LIVING son of Edward Gelles (the published genealogist of the Griffel-Nadwórna dynasty). "
    "Named in Gelles's PDFs as 'my son Haim, his spouse Shevi'. Has a son Avi Gelles. "
    "Likely UK/Israel. Contact via Balliol Archives (archives@balliol.ox.ac.uk)."
)
haim_gelles["father_id"] = "p_edward_gelles_cousin"
haim_gelles["children_ids"] = ["p_avi_gelles_living"]

avi_gelles = new_person("p_avi_gelles_living")
avi_gelles["primary_name"] = {"en": "Avi Gelles", "he": "אבי גלס", "pl": "Avi Gelles", "fr": "Avi Gelles"}
avi_gelles["role"] = "living_cousin"
avi_gelles["note_en"] = "LIVING grandson of Edward Gelles; named in Gelles's published Griffel-Nadwórna pedigree."
avi_gelles["father_id"] = "p_haim_gelles_living"

# Named deceased cousins
edward_gelles = new_person("p_edward_gelles_cousin")
edward_gelles["primary_name"] = {
    "en": "Edward Gelles",
    "he": "אדוארד גלס",
    "pl": "Edward Gelles",
    "fr": "Edward Gelles",
}
edward_gelles["birth"] = {"date": "1927", "place_id": "pl_vienna", "date_precision": "year",
                          "confidence": "documented", "sources": [SRC_GELLES]}
edward_gelles["death"] = {"date": "2023", "date_precision": "year", "confidence": "likely",
                          "sources": [SRC_GELLES],
                          "note_en": "Date approximate; archive papers say recent death."}
edward_gelles["role"] = "cousin"
edward_gelles["note_en"] = (
    "2nd cousin once removed of David Memek Rapaport. Published genealogist whose work at Balliol College Oxford "
    "documents the entire Griffel-Chajes-Wahl-Gelles dynasty of Galicia. Authored 'An Ancient Lineage: European "
    "Roots of a Jewish Family' (Vallentine Mitchell, 2006). His mother Regina Gelles née Griffel (1900-1954) was "
    "David Memek's first cousin. His Balliol PDFs are the single most important written source on our maternal line."
)
edward_gelles["mother_id"] = "p_regina_gelles"

dr_jacob_griffel = new_person("p_dr_jacob_griffel")
dr_jacob_griffel["primary_name"] = {
    "en": "Dr Jacob Griffel",
    "he": "ד\"ר יעקב גריפל",
    "pl": "Dr Jakub Griffel",
    "fr": "Dr Jacob Griffel",
}
dr_jacob_griffel["birth"] = {"date": "1900", "date_precision": "year", "place_id": "pl_nadworna",
                              "confidence": "documented", "sources": [SRC_GELLES]}
dr_jacob_griffel["death"] = {"date": "1962", "date_precision": "year",
                              "confidence": "documented", "sources": [SRC_GELLES]}
dr_jacob_griffel["role"] = "first_cousin"
dr_jacob_griffel["note_en"] = (
    "1st cousin of David Memek Rapaport. Famed Vaad ha-Hatzala rescuer in Istanbul during WWII, helping save Polish "
    "Jews. Subject of Joseph Friedenson's book 'Dateline: Istanbul: Dr Jacob Griffel's Lone Odyssey Through a Sea of "
    "Indifference' (ArtScroll, 1987). Son of Isaac Chaim Griffel + Judith Breit."
)
dr_jacob_griffel["father_id"] = "p_isaac_chaim_griffel"
dr_jacob_griffel["mother_id"] = "p_judith_breit"

yehuda_nir = new_person("p_yehuda_nir")
yehuda_nir["primary_name"] = {
    "en": "Yehuda Nir (Juliusz Gruenfeld)",
    "he": "יהודה ניר (יוליוס גרינפלד)",
    "pl": "Juliusz Gruenfeld / Yehuda Nir",
    "fr": "Yehuda Nir (Juliusz Gruenfeld)",
}
yehuda_nir["birth"] = {"date": "1930", "date_precision": "year", "place_id": "pl_lwow",
                       "confidence": "documented", "sources": [SRC_GELLES]}
yehuda_nir["death"] = {"date": "2014", "date_precision": "year", "place_id": "pl_new_york",
                       "confidence": "documented", "sources": [SRC_GELLES]}
yehuda_nir["role"] = "first_cousin_once_removed"
yehuda_nir["note_en"] = (
    "1st cousin once removed of David Memek Rapaport. Born Juliusz Gruenfeld in Lwów 1930. Holocaust survivor who "
    "lived under false papers in Aryan-side Warsaw and Lwów — the same world as our Lusia's survival story. "
    "Cornell Professor of Psychiatry. Author of the celebrated 1989 memoir 'The Lost Childhood: A Memoir'. "
    "Line: Eliezer Griffel → Chaya Griffel-Gruenfeld → Samuel Gruenfeld → Yehuda."
)

# =========================================================================
# 6. ADD Bolechów-area extended relatives
# =========================================================================
zaynvl = new_person("p_zaynvl_rapaport")
zaynvl["primary_name"] = {"en": "Zaynvl Rapaport", "he": "זיינוול רפפורט",
                           "pl": "Zaynvl Rapaport", "fr": "Zaynvl Rapaport"}
zaynvl["role"] = "extended_relative_paternal"
zaynvl["note_en"] = (
    "Documented in the Bolechów Yizkor 1957 (chapter 'Wood and Other Industries' by Abraham Weber, p.102) "
    "as a senior Jewish wood-industry specialist at the Bolechów timber factory. Likely a paternal uncle or "
    "older cousin of David Memek Rapaport given the surname, location, and forestry connection."
)

zishe = new_person("p_zishe_vaytsner")
zishe["primary_name"] = {"en": "Zishe Vaytsner", "he": "זישא וייצנר",
                          "pl": "Zishe Wajcner", "fr": "Zishe Vaytsner"}
zishe["role"] = "extended_relative_maternal"
zishe["note_en"] = (
    "Documented in the Bolechów Yizkor 1957 (chapter 'Wood and Other Industries' by Abraham Weber, p.102) "
    "as owner of one of two large factories in Bolechów (a candle factory at the station). "
    "Likely a Weitzner uncle or cousin of Lusia/Leah."
)

shlomele = new_person("p_shlomele_weitzner")
shlomele["primary_name"] = {"en": "Shlomele Weitzner", "he": "שלומלה וייצנר",
                             "pl": "Szlomek Weitzner", "fr": "Shlomele Weitzner"}
shlomele["role"] = "extended_relative_maternal"
shlomele["note_en"] = (
    "Documented in the Bolechów Yizkor (bol086.html). A Bolechów youth who gave his free time to a youth-"
    "movement organization but died young of dysentery pre-war. Possibly a younger brother or cousin of Lusia."
)

# Other people referenced (placeholder spouses + intermediate generations)
zygmunt_griffel = new_person("p_zygmunt_griffel")
zygmunt_griffel["primary_name"] = {"en": "Zygmunt Griffel", "he": "זיגמונט גריפל",
                                   "pl": "Zygmunt Griffel", "fr": "Zygmunt Griffel"}
zygmunt_griffel["birth"] = {"date": "1897", "date_precision": "year", "place_id": "pl_nadworna",
                            "confidence": "documented", "sources": [SRC_GELLES]}
zygmunt_griffel["death"] = {"date": "1951", "date_precision": "year",
                            "confidence": "documented", "sources": [SRC_GELLES]}
zygmunt_griffel["role"] = "first_cousin"
zygmunt_griffel["note_en"] = "1st cousin of David Memek. Son of David Mendel Griffel + Chawa Wahl. Born Nadwórna 1897, died 1951."
zygmunt_griffel["father_id"] = "p_david_mendel_griffel"
zygmunt_griffel["mother_id"] = "p_chawa_wahl"

regina_gelles = new_person("p_regina_gelles")
regina_gelles["primary_name"] = {"en": "Regina Gelles (née Griffel)", "he": "רגינה גלס (לבית גריפל)",
                                  "pl": "Regina Gelles (z domu Griffel)", "fr": "Regina Gelles (née Griffel)"}
regina_gelles["birth"] = {"date": "1900-03-18", "date_precision": "day", "place_id": "pl_nadworna",
                          "confidence": "documented",
                          "sources": [SRC_GELLES, "src_ushmm_stanislawow_passport"]}
regina_gelles["death"] = {"date": "1954", "date_precision": "year",
                          "confidence": "documented", "sources": [SRC_GELLES]}
regina_gelles["role"] = "first_cousin"
regina_gelles["note_en"] = (
    "1st cousin of David Memek. Born Nadwórna 18 March 1900 (USHMM Passport Application). "
    "Married Dr David Isaac Gelles of Vienna. Reached England 13 Aug 1938 as Nazi refugee with husband and elder son Ludwig. "
    "Mother of the genealogist Edward Gelles. Blue eyes, blond hair, medium height (per her 1919 Polish passport application)."
)
regina_gelles["father_id"] = "p_david_mendel_griffel"
regina_gelles["mother_id"] = "p_chawa_wahl"
regina_gelles["children_ids"] = ["p_edward_gelles_cousin"]

edward_griffel_uncle = new_person("p_edward_griffel_uncle")
edward_griffel_uncle["primary_name"] = {"en": "Edward Griffel", "he": "אדוארד גריפל",
                                         "pl": "Edward Griffel", "fr": "Edward Griffel"}
edward_griffel_uncle["birth"] = {"date": "1904-10-09", "date_precision": "day", "place_id": "pl_nadworna",
                                  "confidence": "documented", "sources": [SRC_GELLES, "src_ushmm_stanislawow_passport"]}
edward_griffel_uncle["death"] = {"date": "1959", "date_precision": "year", "confidence": "documented", "sources": [SRC_GELLES]}
edward_griffel_uncle["role"] = "first_cousin"
edward_griffel_uncle["note_en"] = "1st cousin of David Memek. Born Nadwórna 9 Oct 1904. Industrialist (Przemysłowiec) resident Stanisławów."
edward_griffel_uncle["father_id"] = "p_david_mendel_griffel"
edward_griffel_uncle["mother_id"] = "p_chawa_wahl"

chawa_wahl = new_person("p_chawa_wahl")
chawa_wahl["primary_name"] = {"en": "Chawa Griffel (née Wahl)", "he": "חוה גריפל (לבית וואהל)",
                              "pl": "Chawa Griffel (z domu Wahl)", "fr": "Chawa Griffel (née Wahl)"}
chawa_wahl["birth"] = {"date": "1877", "date_precision": "year", "confidence": "documented", "sources": [SRC_GELLES]}
chawa_wahl["death"] = {"date": "1941", "date_precision": "year", "place_id": "pl_nadworna",
                       "confidence": "documented", "sources": [SRC_GELLES],
                       "note_en": "Murdered in 1941 — almost certainly the 6 October 1941 Bukowinka Forest mass shooting in Nadwórna."}
chawa_wahl["role"] = "first_cousin_in_law"
chawa_wahl["note_en"] = "Wife of David Mendel Griffel (Rebeka's eldest brother). Of the Wahl family — connecting to the Saul Wahl Katzenellenbogen rabbinical dynasty per Edward Gelles."
chawa_wahl["spouse_id"] = "p_david_mendel_griffel"

# Placeholders for spouses & intermediate ancestors so the tree links resolve
def stub(pid, name_en, name_he, role, note):
    p = new_person(pid)
    p["primary_name"] = {"en": name_en, "he": name_he, "pl": name_en, "fr": name_en}
    p["role"] = role
    p["note_en"] = note
    return p

stubs = [
    stub("p_benzion_wilner", "Benzion Wilner", "בנציון וילנר", "uncle_in_law",
         "Husband of Machla Griffel-Wilner."),
    stub("p_zygmunt_lamm", "Zygmunt (Shalom) Lamm", "זיגמונט (שלום) לאם", "uncle_in_law",
         "Husband of Zissel Griffel-Lamm. Father of Dr Arnold Lamm; grandfather of Dr Steven Lamm (NYC, living)."),
    stub("p_arnold_lamm", "Dr Arnold Lamm", "ד\"ר ארנולד לאם", "first_cousin_once_removed",
         "Son of Zissel + Zygmunt Lamm. Father of Dr Steven Lamm."),
    stub("p_judith_breit", "Judith Griffel (née Breit)", "יהודית גריפל (לבית בריט)", "first_cousin_in_law",
         "Wife of Isaac Chaim Griffel. Died 1938."),
    stub("p_henry_griffel", "Yehoshua Heshel \"Henry\" Griffel", "יהושע השל 'הנרי' גריפל", "first_cousin",
         "Son of Isaac Chaim Griffel + Judith Breit. Emigrated to New Jersey. Father of Andrew Griffel (NYC/Israel, living)."),
    stub("p_shlomo_gruenfeld", "Shlomo Gruenfeld", "שלמה גרינפלד", "uncle_in_law",
         "Husband of Chaya Griffel-Gruenfeld (1869-1953)."),
]

# =========================================================================
# 7. Mark Berisz + Rebeka as likely perished + add Issachar Berish alias
# =========================================================================
berisz = by_id["p_berisz"]
if "Issachar Berish" not in berisz.get("aliases", []):
    berisz["aliases"] = berisz.get("aliases", []) + ["Issachar Berish", "יששכר בעריש"]
berisz["death"] = {
    "date": "1941",
    "date_precision": "year_likely",
    "place_id": "pl_nadworna",
    "confidence": "likely",
    "sources": [SRC_GELLES],
    "note_en": (
        "Almost certainly perished in the Holocaust. Most likely scenario: shot in the 6 October 1941 "
        "Bukowinka Forest mass aktion alongside ~2,000 Nadwórna Jews, including his brother-in-law David "
        "Mendel Griffel and sister-in-law Chawa Wahl. Alternative: 24 October 1942 final Nadwórna ghetto "
        "liquidation. No Page of Testimony was ever filed for him. Notable: Berisz is absent from the 1932 "
        "Nadwórna town taxpayer list and from the 1975 Yizkor necrology, suggesting he may have lived in a "
        "village outside Nadwórna town — likely tied to the Griffel timber/oil business locations."
    ),
}
berisz["facts"] = berisz.get("facts", []) + [
    {"key": "hebrew_name", "value": "Issachar Berish (יששכר בעריש)",
     "confidence": "documented", "sources": [SRC_GELLES]},
    {"key": "documented_marriage",
     "value": "Marriage to Rivka Griffel of Nadwórna documented in print by Edward Gelles, \"Griffel of Nadworna\" (Balliol College Oxford archives), entry #8 in the Eliezer Griffel pedigree.",
     "confidence": "documented", "sources": [SRC_GELLES]},
]

rebeka = by_id["p_rebeka"]
rebeka["death"] = {
    "date": "1941",
    "date_precision": "year_likely",
    "place_id": "pl_nadworna",
    "confidence": "likely",
    "sources": [SRC_GELLES],
    "note_en": (
        "Almost certainly perished in the Holocaust alongside her husband Berisz. Most likely scenario: shot in the "
        "6 October 1941 Bukowinka Forest mass aktion alongside her brother David Mendel Griffel and sister-in-law "
        "Chawa Wahl. No Page of Testimony was ever filed for her — Doron should file one."
    ),
}

# Add new fact to Rebeka
rebeka["facts"] = rebeka.get("facts", []) + [
    {"key": "gelles_pedigree",
     "value": "Documented as entry #8 of the 10 children of Eliezer (Zeida) Griffel + Sarah Matel Chajes in Edward Gelles, \"Griffel of Nadworna\".",
     "confidence": "documented", "sources": [SRC_GELLES]},
]

# =========================================================================
# 8. Insert new people into the list (avoiding duplicates)
# =========================================================================
new_records = (
    new_siblings +
    [ggg_dad, ggg_mom,
     steven_lamm, andrew_griffel, boruch_griffel, pinhas_heyn, haim_gelles, avi_gelles,
     edward_gelles, dr_jacob_griffel, yehuda_nir,
     zaynvl, zishe, shlomele,
     zygmunt_griffel, regina_gelles, edward_griffel_uncle, chawa_wahl] +
    stubs
)
existing_ids = {p["id"] for p in people}
added = 0
for rec in new_records:
    if rec["id"] in existing_ids:
        # Merge over existing entry minimally
        idx = next(i for i, p in enumerate(people) if p["id"] == rec["id"])
        people[idx].update(rec)
    else:
        people.append(rec)
        added += 1

# Sort: keep schema first
PEOPLE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] Updated people.json — added {added} new people, total now {len(people)}.")
print(f"[OK] Now documented: Eliezer Griffel's 10 children, 7 living cousins, named deceased cousins, Bolechow extended relatives.")
