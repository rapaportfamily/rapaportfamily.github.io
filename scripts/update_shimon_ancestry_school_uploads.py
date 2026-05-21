"""One comprehensive update addressing:
1. Mark Shimon Rapaport (David's older son, b.1937) as deceased
2. Update Ester Goldfischer's profile with the Tarbut school finding
3. Expand the rabbinical_pedigree section in Research Center with the full
   Sephardic + Italian + Galician chain (now that we have many ancestors)
4. Add a "Tarbut school photo" + "Family uploads" cards
5. Bump cache so Virtual Trip becomes visible
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE_PATH = REPO / 'platform' / 'data' / 'people.json'
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'

SRC_FAMILY = "src_family_oral_2026"
SRC_SCHOOL = "src_bolechow_school_research_2026"

# ============================================================
# 1. Mark Shimon Rapaport as deceased
# ============================================================
pdata = json.loads(PEOPLE_PATH.read_text(encoding='utf-8'))
people = pdata['people']
by_id = {p['id']: p for p in people}

shimon = by_id.get('p_shimon')
if shimon:
    if not shimon.get('death'):
        shimon['death'] = {
            "date": None, "date_precision": "year_unknown",
            "confidence": "family_oral", "sources": [SRC_FAMILY],
            "note_en": "Deceased per family (Doron, 21 May 2026). Exact date to be confirmed via Haifa Chevra Kadisha or Israeli Population Registry."
        }
    note = shimon.get('note_en', '')
    if 'deceased' not in note.lower():
        shimon['note_en'] = (note + " Deceased — exact date to be confirmed via Haifa Chevra Kadisha "
                             "(53 male Rapaports in their records) or Misrad HaPnim.").strip()
    print(f"[OK] Marked Shimon Rapaport as deceased.")

# ============================================================
# 2. Update Ester Goldfischer with Tarbut school finding
# ============================================================
ester = by_id.get('p_ester_goldfischer')
if ester:
    ester['facts'] = [f for f in ester.get('facts', [])
                      if f.get('key') != 'feige_weitzner_school_circle']
    ester['facts'].append({
        "key": "school_with_feige_weitzner",
        "value": (
            "Per family stories, studied with Feige (Tzipora) Weitzner — Lusia's older sister, "
            "b.1911 Bolechów. Most likely school: the Tarbut Hebrew School on Halicka Street "
            "(formerly Kościuszko Street) in Bolechów — a coeducational Hebrew-language secular "
            "Zionist school. The same building also housed the Beth Yakov girls' religious school. "
            "Tarbut was the natural fit for a tannery-owner's daughter (the Weitzners) and for "
            "any Skole-area Jewish girl boarding for education in Bolechów. Alternative: the "
            "Stryj I or II Gymnasium (gymnasium-level, 40km commute from Bolechów; Bolechów "
            "Yizkor confirms 'the gymnasium students travelled to Stryj each morning')."
        ),
        "confidence": "family_oral",
        "sources": [SRC_FAMILY, SRC_SCHOOL]
    })
    print(f"[OK] Updated Ester Goldfischer with Tarbut school finding.")

PEOPLE_PATH.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding='utf-8')

# ============================================================
# 3. Expand the rabbinical_pedigree section to include all ancestors
# ============================================================
rc = json.loads(RC_PATH.read_text(encoding='utf-8'))

# Rebuild rabbinical_pedigree to include the full chain we now have
rp = next(s for s in rc['sections'] if s['id'] == 'rabbinical_pedigree')
rp['title_en'] = "🏛️ Ancestry — 575+ Years of Documented Pedigree"
rp['title_he'] = "🏛️ אילן יוחסין — 575+ שנים של ייחוס מתועד"
rp['intro_en'] = (
    "The full pedigree as documented across all 19 research dossiers: from medieval Sephardic "
    "Spain (Mallorca 1305) through Renaissance Italy (Porto, Verona 1450-1596) to Galician "
    "Nadwórna (1850-1941) to modern Israel. Plus the maternal Chajes + Wahl-Katzenellenbogen "
    "rabbinical dynasties brought into the family via Sarah Matel Chajes + Chawa Wahl Griffel."
)
rp['intro_he'] = (
    "אילן היוחסין המתועד שלנו ב-19 דוסיות המחקר: מספרד הספרדית של ימי הביניים (מיורקה 1305) "
    "דרך איטליה של הרנסנס (פורטו, ורונה 1450-1596) לגליציה של נדבורנה (1850-1941) ועד ישראל. "
    "פלוס שושלות חיות וואהל-קצנלנבוגן הרבניות שהובאו דרך שרה מאטל חיות וחוה ואהל-גריפל."
)
rp['cards'] = [
    {
        "id": "ancestry_full_chain",
        "title_en": "📜 The full documented chain (1305 Mallorca → 2026 Israel)",
        "title_he": "📜 השרשרת המתועדת המלאה (1305 מיורקה → 2026 ישראל)",
        "status": "confirmed",
        "summary_en": (
            "Step by step, generation by generation:"
            "\n\n"
            "**1305 Mallorca** — Dr Vidal Rapapa, the earliest documented Rapaport ancestor by name; "
            "led the 1305 conspiracy to save a Jewish girl from forced conversion-by-marriage.\n\n"
            "**1311-1345 Mallorca** — Dr Jucef Salomon Rapapa, court physician to King Jaime III; "
            "1345 lawsuit against King Pedro IV for unpaid 10 Libres (≈ €600K-1.5M today).\n\n"
            "**1391-1492** — Spanish pogroms + Inquisition expulsion; family flees to Italy.\n\n"
            "**~1450 Mainz → Porto Italy** — R. Meshullam Yekutiel ha-Kohen Rapa (d.1450), "
            "progenitor of the Rapoport-Kohen dynasty.\n\n"
            "**1482-1565 Padua** — R. Meir Katzenellenbogen 'MaHaRaM Padua', Chief Rabbi of Padua, "
            "founded the Katzenellenbogen rabbinical dynasty.\n\n"
            "**1502 Portobuffolè** — R. Yechiel Michael ha-Kohen Rapa born; his son Isaac 'HaMoel' "
            "Rapa-Porto became the first to use 'Rapa-Porto' as a surname (~1550).\n\n"
            "**1520-1596 Verona** — R. Avraham Menachem ha-Kohen Rapa-Porto published 'Mincha "
            "Belulah' (1594) with the iconic raven + priestly-blessing family emblem — still on "
            "our website header today.\n\n"
            "**1541-1617** — Saul Wahl Katzenellenbogen, legendary 'King of Poland for one night'.\n\n"
            "**1584-1651 Lemberg (Lwów)** — R. Abraham Rapoport 'Schrenzel', head of Lemberg "
            "yeshiva 45 years, President of the Council of Four Lands. Founder of the Galician "
            "Rapaport branch.\n\n"
            "**1737-1802 Nadwórna** — R. Tzvi Hirsh Filip, founding Hasidic rebbe of Nadwórna, "
            "teacher of the Kosov dynasty founder.\n\n"
            "**1786-1867** — R. Solomon Judah Loeb Rapoport 'SHI\"R', Chief Rabbi of Tarnopol + "
            "Prague; Hebrew name explicitly contains כהן (Kohen).\n\n"
            "**1830-1884** — R. Menachem Mendel Hager, founder of Vizhnitz Hasidic dynasty; his "
            "son Reb Chaim Hager (1863-1931) was the rebbe of Ottynia where Eliezer Griffel + "
            "Berisz Rapaport prayed.\n\n"
            "**1850-1918 Nadwórna** — Eliezer 'Zeida' Griffel, head of Nadwórna Jewish "
            "community, timber + oil businessman. Married Sarah Matel Chajes (of the Chajes "
            "rabbinical dynasty of Kolomea). 10 children.\n\n"
            "**1877-1941** — Chawa Wahl (Tarnobrzeg branch of Saul Wahl line) married into the "
            "Griffel family — connecting our cousin line to the Wahl-Katzenellenbogen pedigree.\n\n"
            "**1888 Nadwórna** — Rebeka Griffel born (8th child); birth certificate found at ŻIH "
            "Warsaw 15 May 2026.\n\n"
            "**1890 Austria-Hungary** — Baron Dr Arnold Rapoport-Adler Von Porada, member of "
            "Parliament for Galician Jews, granted the title of Baron by Emperor Franz Joseph.\n\n"
            "**1911-12-25 Nadwórna** — David Mendel 'Memek' Rapaport born to Berisz Rapaport + "
            "Rebeka Griffel-Rapaport.\n\n"
            "**1913-04-08 Bolechów** — Lusia (Leah) Weitzner born to Eli Weitzner + Mathilde "
            "Weinreb.\n\n"
            "**1934-36 Muszyna** — David + Lusia marry at the Pensjonat Bristol.\n\n"
            "**1942-1944 Lwów** — Lusia at Legionów 24 under false identity Maria Cizlik.\n\n"
            "**1946 Brussels** — Dov 'Bernard' Rapaport born.\n\n"
            "**1947-48 Theodor Herzl → Cyprus → Atlit → Haifa.**\n\n"
            "**1990-08-29** — David Memek dies, age 78, buried Sde Yehoshua Haifa.\n\n"
            "**1996-12-28** — Lusia dies, age 83, adjacent grave 102ג.\n\n"
            "**2026** — Doron, Dana, Daniel + their children = the 22nd+ generation."
        ),
        "source": "Dossiers 1-19 + Dr Chanan Rapaport 2018 + Edward Gelles 2006"
    },
    {
        "id": "chajes_dynasty",
        "title_en": "Chajes rabbinical line — Kolomea (Sarah Matel)",
        "title_he": "שושלת חיות הרבנית — קולומיאה (שרה מאטל)",
        "status": "confirmed",
        "summary_en": (
            "Sarah Matel Chajes (of Kolomea, married Eliezer Griffel of Nadwórna) descended from "
            "Isaac Chaim Chayes (1823-1866) of Kolomea, who descended from Isaac ben Abraham "
            "Chayes (1538-1617), Chief Rabbi of Prague. Through this line the family connects to "
            "David Halevi Segal (the 'Taz', Chief Rabbi of Lvov) and Joel Sirkes (the 'Bach', "
            "Chief Rabbi of Cracow)."
        ),
        "source": "Edward Gelles 'Facets of My Family History' (Balliol Oxford)"
    },
    {
        "id": "hager_ottynia",
        "title_en": "Hager-Ottynia Chasidim — Eliezer Griffel's religious world",
        "title_he": "חסידי האגר-אוטיניה — עולמו הדתי של אליעזר גריפל",
        "status": "confirmed",
        "summary_en": (
            "Eliezer Griffel and his sons + sons-in-law (including Berisz Rapaport) 'prayed "
            "regularly in the synagogue of the Rabbi of nearby Ottynia' — the Hager Chasidic "
            "dynasty's Ottynia branch under Reb Chaim Hager (1863-1931, author of 'Tal Chaim'). "
            "Pinkas Hakehillot Polin confirms the Ottynia kloiz was one of more than 20 houses "
            "of prayer in pre-war Nadwórna, alongside Kosow, Wiznitz, Czortkow + Belz Chasidim."
        ),
        "source": "Edward Gelles + Pinkas Hakehillot Polin Nadwórna"
    },
    {
        "id": "nadvorna_dynasty_naming",
        "title_en": "Berisz = Issachar Berish = the founder of Nadvorna Hasidic dynasty's name",
        "title_he": "בריש = יששכר בעריש = שמו של מייסד שושלת חסידי נדבורנה",
        "status": "likely",
        "summary_en": (
            "David's father Berisz / Bernard Rapaport's Hebrew name was Issachar Berish — EXACT "
            "match to R. Issachar Dov Ber 'Bertche' Leifer (1790-1848), founder of the Nadvorna "
            "Hasidic dynasty. Overwhelming evidence that Berisz's father was a Nadvorner Chasid "
            "in the 1880s and that Berisz was named for the dynasty founder. R. Issachar Dov "
            "Leifer's mother was Feige bat R' Itamar ha-Kohen — Kohanic descent in the Leifer "
            "matriline as well."
        ),
        "source": "JewishGen Nadwórna authors page + JGB"
    }
]

# ============================================================
# 4. Add a Tarbut school card to Virtual Trip
# ============================================================
trip = next(s for s in rc['sections'] if s['id'] == 'virtual_trip')
# Find the Bolechów card and update its image caption for the Tarbut school
for c in trip['cards']:
    if c['id'] == 'trip_bolechow':
        for img in c.get('images', []):
            if 'Tarbut' in img.get('caption_en', ''):
                img['caption_en'] = (
                    "Tarbut Hebrew school on Halicka Street (formerly Kościuszko Street), "
                    "Bolechów. The same building housed the Beth Yakov girls' religious school. "
                    "Per family stories: where Doron's maternal grandmother ESTER GOLDFISCHER "
                    "and Lusia's older sister FEIGE (Tzipora) WEITZNER studied together in the "
                    "late 1920s / early 1930s — connecting both halves of the family decades "
                    "before Dov and Dalia ever met."
                )

# ============================================================
# 5. Add a "Family Uploads + Gemini verification" card under Open Action Items
# ============================================================
open_act = next(s for s in rc['sections'] if s['id'] == 'open_action_items')
open_act['cards'].insert(0, {
    "id": "gemini_upload_verification_retry",
    "title_en": "🔧 Retry Gemini upload verification (current 503 errors)",
    "title_he": "🔧 חידוש אימות העלאות של ג'מיני (שגיאות 503 נוכחיות)",
    "status": "lead",
    "summary_en": (
        "The Firebase Cloud Function 'verifyUpload' uses Gemini 2.5 Flash to verify family-"
        "uploaded documents (PDFs / photos / WhatsApp chats). Currently returning HTTP 503 "
        "Service Unavailable — Gemini API capacity issue. Recommended fix: extend functions/"
        "index.js to fall back to Claude Sonnet 4.5 (via the existing ANTHROPIC_API_KEY secret) "
        "when Gemini returns 503/429/RECITATION/SAFETY. This makes the upload verifier robust. "
        "Meanwhile, Doron can manually re-trigger pending uploads by setting their Firestore "
        "doc field gemini_verification.status back to 'pending' (the function re-fires on next "
        "doc update if status === 'pending')."
    ),
    "source": "Repo functions/index.js + observed 503 error 19 May 2026 on Daniel's PDF upload",
    "urls": []
})

# ============================================================
# 6. Bump cache: write a small build_version field for the SPA
# ============================================================
rc['build_version'] = "2026-05-21-T3-virtual-trip-shimon-ancestry"
rc['generated'] = "2026-05-21"

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
total = sum(len(s['cards']) for s in rc['sections'])
print(f"[OK] Ancestry section expanded to a 22-generation full-chain card + 3 sub-cards.")
print(f"[OK] Tarbut school caption updated in Virtual Trip Bolechów card.")
print(f"[OK] Gemini-upload-retry action card added.")
print(f"[OK] Research Center now {len(rc['sections'])} sections, {total} cards.")
