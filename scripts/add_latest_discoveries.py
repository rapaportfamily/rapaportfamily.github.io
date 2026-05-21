"""Append 2026-05-21 discoveries to events.json so the Home page
'Latest finds' section reflects the most recent work."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EV_PATH = REPO / 'platform' / 'data' / 'events.json'
data = json.loads(EV_PATH.read_text(encoding='utf-8'))

NEW_DISCOVERIES = [
    {
        "id": "e_2026_05_21_legionow24_building_identified",
        "date": "2026-05-21",
        "date_precision": "day",
        "date_sort": "2026-05-21T0900",
        "type": "discovery",
        "place_id": "pl_lviv",
        "people_ids": ["p_lusia"],
        "title": {
            "en": "🏠 Lusia's wartime apartment building IDENTIFIED — Prospekt Svobody 24, Lviv",
            "he": "🏠 בניין דירת לוסיה בזמן המלחמה זוהה — פרוספקט סבובודי 24, לבוב",
            "pl": "🏠 Zidentyfikowano wojenne mieszkanie Lusi — Prospekt Swobody 24, Lwów",
            "fr": "🏠 Identifié l'immeuble de l'appartement de Lusia pendant la guerre — Prospekt Svobody 24, Lviv"
        },
        "description": {
            "en": "ulica Legionów 24 in 1942-1944 Lwów is today's Prospekt Svobody 24, Lviv: a four-storey Biedermeier stone kamienica built 1836-1837 by architect Johann Salzmann for F. Adamski. Polish national poet Wincenty Pol lived there 1856-1866. Lusia rented an upper-floor apartment as 'Maria Cizlik' while a German military base fired guns from across the central promenade. Current photo of the actual building now embedded in the Virtual Trip card.",
            "he": "רחוב לגיונוב 24 בלבוב 1942-1944 הוא היום פרוספקט סבובודי 24 בלביב: בניין אבן ביידרמייר בן ארבע קומות שנבנה ב-1836-1837 על-ידי האדריכל יוהן זלצמן עבור פ. אדמסקי. המשורר הפולסי וינצנטי פול גר בו 1856-1866. לוסיה שכרה דירה בקומה עליונה כ'מריה ציצליק' בעוד בסיס צבאי גרמני מהעבר השני של השדרה ירה ביריות. צילום עדכני של הבניין משובץ עכשיו בכרטיס המסע הוירטואלי.",
            "pl": "Ulica Legionów 24 we Lwowie z lat 1942-1944 to dzisiejszy Prospekt Swobody 24: czteropiętrowa kamienica w stylu biedermeier zbudowana w latach 1836-1837 przez architekta Johanna Salzmanna dla F. Adamskiego. Polski poeta narodowy Wincenty Pol mieszkał tam w latach 1856-1866. Lusia wynajmowała mieszkanie pod nazwiskiem 'Maria Cizlik'.",
            "fr": "La rue Legionów 24 à Lwów en 1942-1944 est l'actuel Prospekt Svobody 24 à Lviv : un immeuble de pierre Biedermeier de quatre étages construit en 1836-1837 par l'architecte Johann Salzmann pour F. Adamski. Le poète polonais Wincenty Pol y vécut de 1856 à 1866. Lusia y louait un appartement sous l'identité 'Maria Cizlik'."
        },
        "confidence": "documented"
    },
    {
        "id": "e_2026_05_21_theodor_herzl_ship_identity",
        "date": "2026-05-21",
        "date_precision": "day",
        "date_sort": "2026-05-21T0800",
        "type": "discovery",
        "place_id": None,
        "people_ids": ["p_david", "p_lusia"],
        "title": {
            "en": "🚢 The Theodor Herzl ship VERIFIED — ex-HMS \"Guardian\", Newcastle 1907 (NOT Exodus 1947)",
            "he": "🚢 זהות אוניית תיאודור הרצל אומתה — HMS \"גארדיאן\" לשעבר, ניוקאסל 1907 (לא אקסודוס)",
            "pl": "🚢 Tożsamość statku Theodor Herzl POTWIERDZONA — d. HMS \"Guardian\", Newcastle 1907 (NIE Exodus 1947)",
            "fr": "🚢 Identité du navire Theodor Herzl VÉRIFIÉE — ex-HMS \"Guardian\", Newcastle 1907 (PAS Exodus 1947)"
        },
        "description": {
            "en": "The Aliyah Bet ship that carried David, Lusia, Shimon and infant Dov from Sète to Cyprus on 2 April 1947 was the ex-British cable-laying ship HMS/SS \"Guardian\" — built 1907 by Swan Hunter & Wigham Richardson in Newcastle, 1,768 tons, triple-expansion engine. Acquired by Mossad LeAliyah Bet in 1946 and refitted at Marseille. Distinct from the SS Exodus 1947 (ex-President Warfield), with which it is routinely conflated.",
            "he": "אוניית העלייה ב' שהובילה את דוד, לוסיה, שמעון ודב התינוק מסט לקפריסין ב-2 באפריל 1947 הייתה ספינת הכבלים הבריטית HMS/SS 'גארדיאן' — נבנתה ב-1907 על-ידי Swan Hunter & Wigham Richardson בניוקאסל, 1,768 טון, מנוע קיטור. נרכשה ב-1946 על-ידי המוסד לעלייה ב' ושופצה במרסיי. שונה מאוניית אקסודוס 1947 (פרסידנט וורפילד לשעבר), איתה היא בלבול נפוץ.",
            "pl": "Statek Aliyah Bet, który przewiózł Dawida, Lusię, Szymona i niemowlę Dova z Sète na Cypr 2 kwietnia 1947, to brytyjski statek kablowy HMS/SS \"Guardian\" — zbudowany w 1907 w Newcastle, 1 768 ton. Nabyty w 1946 przez Mossad LeAliyah Bet i przebudowany w Marsylii. Inny statek niż SS Exodus 1947.",
            "fr": "Le navire Aliyah Bet qui transporta David, Lusia, Szymon et Dov bébé de Sète à Chypre le 2 avril 1947 était le câblier britannique HMS/SS « Guardian » — construit en 1907 à Newcastle, 1 768 tonnes. Acquis en 1946 par le Mossad LeAliyah Bet et réaménagé à Marseille. À ne pas confondre avec le SS Exodus 1947."
        },
        "confidence": "documented"
    },
    {
        "id": "e_2026_05_21_cyprus_karaolos_camp_numbers",
        "date": "2026-05-21",
        "date_precision": "day",
        "date_sort": "2026-05-21T0700",
        "type": "discovery",
        "place_id": None,
        "people_ids": ["p_david", "p_lusia"],
        "title": {
            "en": "🏕️ Cyprus camp numbers DOCUMENTED — Karaolos 55/60/61/62/63 (summer tents) vs Dekhelia (winter huts)",
            "he": "🏕️ מספרי מחנות קפריסין תועדו — קראולוס 55/60/61/62/63 (אוהלי קיץ) מול דכליה (צריפי חורף)",
            "pl": "🏕️ Numery cypryjskich obozów UDOKUMENTOWANE — Karaolos 55/60/61/62/63 (namioty letnie) vs Dekhelia (baraki zimowe)",
            "fr": "🏕️ Numéros des camps de Chypre DOCUMENTÉS — Karaolos 55/60/61/62/63 (tentes d'été) vs Dekhelia (baraques d'hiver)"
        },
        "description": {
            "en": "British internment camps in Cyprus were organised in two clusters: SUMMER tent camps numbered 55, 60, 61, 62, 63 at Caraolos/Karaolos north of Famagusta, and WINTER Nissen-hut camps at Dekhelia/Decauville near Larnaca (~50 km away). 53,510 Jews detained 1946-1949; ~2,200 children born in captivity. David's family was held ~8 months. JDC Archives only holds the Aug 1948 - Feb 1949 birth lists — for the family's roster look at Yad Vashem and USHMM databases.",
            "he": "מחנות המעצר הבריטיים בקפריסין היו מסודרים בשני אשכולות: מחנות אוהלים קיציים במספרים 55, 60, 61, 62, 63 בקראולוס מצפון לפמגוסטה, ומחנות חורף עם צריפי ניסן בדכליה/דקוויל (כ-50 ק\"מ משם). 53,510 יהודים נעצרו 1946-1949; כ-2,200 ילדים נולדו במעצר.",
            "pl": "Brytyjskie obozy internowania na Cyprze były zorganizowane w dwóch klastrach: letnie obozy namiotowe nr 55, 60, 61, 62, 63 w Karaolos koło Famagusty, oraz zimowe baraki Nissen w Dekhelia koło Larnaki.",
            "fr": "Les camps d'internement britanniques de Chypre étaient organisés en deux groupes : camps d'été sous tente nos 55, 60, 61, 62, 63 à Karaolos près de Famagouste, et camps d'hiver en baraques Nissen à Dekhelia près de Larnaca."
        },
        "confidence": "documented"
    },
    {
        "id": "e_2026_05_21_dalia_equal_partner",
        "date": "2026-05-21",
        "date_precision": "day",
        "date_sort": "2026-05-21T0600",
        "type": "discovery",
        "place_id": None,
        "people_ids": ["p_dalia", "p_dana", "p_doron", "p_daniel"],
        "title": {
            "en": "👨‍👩‍👧‍👦 Attribution updated — Dalia, Dana, Doron and Daniel as equal partners",
            "he": "👨‍👩‍👧‍👦 הקרדיט עודכן — דליה, דנה, דורון ודניאל כשותפים שווים",
            "pl": "👨‍👩‍👧‍👦 Atrybucja zaktualizowana — Dalia, Dana, Doron i Daniel jako równi partnerzy",
            "fr": "👨‍👩‍👧‍👦 Crédit mis à jour — Dalia, Dana, Doron et Daniel à parts égales"
        },
        "description": {
            "en": "All attribution language throughout the archive (events, people, places, documents, hypotheses, research center, multilingual UI strings) has been updated to credit Dalia (mother), Dana, Doron and Daniel Rapaport as equal partners in this birthday gift to Dov. Mother and three children — one family voice.",
            "he": "כל שפת הקרדיט בכל הארכיון (אירועים, אנשים, מקומות, מסמכים, השערות, מרכז המחקר, מחרוזות UI רב-לשוניות) עודכנה לכבד את דליה (אמא), דנה, דורון ודניאל רפפורט כשותפים שווים במתנת יום ההולדת הזו לדב. אמא ושלושת ילדיה — קול משפחתי אחד.",
            "pl": "Wszystkie atrybucje w archiwum (wydarzenia, osoby, miejsca, dokumenty, hipotezy, centrum badawcze, wielojęzyczne ciągi UI) zostały zaktualizowane, aby uznać Dalię (matkę), Danę, Dorona i Daniela Rapaport za równych partnerów w tym urodzinowym prezencie dla Dova.",
            "fr": "Tout le langage d'attribution dans l'archive (événements, personnes, lieux, documents, hypothèses, centre de recherche, chaînes d'interface multilingues) a été mis à jour pour créditer Dalia (mère), Dana, Doron et Daniel Rapaport à parts égales dans ce cadeau d'anniversaire pour Dov."
        },
        "confidence": "context"
    },
    {
        "id": "e_2026_05_21_street_view_embeds",
        "date": "2026-05-21",
        "date_precision": "day",
        "date_sort": "2026-05-21T0500",
        "type": "discovery",
        "place_id": None,
        "people_ids": [],
        "title": {
            "en": "🗺️ Every Virtual Trip card now shows the address in Google Street View",
            "he": "🗺️ כל כרטיס במסע הוירטואלי מציג עכשיו את הכתובת בתצוגת רחוב של גוגל",
            "pl": "🗺️ Każda karta Wirtualnej podróży pokazuje teraz adres w Google Street View",
            "fr": "🗺️ Chaque carte du Voyage virtuel affiche désormais l'adresse en Google Street View"
        },
        "description": {
            "en": "All 13 Virtual Trip cards now embed two side-by-side iframes: the OpenStreetMap location plus a Google Street View pegman view at the exact coordinates — labelled 'How it looks today'. No API key required. Click any card to see the place AS IT LOOKS RIGHT NOW.",
            "he": "כל 13 הכרטיסים במסע הוירטואלי משבצים עכשיו שני iframe אחד ליד השני: מיקום ה-OpenStreetMap בתוספת תצוגת רחוב של גוגל ב-coordinates המדויקים — בתווית 'איך זה נראה היום'. ללא צורך במפתח API.",
            "pl": "Wszystkie 13 kart Wirtualnej podróży zawiera teraz dwa iframe obok siebie: lokalizację OpenStreetMap oraz widok Google Street View we wskazanych współrzędnych — z etykietą 'Jak to wygląda dziś'.",
            "fr": "Les 13 cartes du Voyage virtuel intègrent désormais deux iframes côte à côte : la position OpenStreetMap et une vue Google Street View aux coordonnées exactes — étiquetée « Comment cela apparaît aujourd'hui »."
        },
        "confidence": "context"
    }
]

existing_ids = {e['id'] for e in data['events']}
appended = 0
for d in NEW_DISCOVERIES:
    if d['id'] in existing_ids:
        # update in place
        for i, e in enumerate(data['events']):
            if e['id'] == d['id']:
                data['events'][i] = d
                break
    else:
        data['events'].append(d)
        appended += 1

EV_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Appended {appended} new discovery events; total events: {len(data['events'])}")
print(f"Latest 4 discoveries (sorted by date_sort desc):")
discs = sorted([e for e in data['events'] if e.get('type') == 'discovery'],
               key=lambda d: d.get('date_sort',''), reverse=True)
for d in discs[:4]:
    print(f"  {d['date_sort']}  {d['title']['en'][:75]}")
