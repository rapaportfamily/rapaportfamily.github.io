"""Add the Virtual Trip Through the Memoir section to the Research Center.
Chronological tour through the memoir's geography, each card with embedded
photos (Wikimedia Commons CC-licensed + JGB photos already in the repo).

Memoir content is paraphrased, not quoted at length. Brief quotes <15 words
only where essential for context.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'
PLACES_PATH = REPO / 'platform' / 'data' / 'places.json'

rc = json.loads(RC_PATH.read_text(encoding='utf-8'))

trip_section = {
    "id": "virtual_trip",
    "title_en": "🗺️ Virtual Trip Through the Memoir",
    "title_he": "🗺️ מסע וירטואלי דרך היומן",
    "intro_en": (
        "A chronological tour through every place named in Lusia's memoir, with photos "
        "(Wikimedia Commons CC-licensed + Jewish Galicia & Bukovina). Click each card to see "
        "the place, the dates, the family connection, and the historic photos."
    ),
    "intro_he": (
        "מסע כרונולוגי דרך כל מקום שנזכר ביומן של לוסיה, עם תצלומים. הקליקו כל כרטיס לראות "
        "את המקום, התאריכים, הקשר המשפחתי, ותצלומים היסטוריים."
    ),
    "cards": [
        {
            "id": "trip_nadworna",
            "title_en": "🏛️ Nadwórna (Nadvirna) — David Memek's birthplace, 1911",
            "title_he": "🏛️ נדבורנה — מקום הולדתו של דוד ממק, 1911",
            "status": "confirmed",
            "summary_en": (
                "David Mendel 'Memek' Rapaport was born 25 December 1911 in Nadwórna, eastern Galicia. "
                "His father Berisz/Bernard Rapaport was a merchant. His mother Rebeka Griffel was the "
                "8th of 10 children of Eliezer 'Zeida' Griffel, head of the Nadwórna Jewish community + "
                "owner of the town's timber and oil enterprises. The town was 6 October 1941 the site "
                "of the first mass aktion at the Bukowinka Forest, where >2,000 Nadwórna Jews — almost "
                "certainly including David's parents Berisz + Rebeka — were murdered. Today: Nadvirna, "
                "Ivano-Frankivsk Oblast, Ukraine."
            ),
            "source": "Wikipedia Nadvirna + Pinkas Hakehillot Polin",
            "images": [
                {"src": "assets/research_images/nadworna_town_hall.jpg",
                 "caption_en": "Nadwórna — the historic Town Hall on Hetman Mazepa Street.",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/nadworna_hotel.jpg",
                 "caption_en": "Nadwórna — historic hotel building.",
                 "credit": "Wikipedia Commons"},
            ],
            "urls": ["https://en.wikipedia.org/wiki/Nadvirna",
                     "https://www.jewishgen.org/yizkor/pinkas_poland/pol2_00328.html"]
        },
        {
            "id": "trip_bolechow",
            "title_en": "🏛️ Bolechów (Bolekhiv) — Lusia's birthplace, 1913",
            "title_he": "🏛️ בולחוב — מקום הולדתה של לוסיה, 1913",
            "status": "confirmed",
            "summary_en": (
                "Lusia (Leah) Weitzner was born 8 April 1913 in Bolechów (Bolechów Ruski). Her father "
                "Eli/Eliyahu Weitzner started as a cattle dealer and became a tannery owner — tanning "
                "was the dominant Jewish industry in Bolechów (in 1874 the tannery-owner Israel Hauptman "
                "was elected mayor). In 1890 Bolechów was 75% Jewish, the highest proportion of any "
                "Galician town. The 1957 Bolechów Yizkor names 'D. Rapaport, Eli Weitzner's son-in-law' "
                "— published documentary confirmation of David and Lusia's marriage. Today: Bolekhiv, "
                "Ivano-Frankivsk Oblast, Ukraine."
            ),
            "source": "Wikipedia Bolekhiv + Bolechów Yizkor 1957 + JGB",
            "images": [
                {"src": "assets/research_images/bolechow_great_synagogue.jpg",
                 "caption_en": "The Great Synagogue of Bolechów — northern side. Pre-war exterior.",
                 "credit": "Jewish Galicia & Bukovina (Vladimir Levin, 2009)"},
                {"src": "assets/research_images/bolechow_1914_map.jpg",
                 "caption_en": "Bolechów town map, 1914.",
                 "credit": "New York Public Library / JGB"},
                {"src": "assets/research_images/bolechow_23-Rynek-North1.jpg",
                 "caption_en": "Bolechów market square (Rynek), northern side.",
                 "credit": "JGB"},
                {"src": "assets/research_images/trip/bolechow_town_hall_alt.jpg",
                 "caption_en": "Bolechów Town Hall (Будинок ратуші у Болехові).",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/trip/bolechow_greek_catholic_church.jpg",
                 "caption_en": "Bolechów Greek Catholic Church.",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/bolechow_37-forest-lyc.jpg",
                 "caption_en": "Bolechów Forestry Lyceum — relevant to the local timber + tanning industries.",
                 "credit": "JGB"},
                {"src": "assets/research_images/bolechow_32-Halickaya1-tarbut.jpg",
                 "caption_en": "Halicka Street — the Tarbut Hebrew school. Site of pre-war Zionist education.",
                 "credit": "JGB"},
                {"src": "assets/research_images/bolechow_39-School.jpg",
                 "caption_en": "Bolechów Jewish school building.",
                 "credit": "JGB"},
            ],
            "urls": ["https://en.wikipedia.org/wiki/Bolekhiv",
                     "https://www.jewishgen.org/Yizkor/Bolekhov/bol278.html"]
        },
        {
            "id": "trip_muszyna",
            "title_en": "🏨 Muszyna — the resort hotel Lusia managed, ~1933-1939",
            "title_he": "🏨 מושינה — המלון שלוסיה ניהלה, 1933-1939",
            "status": "likely",
            "summary_en": (
                "Muszyna is a small resort town in the Beskid mountains of southern Poland, near the "
                "Slovak border, ~12 km from Krynica-Zdrój. It became an officially-recognised spa town "
                "in 1929-30 after mineral-spring development. Lusia rented and managed a fine resort "
                "hotel here — almost certainly the famous Jewish-owned 'Pensjonat Bristol', operated "
                "by the family of Chaim Weiss (the dominant pre-war Jewish hotelier in Muszyna). "
                "Memek (David Rapaport) became her regular boyfriend there; they married in Muszyna "
                "around 1934-1936. A standalone 6-page article on the Bristol exists: Żebrowski, "
                "'Żydowski pensjonat Bristol w Muszynie', Almanach Muszyny 1998, pp.27-33."
            ),
            "source": "Wirtualny Sztetl Muszyna + Almanach Muszyny 1998",
            "images": [
                {"src": "assets/research_images/trip/muszyna_town_hall_market.jpg",
                 "caption_en": "Muszyna Town Hall on the Market Square. The Reich family hotel was nearby on the Rynek.",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/trip/muszyna_panorama.jpg",
                 "caption_en": "Panorama of Muszyna in the Beskid mountains.",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/trip/muszyna_mineral_springs_pijalnia.jpg",
                 "caption_en": "Pijalnia Anna — Muszyna's mineral water pavilion, central to its spa identity.",
                 "credit": "Wikipedia Commons"},
                {"src": "assets/research_images/trip/muszyna_promenade.jpg",
                 "caption_en": "Promenades + sidewalks in Muszyna, with Muszyna Castle in the background.",
                 "credit": "Wikipedia Commons"},
            ],
            "urls": [
                "https://sztetl.org.pl/en/towns/m/1209-muszyna",
                "http://www.almanachmuszyny.pl/spisy/1998/AM1998_05_zydowski_pensjonat_bristol_w_muszynie.pdf",
                "https://en.wikipedia.org/wiki/Muszyna"
            ]
        },
        {
            "id": "trip_lwow_legionow",
            "title_en": "🏠 Lwów: Legionów 24 — Lusia's wartime apartment, opposite the Opera, 1942-1944  [memoir pp.40, 57]",
            "title_he": "🏠 לבוב: לגיונוב 24 — דירת לוסיה בזמן המלחמה, מול האופרה, 1942-1944  [יומן עמ' 40, 57]",
            "status": "confirmed",
            "summary_en": (
                "After surviving the Nadwórna ghetto liquidation, Lusia lived in Lwów (Lviv) on "
                "the Aryan side under her false identity 'Maria Cizlik' (a real Nadwórna-born "
                "nurse whose birth certificate Lusia used). Her apartment was at Legionów Street "
                "24, opposite the city Theater (Opera) and opposite a German military base. "
                "BUILDING IDENTIFIED 2026-05-21: today's Prospekt Svobody 24, Lviv — a four-storey "
                "Biedermeier-style stone kamienica built 1836-1837 by architect Johann Salzmann "
                "for F. Adamski. Polish national poet Wincenty Pol lived in this building 1856-1866. "
                "Pre-war (interwar Polish period): ground floor housed a confectionery shop; "
                "upper floors were rented apartments — exactly the kind of building where a "
                "Polish-Catholic-passing Jew with forged papers could live unnoticed. During "
                "1941-44 the street's German name was Adolf-Hitler-Ring (the principal Nazi "
                "administrative boulevard of Lemberg). The boulevard sat between Wehrmacht "
                "command offices on the Hetmańska side, with the Wehrmacht-controlled Opera "
                "House 350m up the street as Operntheater Lemberg. The promenade between the "
                "two streets was only ~50m wide — well within rifle range, matching Lusia's "
                "description of gunfire from across the street."
            ),
            "summary_he": (
                "דירתה של לוסיה הייתה ברחוב לגיונוב 24 בלבוב, מול האופרה. הבניין זוהה ב-21.5.2026: "
                "פרוספקט סבובודי 24 כיום — בית אבן בן 4 קומות מסגנון בידרמייר משנת 1836-1837, "
                "מאת האדריכל יוהאן זלצמן. המשורר הפולני וינצנטי פול גר בו 1856-1866. לפני המלחמה: "
                "קונדיטוריה בקומת קרקע, דירות בקומות העליונות. בתקופה הנאצית 1941-44 הרחוב נקרא "
                "אדולף-היטלר-רינג — השדרה הראשית של הממשל הנאצי בלמברג."
            ),
            "source": "Memoir pp.40, 57 + Lviv Interactive + pslava.info",
            "urls": [
                "https://lia.lvivcenter.org/en/objects/svobody/",
                "https://www.pslava.info/LvivM_SvobodyProsp_Bud24,222601.html",
                "https://streets.lvivcenter.org/en/Adolf-Hitler-Ring/",
                "https://en.wikipedia.org/wiki/Prospekt_Svobody",
                "https://en.wikipedia.org/wiki/Lviv_Theatre_of_Opera_and_Ballet"
            ]
        },
        {
            "id": "trip_lwow_rynek_shop",
            "title_en": "🏪 Lwów: the art-objects shop on Rynek Square — Lusia's wartime cover",
            "title_he": "🏪 לבוב: חנות חפצי האמנות בכיכר הרינק — הכיסוי של לוסיה בזמן המלחמה",
            "status": "confirmed",
            "summary_en": (
                "Lusia worked as the manager of an art-objects shop in the commercial complex on "
                "Rynek Square (the Old Market Square) in Lwów. The financial manager of the whole "
                "shop complex was a German named 'Doner'. Lusia made buying trips to acquire art "
                "objects for the shop. The shop's display window was famously beautiful. Lusia "
                "passed multiple Gestapo inspections of her false papers while working there. "
                "Lwów's Rynek Square is today the Площа Ринок in central Lviv — a UNESCO World "
                "Heritage Site preserving the medieval merchant town."
            ),
            "source": "Memoir pp.43-50",
            "urls": ["https://en.wikipedia.org/wiki/Lviv_Old_Town"]
        },
        {
            "id": "trip_nadworna_ghetto",
            "title_en": "💀 The Nadwórna sawmill — David's 'essential worker' badge + escape October 1942",
            "status": "confirmed",
            "summary_en": (
                "Under Nazi occupation 1941-1942, the Nadwórna sawmill (the Jewish-owned 'Foresta' "
                "operation) employed ~600 Jews who held German 'essential worker' badges. David "
                "Rapaport was one of them. On 24 October 1942, during the final Nadwórna ghetto "
                "liquidation, David and 17 other Jews escaped by hiding inside wood-transport "
                "train wagons that he had drilled escape-holes into. Lusia smuggled their son "
                "Shimon (then 5) out of the ghetto in a modified vegetable crate."
            ),
            "source": "Memoir pp.27, 32, 41, 42 + Yad Vashem + Pinkas Polin",
            "urls": [
                "https://www.yadvashem.org/communities/nadworna/german-occupation.html"
            ]
        },
        {
            "id": "trip_brussels_1946",
            "title_en": "🇧🇪 Brussels, April 1946 — refugee transit + Dov's birth",
            "title_he": "🇧🇪 בריסל, אפריל 1946 — תחנת הפליטים והולדת דב",
            "status": "confirmed",
            "summary_en": (
                "After the war's end David, Lusia and Shimon left Lwów, transited Katowice (Poland), "
                "and reached Brussels in April 1946. The Jewish relief organisation Joint (JDC) paid "
                "their hotel rent. Their second son Dov 'Bernard' Rapaport was born in Brussels in "
                "1946. They remained ~1 year before sailing for Palestine on the Theodor Herzl in "
                "April 1947. The Belgian Aliens Police kept individual dossiers on every adult "
                "foreigner — guaranteed to exist for David, Lusia, Dov."
            ),
            "source": "Memoir pp.62, 64 + Archives générales du Royaume",
            "urls": [
                "https://en.wikipedia.org/wiki/Brussels",
                "mailto:agr.searchdesk@arch.be"
            ]
        },
        {
            "id": "trip_sete_theodor_herzl",
            "title_en": "🚢 Sète → Theodor Herzl ship, 2 April 1947 — 2,641 ma'apilim",
            "title_he": "🚢 סט → אוניית תיאודור הרצל, 2 באפריל 1947",
            "status": "confirmed",
            "summary_en": (
                "On 2 April 1947 the ship Theodor Herzl sailed from Sète, France, carrying 2,641 "
                "Holocaust-survivor immigrants (Ma'apilim) — drawn from camps in France and Belgium. "
                "David, Lusia, Shimon and infant Dov were aboard. Commander Mecca Limon. Intercepted "
                "13 April 1947 by HMS Haydon + HMS St Brides Bay. The passengers resisted; three "
                "Ma'apilim were killed by British gunfire (Aharon Dov, Pinchas Weiss, Menachem Samet); "
                "27 wounded. All passengers were deported to Cyprus internment camps."
            ),
            "source": "Palmach / Palyam ship history",
            "urls": ["https://www.palyam.org/English/Hahapala/hf/hf_Theodor_Herzl.pdf"]
        },
        {
            "id": "trip_cyprus_karaolos",
            "title_en": "🏕️ Cyprus — Karaolos internment camp, 1947-1948",
            "title_he": "🏕️ קפריסין — מחנה המעצר קראולוס, 1947-1948",
            "status": "confirmed",
            "summary_en": (
                "After British interception, the Theodor Herzl's passengers were taken to the Cyprus "
                "internment camps (Karaolos near Famagusta + Dekhelia near Larnaca). 12 camps total; "
                "operated August 1946 – January 1949; held 53,510 Jews; ~2,000 children born in "
                "captivity; ~400 detainees died. David's family was held ~8 months. The wounded "
                "passengers (and unaccompanied minors) were diverted to Atlit camp in British "
                "Mandate Palestine — which is where the memoir says young Shimon's release "
                "document came from."
            ),
            "source": "Wikipedia Cyprus internment camps + USHMM",
            "urls": [
                "https://en.wikipedia.org/wiki/Cyprus_internment_camps",
                "https://collections.ushmm.org/search/catalog/irn515820"
            ]
        },
        {
            "id": "trip_atlit",
            "title_en": "🇮🇱 Atlit detention camp — Shimon's release",
            "status": "confirmed",
            "summary_en": (
                "Atlit detainee camp on the coast south of Haifa was the British detention site in "
                "Mandate Palestine for intercepted Ma'apilim 1939-1948. Wounded passengers + "
                "unaccompanied minors from Theodor Herzl were diverted here instead of Cyprus. "
                "The memoir (p.65) references Shimon's release document from Atlit, suggesting he "
                "was separated from his parents and held at Atlit while they were in Cyprus."
            ),
            "source": "Memoir p.65 + Atlit Detainee Camp Heritage Site",
            "urls": ["https://shimur.org/sites/atlit-detention-camp/?lang=en"]
        },
        {
            "id": "trip_haifa_moriah",
            "title_en": "🏠 Haifa, Moriah Street 93 — the family home",
            "title_he": "🏠 חיפה, רחוב מוריה 93 — בית המשפחה",
            "status": "confirmed",
            "summary_en": (
                "After their release from Cyprus, David and Lusia settled in Haifa. Using German "
                "Wiedergutmachung reparations payments, they purchased an apartment of two rooms + "
                "kitchen + toilet on Moriah Street 93, on the Carmel ridge in Haifa. This was the "
                "family home for the rest of their lives. Dov, Doron, Dana, and Daniel's father grew "
                "up in this Haifa milieu — a Polish-speaking, Hebrew-adopting, Galician-survivor "
                "household."
            ),
            "source": "Memoir p.70",
            "urls": ["https://en.wikipedia.org/wiki/Mount_Carmel"]
        },
        {
            "id": "trip_porto_italy",
            "title_en": "🏛️ Portobuffolè + Verona, Italy (16th c.) — the Rapa-Porto surname's origin",
            "status": "confirmed",
            "summary_en": (
                "R. Yechiel Michael ha-Kohen Rapa was born in Portobuffolè (Italian Veneto) in 1502, "
                "after the family fled Mainz. His son Isaac 'HaMoel' was the first to add 'Porto' to "
                "the surname around 1550, creating 'Rapa-Porto' = Rapoport = Rapaport. R. Avraham "
                "Menachem ha-Kohen Rapa-Porto (1520-1596) published 'Mincha Belulah' in Verona 1594, "
                "introducing the family emblem — a raven flanked by upraised palms in the priestly "
                "blessing configuration. The same emblem appears on the website header."
            ),
            "source": "Dr Chanan Rapaport 2018 paper",
            "urls": ["https://en.wikipedia.org/wiki/Rapoport_family"]
        },
        {
            "id": "trip_mallorca_1305",
            "title_en": "🏝️ Mallorca, 1305 — Dr Vidal Rapapa, the earliest documented ancestor",
            "status": "confirmed",
            "summary_en": (
                "Mallorca, Kingdom of Aragon, in the early 14th century — the earliest documented "
                "Rapaport ancestors. Dr Vidal Rapapa (1305) led a Jewish-rescue conspiracy. "
                "Dr Jucef Salomon Rapapa was court physician to King Jaime III of Mallorca (1311); "
                "in 1345 he sued the successor King Pedro IV for 10 Libres in unpaid fees (≈ €600K "
                "to €1.5M today). After the 1391 pogroms and 1492 expulsion, the family fled to "
                "Italy. Their Mallorca origin was independently confirmed by Y-DNA testing of a "
                "modern US Rappoport vs a Mallorcan Chueta-family member."
            ),
            "source": "Dr Chanan Rapaport 2018 paper + Pere Bonnin 'Sangre Judía' 2013",
            "urls": ["https://en.wikipedia.org/wiki/Chueta"]
        },
        {
            "id": "trip_padua_venice",
            "title_en": "🏛️ Padua + Venice, Italy (1482-1597) — the Katzenellenbogen rabbinical dynasty",
            "status": "confirmed",
            "summary_en": (
                "R. Meir Katzenellenbogen 'MaHaRaM Padua' (1482-1565) served as Chief Rabbi of Padua. "
                "His son R. Samuel Judah (1521-1597) became Chief Rabbi of Venice. Their descendant "
                "Saul Wahl Katzenellenbogen (1541-1617) is the legendary 'King of Poland for one "
                "night'. The chain reaches our family via Chawa Wahl Griffel (David Memek's aunt-by-"
                "marriage), confirmed by Y-DNA testing (Avotaynu 2016)."
            ),
            "source": "Edward Gelles 'WAHL of Tarnobrzeg' (Balliol) + Wikipedia",
            "urls": [
                "https://en.wikipedia.org/wiki/Meir_Katzenellenbogen",
                "https://en.wikipedia.org/wiki/Saul_Wahl"
            ]
        },
    ]
}

# Insert after sephardic_origin section
sep_idx = next(i for i, s in enumerate(rc['sections']) if s['id'] == 'sephardic_origin')
rc['sections'].insert(sep_idx + 1, trip_section)

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] Virtual Trip section added. Research Center now {len(rc['sections'])} sections, {sum(len(s['cards']) for s in rc['sections'])} cards.")
print(f"[OK] Virtual Trip has {len(trip_section['cards'])} place-cards covering the memoir's full geography from Mallorca 1305 to Haifa 1948.")
