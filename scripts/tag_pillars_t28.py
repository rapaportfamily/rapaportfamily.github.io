"""T28: Tag every headline_finds card with its research pillar.

Three-column research framework (Doron's directive 2026-05-21):
  📖 from_book          — memoir-derived; enriched with data/visuals
  ⚖️  memoir_vs_history — memoir + historical context together; gentle nuancing
  🔍 independent        — facts beyond the memoir; archival findings on their own
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC = REPO / "platform" / "data" / "research_center.json"
rc = json.loads(RC.read_text(encoding="utf-8"))
hf = next(s for s in rc["sections"] if s["id"] == "headline_finds")

# Each card -> pillar
PILLAR = {
    # Pillar 1: from the book (memoir-supported + visually enriched)
    "bolechow_yizkor_naming":              "from_book",   # memoir confirmed by 1957 Yizkor
    "david_lusia_death_dates_confirmed":   "from_book",   # memoir + cemetery records
    "bolechow_yizkor_weitzner_lone_mention": "from_book", # Yizkor confirms Eli Weitzner per memoir
    "achwa_beitar_hachshara":              "from_book",   # confirms David's Betar context
    "test_was_david_a_kohen":              "from_book",   # confirms family Kohen tradition

    # Pillar 2: memoir vs history (gentle nuancing OR mutual confirmation)
    "shimon_testimony_lacuna_and_dakar_clarification": "memoir_vs_history",  # Dakar nuance
    "eric_griffel_memoir_corrects_zygmunt_anders":     "memoir_vs_history",  # Zygmunt-Anders nuance
    "theodor_herzl_voyage_details":                    "memoir_vs_history",  # ship history added
    "eli_weitzner_taniawa_forest_inferred":            "memoir_vs_history",  # date inferred from history
    "shimon_crate_at_legionow_24":                     "memoir_vs_history",  # corrected from memoir
    "lwow_convents_researched_not_applicable":         "memoir_vs_history",  # context that turned out not to apply
    "lusia_birth_date_confirmed_1913":                 "memoir_vs_history",  # birth date verified
    "lota_us_resident_scheme_lwow":                    "memoir_vs_history",  # historical scheme + memoir detail
    "david_soviet_exile_route_hypothesis":             "memoir_vs_history",  # hypothesis from history filling memoir gap
    "tzvi_hirsh_filip_lineage_verified":               "memoir_vs_history",  # memoir tradition + historical record

    # Pillar 3: independent evidence (facts beyond the book)
    "isak_goldfischer_skole_1927_lvov_ghetto":         "independent",
    "hormak_family_righteous_nomination":              "independent",
    "hormak_polscy_sprawiedliwi_verified_null":        "independent",
    "lota_rapaport_archive_is_her_memorial":           "independent",
    "lota_husband_unnamed_research_thread":            "independent",
    "playwright_yad_vashem_null_finding":              "independent",
    "maria_cieslik_identification_opens":              "independent",
    "pensjonat_bristol_weiss_family":                  "independent",
    "prof_ronen_rapaport_academic_profile":            "independent",
    "hadas_rapaport_linkedin_lead":                    "independent",
    "david_actionable_search_targets":                 "independent",
    "david_indeks_jdc_manual_search_instructions":     "independent",
    "abraham_schrenzel_lineage_verified":              "independent",  # external scholarship
    "goldfischer_skole_research_thread":               "independent",
    "goldfischer_stryj_circle_etymology":              "independent",
    "goldfischer_marin_aliyah_path":                   "independent",
    "nadworna_yizkor_mining_complete":                 "independent",  # external Yizkor mining

    # Additional cards
    "david_primary_documents_trail":                   "independent",
    "basia_1938_auction_notice":                       "independent",  # Basia's archival find
    "basia_zygmunt_griffel_kopernika_5":               "independent",
    "goldfischer_weitzner_school_circle":              "memoir_vs_history",  # adds context to family connection
    "griffel_chajes_dynasty":                          "independent",  # external genealogical research
    "nadworna_first_betar":                            "from_book",   # confirms memoir's Betar context
    "foresta_zetperol":                                "independent",  # external Pinkas finding
    "glesinger_timber_aryanised":                      "independent",  # external research
    "eric_griffel_adst_oral_history":                  "independent",
}

# Apply tags
tagged = 0
untagged = []
for c in hf["cards"]:
    cid = c["id"]
    if cid in PILLAR:
        c["pillar"] = PILLAR[cid]
        tagged += 1
    else:
        untagged.append(cid)

# Also add pillar intro to the section
hf["intro_en"] = (
    "Our research follows a three-column framework. Pillar 1 (📖 from the book) "
    "enriches Lusia's 1986 memoir with data and visuals. Pillar 2 (⚖️ memoir vs "
    "history) reconciles her account with external records, honoring both. "
    "Pillar 3 (🔍 independent evidence) brings facts from archives the memoir "
    "could not include. We hold these in balance — respecting the family voice "
    "and pursuing historical accuracy."
)
hf["intro_he"] = (
    "המחקר שלנו פועל לפי מסגרת של שלוש עמודות. עמוד 1 (📖 מהספר) מעשיר את היומן "
    "של לוסיה משנת 1986 בנתונים ובוויזואלים. עמוד 2 (⚖️ יומן מול היסטוריה) מיישב "
    "את סיפורה עם רישומים חיצוניים, מכבד את שניהם. עמוד 3 (🔍 ראיות עצמאיות) "
    "מביא עובדות מארכיונים שהיומן לא יכול היה לכלול. אנו אוחזים בשלושתם באיזון — "
    "מכבדים את קול המשפחה ופועלים לדיוק היסטורי."
)

rc["build_version"] = "2026-05-21-T28-three-pillars-framework"
RC.write_text(json.dumps(rc, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"=== Tagged {tagged} cards across 3 pillars ===")
print()
print(f"Untagged ({len(untagged)}):")
for u in untagged:
    print(f"  {u}")
print()
print(f"=== build_version: {rc['build_version']} ===")
