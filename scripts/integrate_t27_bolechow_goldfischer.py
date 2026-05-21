"""T27: Bolechów Yizkor mining + Goldfischer Skole research + Indeks/JDC verdict.

5 new headline_finds cards:
  - bolechow_yizkor_weitzner_lone_mention
  - eli_weitzner_taniawa_forest_inferred_fate
  - goldfischer_stryj_circle_etymology
  - goldfischer_marin_aliyah_path
  - david_indeks_jdc_manual_instructions
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC = REPO / "platform" / "data" / "research_center.json"
rc = json.loads(RC.read_text(encoding="utf-8"))
hf = next(s for s in rc["sections"] if s["id"] == "headline_finds")

new_cards = [
    {
        "id": "bolechow_yizkor_weitzner_lone_mention",
        "title_en": "📜 Bolechów Yizkor preserves ONE precious Weitzner mention — Eli Weitzner pinned as pre-war Revisionist patron",
        "title_he": "📜 ספר היזכור של בולחוב שומר אזכור יקר אחד של וייצנר — אלי וייצנר נקבע כפטרון רוויזיוניסטי לפני המלחמה",
        "status": "confirmed",
        "summary_en": (
            "Deep mining of the Bolechów Yizkor (Y. Eshel, 1957) found exactly ONE explicit "
            "Weitzner mention, in Yiddish pp. 278-288 (the Abraham Weber memoir): "
            "'The Revisionist ranks in Bolechow were organized with adults in Hatza'r, young "
            "workers and students in Massadah, and the youngest in Betar. D. Rapaport "
            "(Eli Weitzner's son-in-law) helped the movement grow. Hebrew classes were "
            "conducted under the direction of Hinde Delman.' "
            "This single sentence pins down THREE archival targets in one stroke: Eli "
            "Weitzner (Lusia's father), David Memek Rapaport (her husband), and Hinde "
            "Delman (the Hebrew teacher who taught Bolechów's youth). The phrasing "
            "'Eli Weitzner's son-in-law' — rather than 'Lusia's husband' — tells us Eli "
            "was the better-known socially-prominent figure in pre-war Bolechów. "
            "Of ~6,000 Bolechów Jews, only ~48 survived. Lusia and her older sister "
            "Feige (Tzipora) Weitzner b.1911 carried the family forward."
        ),
        "summary_he": (
            "כריית מעמיקה בספר היזכור של בולחוב (י. אשל, 1957) מצאה אזכור וייצנר מפורש "
            "אחד בלבד, ביידיש עמ' 278-288 (זיכרונותיו של אברהם וובר): 'השורות "
            "הרוויזיוניסטיות בבולחוב אורגנו: מבוגרים ב\"החצ\"ר\", פועלים צעירים וסטודנטים "
            "ב\"מצדה\", והצעירים ביותר ב\"בית\"ר\". ד. רפפורט (חתנו של אלי וייצנר) עזר "
            "לתנועה לצמוח. שיעורי עברית התקיימו תחת ניהול הינדה דלמן.' "
            "המשפט הזה מהדק שלוש מטרות ארכיוניות במכה אחת: אלי וייצנר (אביה של לוסיה), "
            "דוד ממק רפפורט (בעלה), והינדה דלמן (המורה לעברית). הניסוח 'חתנו של אלי "
            "וייצנר' — ולא 'בעלה של לוסיה' — מספר שאלי היה הדמות המוכרת חברתית בבולחוב "
            "שלפני המלחמה. מתוך כ-6,000 יהודי בולחוב, רק כ-48 שרדו. לוסיה ואחותה הבוגרת "
            "פייגה (ציפורה) וייצנר ילידת 1911 נשאו את המשפחה הלאה."
        ),
        "quote_en": "The Revisionist ranks in Bolechow were organized with adults in Hatza'r, young workers and students in Massadah, and the youngest in Betar. D. Rapaport (Eli Weitzner's son-in-law) helped the movement grow.",
        "source": "Sefer ha-zikaron le-kedoshei Bolechow (Eshel, 1957), Yiddish pp. 278-288 — Abraham Weber memoir",
        "urls": [
            "https://www.jewishgen.org/yizkor/bolekhov/bol278.html",
            "https://www.jewishgen.org/yizkor/bolekhov/bolekhov.html",
            "https://www.jewishgen.org/yizkor/indices/Bolekhiv_index.pdf"
        ]
    },
    {
        "id": "eli_weitzner_taniawa_forest_inferred",
        "title_en": "🕯️ Eli Weitzner most plausibly killed 28 October 1941 — Taniawa-forest First Aktion",
        "title_he": "🕯️ אלי וייצנר ככל הנראה נרצח ב-28 באוקטובר 1941 — האקציה הראשונה ביער טניאווה",
        "status": "lead",
        "summary_en": (
            "Inferential dating of Eli Weitzner's death, based on the Bolechów Aktion "
            "chronology + his social profile in the Yizkor:\n\n"
            "TIMELINE: First Aktion 28 Oct 1941 — ~1,000 WEALTHIER Jews (merchants, "
            "doctors, rabbis) rounded up at the magistrate, marched to Dom Katolicki, "
            "tortured 24 hours, then shot in the Taniawa forest. Second Aktion 3-5 Sept "
            "1942 — ~1,500 murdered locally + ~2,000 deported to Bełżec. Later October "
            "and November 1942 transports.\n\n"
            "FIT: The Yizkor positions Eli Weitzner as a PROMINENT Revisionist patron "
            "whose son-in-law (David Rapaport) organised Betar in the town. The Oct 1941 "
            "Aktion's targeting of the wealthier merchant class is the most demographically "
            "consistent fate. The Sept 1942 deportation to Bełżec cannot be ruled out as "
            "an alternative. Mathilde Weinreb's fate is undocumented but would have followed "
            "his — likely the same Aktion.\n\n"
            "VERIFY-NEXT: USHMM Bolechow survivors list (Shlomo Adler, received 2012) "
            "is empty for Weitzner — meaning they did not survive. The family lore now "
            "has a probable date to mark."
        ),
        "summary_he": (
            "תיארוך מסקנתי של מות אלי וייצנר, בהתבסס על כרונולוגיית האקציות בבולחוב + "
            "פרופילו החברתי ביזכור: ציר הזמן: האקציה הראשונה 28 באוקטובר 1941 — כ-1,000 "
            "יהודים עשירים יותר (סוחרים, רופאים, רבנים) נאספו בבית הקאתולי, עונו 24 "
            "שעות, ואז נורו ביער טניאווה. האקציה השנייה 3-5 בספטמבר 1942 — כ-1,500 "
            "נרצחו במקום + כ-2,000 גורשו לבלז'ץ. היזכור ממקם את אלי וייצנר כפטרון "
            "רוויזיוניסטי בולט שחתנו (דוד רפפורט) ארגן את בית\"ר בעיירה. כיוון של "
            "האקציה ב-1941 כלפי מעמד הסוחרים העשירים הוא הגורל הקונסיסטנטי דמוגרפית. "
            "גורלה של מטילדה וויינרב לא מתועד אך כנראה היה זהה."
        ),
        "source": "Bolechów Aktion timeline (bol145 + Holocaust in Bolekhiv Wikipedia) cross-referenced with Eli Weitzner's social profile in the 1957 Yizkor",
        "urls": [
            "https://www.jewishgen.org/yizkor/bolekhov/bol145.html",
            "https://en.wikipedia.org/wiki/Holocaust_in_Bolekhiv",
            "https://www.ushmm.org/online/hsv/source_view.php?SourceId=33476"
        ]
    },
    {
        "id": "goldfischer_stryj_circle_etymology",
        "title_en": "🏞️ Goldfischer is a Stryj-circle ornamental surname — Skole / Dobromil / Medenice / Bolechów cluster",
        "title_he": "🏞️ גולדפישר הוא שם משפחה דקורטיבי מאזור סטרי — אשכול סקולה / דוברומיל / מדניצה / בולחוב",
        "status": "confirmed",
        "summary_en": (
            "Goldfischer is documented in Beider's *Dictionary of Jewish Surnames from "
            "Galicia* as an ornamental-occupational hybrid (gold + Fischer/fisher); NOT "
            "a common Galician surname. The known Goldfischer profiles cluster in the "
            "Stryj circle — Skole, Dobromil, Medenice, Bolechów — within ~50-100 km of "
            "each other, suggesting a single extended Galician kindred radiating outward "
            "during the 19th century. Skole's Jewish community was ~3,099 in 1910 (~half "
            "the town), living off the timber trade, wood processing, the local match "
            "factory, and the summer-resort economy. NOT fishing despite the surname — "
            "Goldfischer was ornamental, not occupational, for this family.\n\n"
            "STRONG CANDIDATE COUSIN BRANCH: Salomon Goldfischer + Chaja Alpern of "
            "Medenice (~50 km north of Skole) — parents of Leibisch Goldfischer (b. 28 "
            "Mar 1905 Medenice, survived Auschwitz Mechelen Transport XIII). Worth a "
            "follow-up trace to see if Salomon's siblings produced S. Goldfischer of Skole. "
            "Skole's Jewish community was decimated 1941-43 (Hungarian army July 1941; "
            "Germans Aug 1941; deportations Sept 1942 + final liquidation June + August 1943)."
        ),
        "summary_he": (
            "גולדפישר מתועד במילון בידר של שמות-משפחה יהודיים מגליציה כהיברידי דקורטיבי-"
            "מקצועי (gold + Fischer/דייג); לא שם משפחה גליציאני נפוץ. הפרופילים הידועים "
            "של גולדפישר מתאשכלים באזור סטרי — סקולה, דוברומיל, מדניצה, בולחוב — בתוך "
            "כ-50-100 ק\"מ זה מזה, מצביעים על קרבת משפחה גליציאנית מורחבת יחידה שהתפרסה "
            "החוצה במאה ה-19. הקהילה היהודית של סקולה הייתה כ-3,099 ב-1910 (כחצי "
            "מהעיירה), חיו מסחר עצים, עיבוד עץ, מפעל הגפרורים המקומי, וכלכלת נופש קיץ."
        ),
        "source": "Beider Dictionary of Jewish Surnames from Galicia + cross-referencing Geni + Gesher Galicia + EHRI Goldfischer profiles 2026-05-21",
        "urls": [
            "https://www.geshergalicia.org/families/?id=goldfischer/",
            "https://www.geshergalicia.org/towns/?id=skole/",
            "https://www.geni.com/projects/Jewish-Families-of-Skole-Poland-Galicia/15777",
            "https://sztetl.org.pl/en/towns/s/964-skole/99-history/138026-history-of-community",
            "https://portal.ehri-project.eu/units/be-002157-kd_01017",
            "https://www.avotaynu.com/books/DJSG.htm"
        ]
    },
    {
        "id": "goldfischer_marin_aliyah_path",
        "title_en": "⚓ S. Goldfischer 'Marin' = Civitavecchia maritime academy + Atid/Zim Haifa — work-permit Fifth Aliyah",
        "title_he": "⚓ ש. גולדפישר 'Marin' = האקדמיה הימית בצ'יוויטאווקיה + אתיד/צים חיפה — עליית-עבודה חמישית",
        "status": "lead",
        "summary_en": (
            "The 'Marin' profession listed on S. Goldfischer's ID documents (and noted in "
            "the family circle of identity-document uploads) is best explained by the "
            "1930s Polish-Jewish maritime training pipeline. In the late 1930s, the "
            "Revisionists' CIVITAVECCHIA MARITIME ACADEMY in Italy trained ~200 Jewish "
            "cadets specifically for Aliyah Bet ship operations and merchant marine work. "
            "Atid Navigation Co. (Haifa-registered, the predecessor of Zim Israel "
            "Navigation) was actively recruiting Jewish-European mariners in the same "
            "period. A Polish-Jewish 'Marin' from Skole arriving in Haifa in the 1930s "
            "fits the Fifth Aliyah maritime-labor cohort — a WORK PERMIT track, distinct "
            "from a refugee track.\n\n"
            "IMPLICATION: S. Goldfischer was likely established in Haifa BEFORE the "
            "Holocaust hit Skole in 1941-43 — explaining why he and his immediate family "
            "(Ester + Dalia) survived. Other Skole Goldfischers (including possibly Isak, "
            "b.1927, who appears in the Lvov Ghetto Database) did not have that "
            "work-permit and were caught in the catastrophe.\n\n"
            "VERIFY-NEXT: Central Zionist Archives Aliyah card files 1933-39 + IGRA AID "
            "Mandate-era Haifa residence cards + Skole martyrs list at "
            "jewishgen.org/yizkor/galicia4/gal314.html."
        ),
        "summary_he": (
            "המקצוע 'Marin' המופיע במסמכי הזהות של ש. גולדפישר מוסבר היטב על-ידי צינור "
            "ההכשרה הימית היהודית-פולנית בשנות ה-30. בסוף שנות ה-30, האקדמיה הימית "
            "הרוויזיוניסטית בצ'יוויטאווקיה באיטליה הכשירה כ-200 חניכים יהודים במיוחד "
            "לפעולות עלייה ב' ולעבודה ימית מסחרית. חברת הנווט אתיד (רשומה בחיפה, אבן "
            "הדרך של צים) גייסה ימאים יהודים-אירופים באותה התקופה. הימאי הפולני-יהודי "
            "מסקולה שהגיע לחיפה בשנות ה-30 מתאים לקבוצת העלייה החמישית של פועלים-ימאים — "
            "מסלול אישור עבודה, נבדל ממסלול פליטים. כלומר: ש. גולדפישר ככל הנראה היה "
            "מבוסס בחיפה לפני שהשואה הגיעה לסקולה 1941-43."
        ),
        "action_item_en": "Verify via Central Zionist Archives Aliyah card files 1933-39 + IGRA AID Mandate-era Haifa residence cards. Get Doron's grandfather's full Hebrew name from family papers.",
        "source": "Cross-reference of Skole demographic + Civitavecchia + Atid Navigation history 2026-05-21",
        "urls": [
            "https://www.zionistarchives.org.il",
            "https://genealogy.org.il/AID/",
            "https://www.jewishgen.org/yizkor/galicia4/gal314.html"
        ]
    },
    {
        "id": "david_indeks_jdc_manual_search_instructions",
        "title_en": "📋 Doron's 5-minute manual search list — Indeks Represjonowanych + JDC Bricha (will resolve Soviet-exile hypothesis)",
        "title_he": "📋 רשימת חיפוש ידני 5 דקות לדורון — Indeks Represjonowanych + ג'וינט בריחה (יפתור את השערת הגלות הסובייטית)",
        "status": "lead",
        "summary_en": (
            "Both crucial databases (IPN Indeks Represjonowanych for Polish Soviet "
            "deportees + JDC Names Index for Bricha 1946 transit) sit behind JavaScript "
            "search forms that automated agents cannot reach (Google doesn't index their "
            "result detail pages). Doron must run these manually — 5 minutes each, free. "
            "A hit on EITHER database is conclusive proof of David's Soviet-exile → "
            "Bricha → Brussels DP trajectory.\n\n"
            "Step-by-step (run in this order, both in browser):\n\n"
            "1. **Indeks Represjonowanych** — go to "
            "https://indeksrepresjonowanych.pl/wyszukiwanie\n"
            "   - Nazwisko (surname): try in turn Rapaport, Rapoport, Rappaport, Rapaport\n"
            "   - Imię (given name): Dawid (then blank, then David)\n"
            "   - Rok urodzenia (birth year): 1911 (then sweep 1909-1913)\n"
            "   - Steve Morse English wrapper available at "
            "https://stevemorse.org/siberia/siberia.html\n"
            "   - If a hit: click through to the /szczegoly/{uuid} page for deportation "
            "date, NKVD source-list (1940 Feb/Apr/Jun/Jul waves, Anders roster, Gulag list, etc.)\n\n"
            "2. **JDC Names Index** — go to https://names.archives.jdc.org\n"
            "   - Last Name: Rapaport, Rapoport, Rappaport\n"
            "   - First Name: David, Dawid\n"
            "   - Narrow to Bricha / Czechoslovakia 1946 / Nachod / Bratislava / Brussels\n"
            "   - A hit on a 1946 Czech transit list = the smoking gun\n\n"
            "DECOYS already ruled out (do not be misled): Czech Terezín victim 'David "
            "Rappaport b.1907' (Holocaust.cz ID 56593); Baranowicze victim 'David "
            "Rapaport' (Yad Vashem ID 13213602); 'David Simkha Rapaport' Shoah victim "
            "(Yad Vashem ID 9843056); the 1891-born Memorial Russia entry; the "
            "Hungarian-American psychologist David Rapaport (1911-1960, Hungary-born)."
        ),
        "summary_he": (
            "שני מסדי הנתונים הקריטיים (IPN Indeks Represjonowanych לגולים-סובייטים "
            "פולנים + מאגר השמות של הג'וינט לבריחה 1946) יושבים מאחורי טפסי חיפוש "
            "JavaScript שסוכנים אוטומטיים לא יכולים להגיע אליהם. דורון חייב להריץ אותם "
            "ידנית — 5 דקות לכל אחד, חינם. תוצאה באחד מהם היא הוכחה ניצחת למסלולו של "
            "דוד: גלות סובייטית → בריחה → מחנה עקורים בריסל. הוראות צעד אחר צעד "
            "בטקסט האנגלי."
        ),
        "action_item_en": "RUN THESE TWO SEARCHES NOW (5 min each): https://indeksrepresjonowanych.pl/wyszukiwanie + https://names.archives.jdc.org. A hit resolves dossier 21's central hypothesis.",
        "source": "Deep-research agent + cross-source decoy-elimination 2026-05-21",
        "urls": [
            "https://indeksrepresjonowanych.pl/wyszukiwanie",
            "https://stevemorse.org/siberia/siberia.html",
            "https://names.archives.jdc.org",
            "https://archives.jdc.org/our-collections/names-index/"
        ]
    }
]

existing = {c["id"] for c in hf["cards"]}
for nc in new_cards:
    if nc["id"] not in existing:
        hf["cards"].insert(0, nc)

rc["build_version"] = "2026-05-21-T27-bolechow-goldfischer-david-actions"
RC.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"=== Added {len(new_cards)} new headline_finds cards ===")
for c in new_cards:
    print(f"  {c['id']}")
print(f"=== build_version: {rc['build_version']} ===")
