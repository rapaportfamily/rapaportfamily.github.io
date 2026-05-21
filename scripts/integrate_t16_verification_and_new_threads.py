"""T16: Verification caveats + new research threads (Goldfischer, Filip, Schrenzel).

1. Update h_david_war_escape with primary-source verification caveat.
2. Add headline_finds cards for:
   - Tzvi Hirsh Filip (verified primary-source teacher lineage)
   - Abraham Rapoport 'Schrenzel' (verified - Eitan ha-Ezrachi 1796 genealogy bridge)
   - S. Goldfischer (inferred — flagged as unverified)
3. Bump build_version.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'
HY_PATH = REPO / 'platform' / 'data' / 'hypotheses.json'

rc = json.loads(RC_PATH.read_text(encoding='utf-8'))
hy = json.loads(HY_PATH.read_text(encoding='utf-8'))

# ── 1) Update David's hypothesis with verification caveat ────────────
hyps = hy['hypotheses'] if isinstance(hy, dict) and 'hypotheses' in hy else hy
for h in hyps:
    if h.get('id') == 'h_david_war_escape':
        existing_next = h.get('next_steps', [])
        if isinstance(existing_next, list):
            highest_priority_step = (
                "🎯 HIGHEST-LEVERAGE NEXT STEP (2026-05-21 verification): "
                "Browser-search Yad Vashem Names DB (collections.yadvashem.org/en/names) for "
                "'Berisz Rapaport' or 'Rebeka Griffel' Pages of Testimony. If David Rapaport "
                "is the submitter, that single document PROVES survival + identifies post-war "
                "address. All 6 primary databases require interactive form submission that "
                "automated tools cannot execute. Soviet-exile hypothesis remains the most "
                "parsimonious fit but is NEITHER confirmed NOR contradicted by remote search."
            )
            if highest_priority_step not in existing_next:
                h['next_steps'] = [highest_priority_step] + existing_next
        h['confidence'] = 'hypothesis'  # remain hypothesis until Yad Vashem hit
        break

# ── 2) Add 3 new headline_finds ──────────────────────────────────────
hf = next(s for s in rc['sections'] if s['id'] == 'headline_finds')
new_cards = [
    {
        "id": "tzvi_hirsh_filip_lineage_verified",
        "title_en": "🕯️ Tzvi Hirsh Filip of Nadwórna (c.1740-1801) — teachers + students CONFIRMED",
        "title_he": "🕯️ צבי הירש פיליפ מנדבורנה (לערך 1740-1801) — מוריו ותלמידיו אומתו",
        "status": "confirmed",
        "summary_en": "R. Tzvi Hirsh Filip, founding Hasidic rebbe of Nadwórna, verified via Jewish Galicia & Bukovina and KehilaLinks Nadwórna authors page: disciple of the Maggid of Mezeritch (Dov Ber) and the Maggid of Zlotchov (Yechiel Michel). Students included R. Menachem Mendel Hager of Kosov (founder of the Kosov/Vizhnitz Hasidic dynasty!) and R. Avraham David Wahrman of Buczacz. Major works: Tzemach Hashem LeTzvi, Siftei Kedoshim, Mili De-Avot, Alpha Beita (Zhytomyr 1848 — posthumous; auction record at tiferetauctions.com). Died 1801, succeeded in Nadwórna by son R. David Aryeh Leib Filip and son-in-law R. Yitzhak of Radzivil. Burial in Nadwórna cemetery (destroyed in WWII).",
        "summary_he": "רבי צבי הירש פיליפ, האדמו\"ר המייסד של חסידות נדבורנה, אומת דרך 'גליציה ובוקובינה היהודית' ועמוד המחברים של KehilaLinks נדבורנה: תלמיד המגיד ממזריץ' (דב בר) והמגיד מזלוטשוב (יחיאל מיכל). בין תלמידיו: רבי מנחם מנדל הגר מקוסוב (מייסד שושלת קוסוב/ויזניץ' החסידית!) ורבי אברהם דוד וורמן מבוצ'אץ'. חיבוריו העיקריים: צמח השם לצבי, שפתי קדושים, מילי דאבות, אלפא ביתא (ז'יטומיר 1848 — אחרי מותו). נפטר 1801, ירש אותו בנדבורנה בנו רבי דוד אריה לייב פיליפ וחתנו רבי יצחק מרדזיוויל. נטמן בבית הקברות בנדבורנה (נחרב במלחה\"ע ה-2).",
        "source": "Jewish Galicia & Bukovina person record + KehilaLinks Nadwórna authors page + Tiferet Auctions catalog record",
        "urls": [
            "http://www.jgaliciabukovina.net/112257/person/tzvi-hirsh-filip-nadworna",
            "https://kehilalinks.jewishgen.org/nadvorna/authors.asp",
            "https://en.wikipedia.org/wiki/Kosov_(Hasidic_dynasty)",
            "https://encyclopedia.yivo.org/article.aspx/Kosov-Vizhnits_Hasidic_Dynasty"
        ],
        "open_thread_en": "The traditional family claim that Tzvi Hirsh Filip is a direct Rapaport-Kohen ancestor is currently oral-tradition only. Documentary proof would require matching JewishGen's rabbinic-surnames file or a generation-by-generation tree from Filip's son R. David Aryeh Leib down through Nadwórna's 19th-century Kohanic rabbinical families.",
        "open_thread_he": "המסורת המשפחתית שצבי הירש פיליפ הוא אב קדמון ישיר של שושלת רפפורט-כהן היא כיום מסורת בעל-פה בלבד. הוכחה תיעודית תדרוש התאמה לקובץ שמות הרבנים של JewishGen או עץ דור-אחר-דור מבנו רבי דוד אריה לייב, דרך משפחות הרבנים הכהניים של נדבורנה במאה ה-19."
    },
    {
        "id": "abraham_schrenzel_lineage_verified",
        "title_en": "📜 R. Abraham Rapoport 'Schrenzel' (1584-1651) — full bio CONFIRMED, descent bridge in Eitan ha-Ezrachi (1796)",
        "title_he": "📜 רבי אברהם רפפורט 'שרנצל' (1584-1651) — ביוגרפיה מלאה אומתה, גשר היוחסין ב'איתן האזרחי' (1796)",
        "status": "confirmed",
        "summary_en": "R. Abraham Rapoport 'Schrenzel' (b.1584 Lemberg, d.7 June 1651 Lemberg) confirmed via Wikipedia + Jewish Encyclopedia. Father: R. Israel Yehiel Rapoport of Kraków (Kohen line). Father-in-law: R. Mordecai Schrenzel of Lemberg — hence the 'Schrenzel' cognomen from marrying into a wealthy Lemberg family. Teacher: R. Yehoshua Falk Katz (the SMA — Sefer Me'irat Einayim). Head of Lemberg yeshiva 45 years; President of the Vaad Arba Aratzot (Council of Four Lands); treasurer of Holy Land charity (Halukah) collections. Major work: 'Eitan ha-Ezrachi' (Ostrów 1796), published posthumously by his grandson Abraham (rabbi of Baslov) — the family genealogy at the end of the printed volume is the PRIMARY-SOURCE BRIDGE for Rapaport descendant claims. Three documented daughters: (1) wife of R. Joel Katzenellenbogen; (2) wife of R. Aaron ha-Levi Ettinger, rabbi of Rzeszów; (3) wife of Baruch b. Mendel b. Hirz.",
        "summary_he": "רבי אברהם רפפורט 'שרנצל' (נולד 1584 בלמברג, נפטר 7 ביוני 1651 בלמברג) אומת דרך ויקיפדיה והאנציקלופדיה היהודית. אביו: רבי ישראל יחיאל רפפורט מקרקוב (שושלת הכהנים). חותנו: רבי מרדכי שרנצל מלמברג — מכאן הכינוי 'שרנצל' שמקורו בנישואיו למשפחה לבמברגית עשירה. רבו: רבי יהושע פלק כץ (הסמ\"ע — ספר מאירת עיניים). ראש ישיבת למברג במשך 45 שנה; נשיא ועד ארבע הארצות; גזבר אוסף חלוקת ארץ הקודש. חיבורו העיקרי: 'איתן האזרחי' (אוסטרוב 1796) — שיצא לאור לאחר מותו על-ידי נכדו אברהם (רב בסלוב). עץ היוחסין המופיע בסוף החיבור הוא **המקור הראשוני** לטענות צאצאות רפפורט. שלוש בנות מתועדות: (1) אשת רבי יואל קצנלנבוגן; (2) אשת רבי אהרון הלוי אטינגר, רב ז'שוב; (3) אשת ברוך בן מנדל בן הירץ.",
        "source": "Wikipedia 'Abraham Rapoport' + JewishEncyclopedia.com 'Rapoport' + Encyclopedia.com + Geni 'Avraham Shrentzel Rappoport'",
        "urls": [
            "https://en.wikipedia.org/wiki/Abraham_Rapoport",
            "https://www.jewishencyclopedia.com/articles/12576-rapoport",
            "https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/rapoport-abraham-ben-israel-jehiel-hakohen",
            "https://www.geni.com/people/R-Avraham-Shrentzel-Rappoport/6000000008919045305"
        ],
        "open_thread_en": "Specific Berisz Rapaport (David Memek's father) → Abraham Schrenzel chain not yet verified link-by-link. Required next step: scan the genealogy appendix of Eitan ha-Ezrachi 1796 on HebrewBooks.org / Otzar HaHochma and match each generation."
    },
    {
        "id": "goldfischer_skole_research_thread",
        "title_en": "🔍 S. Goldfischer of Skole (b.1909) — research thread opened",
        "title_he": "🔍 ש. גולדפישר מסקולה (יליד 1909) — חוט מחקר נפתח",
        "status": "lead",
        "summary_en": "Dalia, Dana, Doron and Daniel's maternal grandfather S. Goldfischer was born 23 November 1909 in Skole (Carpathian foothills, eastern Galicia; today Skole, Lviv Oblast, Ukraine). Profession 'Marin' (sailor/merchant marine). Married Ester. Settled in Haifa. WHAT WE STILL NEED TO FIND: (a) his Hebrew/Yiddish first name — 'S.' most likely Shmuel or Shlomo per Skole-area 1909 naming patterns; (b) his parents (search JRI-Poland Skole birth records); (c) why 'Marin' — likely Polish merchant marine via Gdynia 1930s, OR Mandate-era Jewish coastal shipping out of Haifa, OR the Hebrew 'מארין' = port-trades worker; (d) Aliyah window most likely 1933-1939 (Fifth Aliyah, Polish Jews fleeing rising antisemitism).",
        "summary_he": "סבא מצד אמא של דליה, דנה, דורון ודניאל — ש. גולדפישר — נולד ב-23 בנובמבר 1909 בסקולה (למרגלות הקרפטים, גליציה המזרחית; היום סקולה, מחוז לבוב, אוקראינה). מקצוע: 'Marin' (מלח/ימאי סוחר). נישא לאסתר. התיישב בחיפה. מה שעדיין צריך למצוא: (א) השם העברי/יידיש שלו — 'ש.' ככל הנראה שמואל או שלמה לפי דפוסי שמות אזור סקולה ב-1909; (ב) הוריו (לחפש בתעודות לידה של סקולה ב-JRI-Poland); (ג) מדוע 'Marin' — ככל הנראה מסחר ימי פולני דרך גדיניה בשנות ה-30, או ספנות יהודית בתקופת המנדט מחיפה, או 'מארין' = פועל בענפי הנמל; (ד) חלון העלייה הסביר ביותר 1933-1939 (העלייה החמישית, יהודים פולנים בורחים מאנטישמיות גוברת).",
        "source": "Family identity documents (5/19 upload, French-Hebrew bilingual Israeli passport) + Skole-area Galician naming-pattern inference (2026-05-21)",
        "urls": [
            "https://www.jri-poland.org/town/skole/",
            "https://beta.jri-poland.org/town-surnames-list/skole/",
            "https://www.geshergalicia.org/all-galicia-database/",
            "https://www.geni.com/projects/Jewish-Families-of-Skole-Poland-Galicia/15777"
        ],
        "next_steps_en": "JRI-Poland Skole surname search for Goldfischer / Goldfisher / Goldfiszer; Yad Vashem Names DB for any Goldfischer Shoah victims from Skole; Israel State Archives Aliyah file request."
    }
]

existing_ids = {c['id'] for c in hf['cards']}
for nc in new_cards:
    if nc['id'] in existing_ids:
        for i, c in enumerate(hf['cards']):
            if c['id'] == nc['id']:
                hf['cards'][i] = nc
                break
    else:
        hf['cards'].insert(0, nc)

# ── 3) Bump build_version ────────────────────────────────────────────
rc['build_version'] = "2026-05-21-T16-verification-+-new-threads"

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
HY_PATH.write_text(json.dumps(hy, ensure_ascii=False, indent=2), encoding='utf-8')

print("=== Hypotheses updated ===")
print("  h_david_war_escape: highest-leverage verification step prepended to next_steps")
print("=== 3 new headline_finds added at top ===")
print("  tzvi_hirsh_filip_lineage_verified  (CONFIRMED via Jewish Galicia & Bukovina)")
print("  abraham_schrenzel_lineage_verified (CONFIRMED via Wikipedia + JewishEncyclopedia)")
print("  goldfischer_skole_research_thread  (LEAD)")
print(f"=== build_version: {rc['build_version']} ===")
