"""Places update (T13):
1. Update Lwów with Prospekt Svobody 24 building identification + multi-lang
   significance.
2. Add new significant places from the Virtual Trip not yet in places.json:
   Sète, Cyprus (Karaolos), Atlit, Haifa, Marseille.
3. Fill in missing names.he and names.fr for 5 places.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PL_PATH = REPO / 'platform' / 'data' / 'places.json'
data = json.loads(PL_PATH.read_text(encoding='utf-8'))
places = data['places']
by_id = {p['id']: p for p in places}

# ── 1) Update Lwów ────────────────────────────────────────────────────
lwow = by_id['pl_lwow']
lwow['building_now'] = "Prospekt Svobody 24, Lviv, Ukraine"
lwow['significance'] = (
    "David Rapaport's residence as of 1 Jan 1938 (per Brussels DP card). "
    "Where David and Lusia survived the war under false identities. Lusia lived "
    "at Legionów Street 24 (today's Prospekt Svobody 24) as 'Maria Cizlik' — "
    "a four-storey Biedermeier kamienica built 1836-1837 by architect Johann "
    "Salzmann for F. Adamski, where Polish national poet Wincenty Pol lived "
    "1856-1866. The street was renamed Adolf-Hitler-Ring during the 1941-1944 "
    "Nazi occupation. David worked on rail/road construction. David's sister "
    "Lota lived in Lwów too."
)
lwow['significance_he'] = (
    "מקום מגוריו של דוד רפפורט נכון ל-1 בינואר 1938 (לפי כרטיס ה-DP מבריסל). "
    "שם שרדו דוד ולוסיה את המלחמה תחת זהויות בדויות. לוסיה התגוררה ברחוב "
    "לגיונוב 24 (היום פרוספקט סבובודי 24) בזהות 'מריה ציצליק' — בניין אבן "
    "ביידרמייר בן ארבע קומות שנבנה ב-1836-1837 על-ידי האדריכל יוהן זלצמן עבור "
    "פ. אדמסקי, ובו גר המשורר הפולסי וינצנטי פול 1856-1866. הרחוב נקרא "
    "אדולף-היטלר-רינג בזמן הכיבוש הנאצי 1941-1944. דוד עבד בבניית כבישים ומסילות. "
    "אחותו של דוד לוטה התגוררה אף היא בלבוב."
)
lwow['significance_pl'] = (
    "Miejsce zamieszkania Dawida Rapaporta od 1 stycznia 1938 (wg brukselskiej "
    "karty DP). Tu Dawid i Lusia przetrwali wojnę pod fałszywymi tożsamościami. "
    "Lusia mieszkała przy ulicy Legionów 24 (dzisiejszy Prospekt Swobody 24) "
    "jako 'Maria Cizlik' — czteropiętrowa kamienica w stylu biedermeier "
    "zbudowana w latach 1836-1837 przez Johanna Salzmanna dla F. Adamskiego. "
    "Polski poeta narodowy Wincenty Pol mieszkał tam w latach 1856-1866. "
    "Podczas okupacji nazistowskiej 1941-1944 ulica nosiła nazwę Adolf-Hitler-Ring."
)
lwow['significance_fr'] = (
    "Lieu de résidence de David Rapaport au 1er janvier 1938 (selon la fiche "
    "DP de Bruxelles). David et Lusia y survécurent à la guerre sous de "
    "fausses identités. Lusia habitait rue Legionów 24 (aujourd'hui Prospekt "
    "Svobody 24) sous l'identité « Maria Cizlik » — un immeuble Biedermeier "
    "de quatre étages construit en 1836-1837 par l'architecte Johann Salzmann "
    "pour F. Adamski, où le poète national polonais Wincenty Pol vécut de "
    "1856 à 1866. La rue fut rebaptisée Adolf-Hitler-Ring durant l'occupation "
    "nazie de 1941-1944."
)

# ── 2) Update Nadwórna with HE significance ──────────────────────────
nad = by_id['pl_nadworna']
nad['significance_he'] = (
    "מקום הולדתו של דוד רפפורט (1911) ושל רבקה גריפל (1888). משפחות גריפל-חיות "
    "היו סוחרים במקום. אתר הגטו שממנו ברח דוד."
)
nad['significance_pl'] = (
    "Miejsce urodzenia Dawida Rapaporta (1911) i Rebeki Griffel (1888). "
    "Rodziny Griffel-Chajes były tu kupcami. Miejsce getta, z którego Dawid uciekł."
)
nad['significance_fr'] = (
    "Lieu de naissance de David Rapaport (1911) et de Rebeka Griffel (1888). "
    "Les familles Griffel-Chajes y étaient commerçantes. Site du ghetto d'où David s'est échappé."
)

# ── 3) Fill missing names.he / names.fr ──────────────────────────────
MISSING_NAMES = {
    'pl_wierzbiany': {
        'he': 'ויירז\'ביאני (כיום וירזביאני, אוקראינה)',
        'fr': 'Wierzbiany (aujourd\'hui Vierzbiany, Ukraine)'
    },
    'pl_morszyn': {
        'he': 'מורשין (כיום מורשין, אוקראינה)',
        'fr': 'Morszyn (aujourd\'hui Morshyn, Ukraine)'
    },
    'pl_muszyna': {
        'he': 'מושינה',
    },
    'pl_mszana_dolna': {
        'he': 'משאנה דולנה',
    },
    'pl_mosina_greater_poland': {
        'he': 'מוסינה (ליד פוזנן)',
        'fr': 'Mosina (près de Poznań)'
    },
}
for pid, names in MISSING_NAMES.items():
    if pid not in by_id:
        continue
    for lang, name in names.items():
        if not by_id[pid].setdefault('names', {}).get(lang):
            by_id[pid]['names'][lang] = name

# ── 4) Add NEW PLACES from the Virtual Trip ──────────────────────────
NEW_PLACES = [
    {
        "id": "pl_sete",
        "names": {
            "en": "Sète, France",
            "he": "סט, צרפת",
            "pl": "Sète, Francja",
            "fr": "Sète, France",
            "yi": "סעט"
        },
        "coords": [43.4045, 3.6963],
        "era_context": {
            "1947": "Allied-occupied France post-war. Mediterranean fishing port used by Mossad LeAliyah Bet as a clandestine departure point for survivor-bearing ships to British Mandate Palestine."
        },
        "significance": "Departure port of the Aliyah Bet ship Theodor Herzl on 2 April 1947 with 2,641 ma'apilim — including David, Lusia, Shimon and infant Dov Rapaport.",
        "significance_he": "נמל היציאה של אוניית העלייה ב' תיאודור הרצל ב-2 באפריל 1947 עם 2,641 מעפילים — ובהם דוד, לוסיה, שמעון ודב התינוק.",
        "significance_pl": "Port wyjścia statku Aliyah Bet Theodor Herzl 2 kwietnia 1947 z 2 641 ma'apilim — w tym Dawid, Lusia, Szymon i niemowlę Dov.",
        "significance_fr": "Port de départ du navire Aliyah Bet Theodor Herzl le 2 avril 1947 avec 2 641 ma'apilim — dont David, Lusia, Szymon et le bébé Dov.",
        "important_events_ids": []
    },
    {
        "id": "pl_cyprus_karaolos",
        "names": {
            "en": "Karaolos / Caraolos, Cyprus",
            "he": "קראולוס, קפריסין",
            "pl": "Karaolos, Cypr",
            "fr": "Karaolos, Chypre",
            "el": "Καραόλος"
        },
        "coords": [35.1265, 33.943],
        "era_context": {
            "1946_1949": "British-controlled Cyprus. Site of British internment camps for Jewish Holocaust survivors intercepted en route to British Mandate Palestine. 53,510 Jews held, ~2,200 children born in captivity."
        },
        "significance": "Internment site of David, Lusia, Shimon and infant Dov for ~8 months after the British boarded the Theodor Herzl in April 1947. Summer tent camps 55, 60, 61, 62, 63 were at Karaolos north of Famagusta; winter Nissen-hut camps were at Dekhelia near Larnaca.",
        "significance_he": "אתר המעצר של דוד, לוסיה, שמעון ודב התינוק במשך כ-8 חודשים לאחר השתלטות הבריטית על תיאודור הרצל באפריל 1947. מחנות אוהלים קיציים 55, 60, 61, 62, 63 היו בקראולוס צפונית לפמגוסטה; מחנות חורף עם צריפי ניסן היו בדכליה ליד לרנקה.",
        "significance_pl": "Miejsce internowania Dawida, Lusi, Szymona i niemowlęcia Dova przez około 8 miesięcy po przejęciu Theodora Herzla przez Brytyjczyków w kwietniu 1947. Letnie obozy namiotowe nr 55, 60, 61, 62, 63 znajdowały się w Karaolos koło Famagusty.",
        "significance_fr": "Lieu d'internement de David, Lusia, Szymon et Dov bébé pendant environ 8 mois après l'arraisonnement du Theodor Herzl en avril 1947. Camps d'été sous tente nos 55, 60, 61, 62, 63 à Karaolos, près de Famagouste.",
        "important_events_ids": []
    },
    {
        "id": "pl_atlit",
        "names": {
            "en": "Atlit, British Mandate Palestine",
            "he": "עתלית",
            "pl": "Atlit, Brytyjski Mandat Palestyny",
            "fr": "Atlit, Mandat britannique de Palestine"
        },
        "coords": [32.7264, 34.9389],
        "era_context": {
            "1939_1948": "British detention camp on the Mediterranean coast south of Haifa. Held intercepted Ma'apilim (Aliyah Bet illegal immigrants), unaccompanied minors and the wounded who could not be deported to Cyprus."
        },
        "significance": "Detention site of young Shimon Rapaport (David and Lusia's elder son) per his release document referenced in the memoir (p.65) — likely separated from his parents with the wounded from the Theodor Herzl and held at Atlit while David and Lusia were in Cyprus.",
        "significance_he": "אתר המעצר של שמעון רפפורט הצעיר (בכורם של דוד ולוסיה) לפי תעודת השחרור שלו המוזכרת ביומן (עמ' 65) — ככל הנראה הופרד מהוריו עם פצועי תיאודור הרצל בעוד דוד ולוסיה היו בקפריסין.",
        "significance_pl": "Miejsce zatrzymania młodego Szymona Rapaporta (starszego syna Dawida i Lusi) wg dokumentu zwolnienia wspomnianego w pamiętniku (s. 65).",
        "significance_fr": "Lieu de détention du jeune Szymon Rapaport (fils aîné de David et Lusia) selon son document de libération mentionné dans le mémoire (p. 65).",
        "important_events_ids": []
    },
    {
        "id": "pl_haifa",
        "names": {
            "en": "Haifa, Israel",
            "he": "חיפה",
            "pl": "Hajfa, Izrael",
            "fr": "Haïfa, Israël",
            "yi": "חיפה",
            "ar": "حيفا"
        },
        "coords": [32.7940, 34.9896],
        "era_context": {
            "1947_1948": "Main British-administered port of Mandate Palestine. Where Aliyah Bet ships were intercepted and where the State of Israel proclaimed independence in May 1948.",
            "1948_": "Major Israeli port city on Mount Carmel. The Rapaport family settled here after release from Cyprus."
        },
        "significance": "Arrival and lifelong-home city of the Rapaport family after Cyprus. David died here 29 August 1990, age 78, buried at Sde Yehoshua cemetery. Lusia died 28 December 1996, age 83, adjacent grave 102ג. Doron, Dana and Daniel grew up here.",
        "significance_he": "עיר ההגעה והבית של משפחת רפפורט לאחר קפריסין. דוד נפטר כאן ב-29 באוגוסט 1990, בן 78, נטמן בבית הקברות שדה יהושע. לוסיה נפטרה ב-28 בדצמבר 1996, בת 83, בקבר סמוך 102ג. דורון, דנה ודניאל גדלו כאן.",
        "significance_pl": "Miasto przybycia i pożycia rodziny Rapaport po Cyprze. Dawid zmarł tu 29 sierpnia 1990, wiek 78. Lusia zmarła 28 grudnia 1996, wiek 83.",
        "significance_fr": "Ville d'arrivée et de vie de la famille Rapaport après Chypre. David y mourut le 29 août 1990, à 78 ans. Lusia mourut le 28 décembre 1996, à 83 ans.",
        "important_events_ids": []
    },
    {
        "id": "pl_marseille",
        "names": {
            "en": "Marseille, France",
            "he": "מרסיי, צרפת",
            "pl": "Marsylia, Francja",
            "fr": "Marseille, France"
        },
        "coords": [43.2965, 5.3698],
        "era_context": {
            "1946_1947": "Major Mediterranean port in post-war Allied France. Used by Mossad LeAliyah Bet to refit acquired ships for the clandestine immigration to Palestine."
        },
        "significance": "Where the ex-British cable ship HMS Guardian (built 1907, Newcastle) was refitted in 1946-1947 for ~2,600 passengers before its rechristening as the 'Theodor Herzl' and the April 1947 voyage from Sète that carried David, Lusia, Shimon and infant Dov.",
        "significance_he": "המקום שבו שופצה ב-1946-1947 ספינת הכבלים הבריטית HMS גארדיאן (נבנתה ב-1907 בניוקאסל) להובלת כ-2,600 מעפילים, לפני קבלת השם 'תיאודור הרצל' והפלגתה מסט באפריל 1947.",
        "significance_pl": "Miejsce, gdzie w latach 1946-1947 brytyjski statek kablowy HMS Guardian został przebudowany na transport około 2 600 ma'apilim przed przemianowaniem na 'Theodor Herzl'.",
        "significance_fr": "Lieu où le câblier britannique HMS Guardian (construit en 1907 à Newcastle) fut réaménagé en 1946-1947 pour environ 2 600 passagers avant d'être rebaptisé « Theodor Herzl ».",
        "important_events_ids": []
    }
]

added = []
for new in NEW_PLACES:
    if new['id'] in by_id:
        # update in place
        by_id[new['id']].update(new)
    else:
        places.append(new)
        added.append(new['id'])

PL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"Lwów updated with Prospekt Svobody 24 details + multi-lang significance")
print(f"Nadwórna multi-lang significance added")
print(f"Filled missing names.he/fr in {len(MISSING_NAMES)} places")
print(f"Added {len(added)} new places: {', '.join(added) if added else '(all already existed, updated in place)'}")
print(f"Total places now: {len(places)}")
