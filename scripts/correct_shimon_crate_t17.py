"""T17: CORRECT the Shimon hypothesis using primary-source memoir evidence.

The T14/T16 inference that Shimon was hidden in a Lwów Catholic convent was
WRONG. The memoir (Chapter D, pages 30-46) tells the actual story:

  - In Nadwórna 1941 Shimon was first taken into the ghetto with extended family.
  - Lusia's sister-in-law LOTA hid Shimon in the Lwów ghetto for a period.
  - The HORMAK family (gentile Nadwórna neighbours) smuggled Shimon from
    Nadwórna to Lwów; the sister of Hormak hosted Lusia overnight.
  - Lusia retrieved Shimon from the Lwów ghetto (then briefly open).
  - From that point Shimon lived with Lusia at Legionów 24 — HIDDEN IN A
    CRATE (70 cm × 1.50 m) during the day, sleeping with his mother at
    night. He never saw sunlight for years; his complexion went white and
    pale. When neighbours visited, Lusia operated a phonograph atop the
    crate so music masked his sounds. This continued through 1944.

The Catholic-convent / Żegota-placement hypothesis was a reasonable
INFERENCE before reading the memoir carefully, but it does not match what
Lusia herself recorded. The memoir is decisive.

This script:
1. CORRECTS the shimon_hidden_separately_lwow_convent card → renames to
   shimon_crate_at_legionow_24 + replaces content with the memoir-derived
   true story, citing specific memoir pages.
2. UPDATES h_leah_shimon_survival → RESOLVED via memoir.
3. Adds memoir source URL/page references for an LLM narrator.
4. Bumps build_version.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC_PATH = REPO / 'platform' / 'data' / 'research_center.json'
HY_PATH = REPO / 'platform' / 'data' / 'hypotheses.json'

rc = json.loads(RC_PATH.read_text(encoding='utf-8'))
hy = json.loads(HY_PATH.read_text(encoding='utf-8'))

# ── 1) Replace shimon_hidden_separately_lwow_convent with the truth ──
hf = next(s for s in rc['sections'] if s['id'] == 'headline_finds')
corrected = {
    "id": "shimon_crate_at_legionow_24",
    "title_en": "📦 CORRECTED — Shimon survived 1941-44 HIDDEN IN A CRATE at Legionów 24, NOT in a convent",
    "title_he": "📦 תוקן — שמעון שרד 1941-44 מוסתר בארגז בלגיונוב 24, ולא במנזר",
    "status": "confirmed",
    "summary_en": (
        "PRIMARY-SOURCE CORRECTION via the memoir itself (Chapter D, pages 30-46). The "
        "earlier inference that Shimon was hidden in a Lwów Catholic convent was WRONG. "
        "What actually happened, in Lusia's own words: (1) In Nadwórna, when the ghetto "
        "was established, Lusia refused to enter — but Shimon was first hidden by the "
        "HORMAK family, gentile neighbours who traded with the Jews. (2) Lusia's "
        "sister-in-law LOTA Rapaport hid Shimon for a period inside the Lwów ghetto. "
        "(3) When rumours spread that the Germans would soon execute the children, "
        "the Hormaks smuggled Shimon out of the Lwów ghetto and brought him to Lusia "
        "(while the ghetto was still briefly open to commerce). (4) From that day "
        "until liberation, Shimon lived with Lusia at Legionów 24 inside a CRATE 70 cm × "
        "1.50 m. Lusia left food in it before work; he slept with his mother at night. "
        "When neighbours visited, Lusia placed a phonograph on the crate and music "
        "burst forth to mask his sounds. He never saw sunlight for years — his "
        "complexion went white and pale. He emerged after the July 1944 Soviet liberation."
    ),
    "summary_he": (
        "תיקון מהמקור הראשוני — היומן עצמו (פרק ד', עמ' 30-46). ההסקה הקודמת שלפיה "
        "שמעון הוסתר במנזר קתולי בלבוב הייתה שגויה. מה שקרה באמת, בלשונה של "
        "לוסיה: (1) בנדבורנה, כשהוקם הגטו, לוסיה סירבה להיכנס אליו — אך שמעון "
        "הוסתר תחילה על-ידי משפחת הורמק, שכנים גויים שסחרו עם היהודים. (2) "
        "גיסתה של לוסיה, לוטה רפפורט, הסתירה את שמעון תקופה מסוימת בתוך גטו לבוב. "
        "(3) כאשר התפשטו שמועות שהגרמנים עומדים להוציא להורג את הילדים בקרוב, "
        "משפחת הורמק הבריחה את שמעון מגטו לבוב והביאה אותו ללוסיה (בעוד הגטו "
        "עדיין היה פתוח חלקית למסחר). (4) מאותו יום ועד השחרור התגורר שמעון עם "
        "לוסיה בלגיונוב 24 בתוך ארגז של 70 ס\"מ × 1.50 מ'. לוסיה השאירה לו אוכל "
        "בארגז לפני שיצאה לעבודה; הוא ישן עם אמו בלילה. כאשר באו שכנים לבקר, "
        "לוסיה הניחה פטיפון על גג הארגז ומוזיקה בקעה ממנו כדי להסוות את קולותיו. "
        "הוא לא ראה את אור השמש במשך שנים — עורו הלבין והחוויר. הוא יצא מהארגז "
        "לאחר שחרור לבוב על-ידי הסובייטים ביולי 1944."
    ),
    "quote_en": (
        "Shimon lived with his mother and spent entire days alone in a crate whose "
        "dimensions were 70 cm × 1.50 m. The crate was his dwelling and his place of "
        "safety. ... At night he slept with his mother. In the evening, when neighbors "
        "came to visit Lusia, she would operate the phonograph that was placed on the "
        "box and music would burst forth from it. ... From the outside, his complexion "
        "was white and pale, since he did not see sunlight for many long years."
    ),
    "source": "Lusia Rapaport, 'Sipura shel Lusia' (The Story of Lusia), ed. Moshe Guter — Chapter D, pages 30, 32-33, 36-38, 44-46",
    "urls": []
}

existing_ids = {c['id'] for c in hf['cards']}
# Remove the old erroneous card if present, and put corrected at top
hf['cards'] = [c for c in hf['cards'] if c['id'] != 'shimon_hidden_separately_lwow_convent']
if corrected['id'] not in existing_ids:
    hf['cards'].insert(0, corrected)

# Add a second card documenting the convent research that turned out not to apply
convent_context = {
    "id": "lwow_convents_researched_not_applicable",
    "title_en": "📚 Lwów Catholic convents researched as a possible alternative — NOT how Shimon actually survived",
    "title_he": "📚 נחקרו מנזרים קתוליים בלבוב כאפשרות חלופית — אך לא כך שרד שמעון בפועל",
    "status": "lead",
    "summary_en": (
        "Background research established that several Lwów-area religious networks "
        "sheltered Jewish children 1941-1944: Albertine Sisters at Persenkówka 66; "
        "Studite Sisters under Metropolitan Andrey Sheptytsky and abbess Mother "
        "Iosyfa (Olena Viter), saving 150-200 Jews including rabbis' sons Adam "
        "Daniel Rotfeld and Leon Chameides; Sacré-Cœur Sisters; Franciscan Sisters of "
        "the Family of Mary (Mother Matylda Getter — ~500 Jewish children nationally). "
        "Żegota's Lwów branch (chair Władysława Choms, the 'Angel of Lwów') placed "
        "children into these institutions from her base at ul. Nabielaka 14 — "
        "walking distance from Legionów 24. The placement pipeline is documented "
        "in Choms's own Yad Vashem M.31 file (1966). HOWEVER — the family memoir "
        "(see corrected card above) makes clear Shimon was NOT placed in any of "
        "these institutions; he was hidden in a crate at his mother's apartment. "
        "The convent path is preserved here as historical context for the LLM "
        "narrator and as a reminder that the Lwów-area Jewish survival options were "
        "broader than the family chose."
    ),
    "summary_he": (
        "מחקר רקע איתר מספר רשתות דתיות באזור לבוב שהסתירו ילדים יהודים 1941-1944: "
        "האחיות האלברטיניות בפרסנקובקה 66; האחיות הסטודיטיות בהנהגת המטרופוליטן "
        "אנדריי שפטיצקי והאם יוסיפה (אולנה ויטר), שהצילו 150-200 יהודים כולל בני "
        "רבנים אדם דניאל רוטפלד ולאון חמיידס; אחיות לב-ישו הקדוש (Sacré-Cœur); "
        "אחיות פרנציסקאניות של משפחת מרים (האם מטילדה גטר — כ-500 ילדים יהודים "
        "ארצית). סניף ז'גוטה בלבוב (יו\"ר ולדיסלבה חומס, 'מלאך לבוב') הכניס ילדים "
        "למוסדות אלה ממרכז פעולתה ברחוב נביילקה 14 — במרחק הליכה מלגיונוב 24. "
        "אבל — היומן המשפחתי (ראה את הכרטיס המתוקן לעיל) מבהיר ששמעון לא הוכנס "
        "לאף אחד מהמוסדות הללו; הוא הוסתר בארגז בדירת אמו. מסלול המנזר נשמר כאן "
        "כהקשר היסטורי לנרטור ה-LLM ותזכורת שאפשרויות ההישרדות באזור לבוב היו "
        "רחבות יותר מהבחירה שעשתה המשפחה."
    ),
    "source": "Polscy Sprawiedliwi, Lviv Center, Yad Vashem M.31 series — research summarized in dossier 23",
    "urls": [
        "https://sprawiedliwi.org.pl/en/stories-of-rescue/story-wladyslawa-choms",
        "https://lia.lvivcenter.org/en/themes/reherit/zegota/",
        "https://lia.lvivcenter.org/en/themes/reherit/church/",
        "https://www.yadvashem.org/righteous/resources/rescue-of-jewish-children-in-polish-convents.html",
        "https://en.wikipedia.org/wiki/Klymentiy_Sheptytsky"
    ]
}
if convent_context['id'] not in {c['id'] for c in hf['cards']}:
    # Insert just below the corrected card
    hf['cards'].insert(1, convent_context)

# ── 2) Update h_leah_shimon_survival → RESOLVED ───────────────────────
hyps = hy['hypotheses'] if isinstance(hy, dict) and 'hypotheses' in hy else hy
for h in hyps:
    if h.get('id') == 'h_leah_shimon_survival':
        h['status'] = 'resolved'
        h['confidence'] = 'confirmed'
        h['verdict'] = {
            'en': (
                "RESOLVED via the memoir itself (Chapter D, pages 30-46). Shimon was NOT placed in a "
                "convent. Sequence: (1) Hormak family (gentile Nadwórna neighbours) helped move Shimon; "
                "(2) Lota Rapaport (David's sister) hid him in the Lwów ghetto for a period; "
                "(3) Hormaks smuggled him out of the Lwów ghetto and brought him to Lusia; "
                "(4) Shimon then lived in a 70 cm × 1.50 m crate inside Lusia's apartment at "
                "Legionów 24 from then until July 1944 Soviet liberation. Lusia operated a phonograph "
                "to mask his sounds when visitors came; he never saw sunlight; his complexion went "
                "white and pale. David Memek lived separately in Lwów under disguise (grew a "
                "mustache, changed his hair) and worked on railroad-track construction with a friend "
                "named Pesach — both circumcised Jews passing as gentiles, sewing up their members "
                "to bathe with the gentile crews."
            ),
            'he': (
                "נפתר באמצעות היומן עצמו (פרק ד', עמ' 30-46). שמעון לא הוכנס למנזר. רצף האירועים: "
                "(1) משפחת הורמק (שכנים גויים בנדבורנה) עזרה להעביר את שמעון; (2) לוטה רפפורט (אחותו "
                "של דוד) הסתירה אותו בגטו לבוב תקופת מה; (3) הורמקים הבריחו אותו מגטו לבוב והביאו "
                "אותו ללוסיה; (4) משם והלאה התגורר שמעון בארגז של 70 ס\"מ × 1.50 מ' בתוך דירת לוסיה "
                "בלגיונוב 24, עד שחרור לבוב על-ידי הסובייטים ביולי 1944. לוסיה הפעילה פטיפון "
                "להסוות את קולותיו כאשר באו אורחים; הוא לא ראה את אור השמש; עורו הלבין והחוויר. "
                "דוד ממק התגורר בלבוב בנפרד תחת תחפושת (הצמיח שפם, שינה את תספורתו) ועבד בהנחת "
                "מסילות רכבת עם חבר בשם פסח — שניהם יהודים נימולים שעברו כגויים, ותפרו את איבריהם "
                "כדי להתקלח עם הצוותים הגויים."
            )
        }
        # Replace evidence_for + evidence_against
        h['evidence_for'] = [
            "Memoir Chapter D pages 36-38: Lusia retrieves Shimon from the Lwów ghetto via Hormak family",
            "Memoir Chapter D page 38: 'All that time he lived with Lucia's sister-in-law, Lota, in the ghetto' (before Lusia retrieved him)",
            "Memoir Chapter D pages 44-46: 'Shimon and the Crate' chapter — explicit description of the 70cm × 1.50m crate, the phonograph, the sunless skin",
            "Memoir Chapter D page 46: David Memek lived separately, sewed circumcision to bathe with gentiles"
        ]
        h['evidence_against'] = []
        h['next_steps'] = [
            "Cross-reference with Shimon's own testimony if one survives (he died — exact date TBD)",
            "Polscy Sprawiedliwi: search for any post-war recognition of the Hormak family of Nadwórna as Righteous Among the Nations (memoir says they helped smuggle and feed the family — they qualify)",
            "Lota Rapaport — find her in Lwów ghetto records (Yad Vashem)"
        ]
        break

# ── 3) Bump build_version ────────────────────────────────────────────
rc['build_version'] = "2026-05-21-T17-memoir-corrects-shimon-crate"

RC_PATH.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding='utf-8')
HY_PATH.write_text(json.dumps(hy, ensure_ascii=False, indent=2), encoding='utf-8')

print("=== Shimon CORRECTED via memoir primary source ===")
print("  Old card 'shimon_hidden_separately_lwow_convent' REMOVED")
print("  New card 'shimon_crate_at_legionow_24' added at top of headline_finds")
print("  Context card 'lwow_convents_researched_not_applicable' added below")
print("=== Hypothesis h_leah_shimon_survival: RESOLVED ===")
print(f"=== build_version: {rc['build_version']} ===")
