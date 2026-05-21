# Sonnet 4.5 translation pass — improvements over Haiku 4.5 (2026-05-21)

26 critical pages were re-translated with **Claude Sonnet 4.5** to verify and improve the original Haiku 4.5 translations. Cost: $0.39 total. Both versions are now stored in `memoir_pages.json` (`english` = Sonnet, `english_haiku` = original).

## New facts surfaced by Sonnet

### New people to add to people.json

1. **"Doner"** — German/Austrian surname mentioned p.48. Possibly Lusia's employer or supervisor (the German owner of the shop where she worked using false papers). Worth investigating.

2. **Kramer (dentist from Nadwórna)** — p.48. Lusia encounters his daughter in Lwów. The Kramer dentist was killed by Germans after gold was found in his home. A neighbor or community member, not family but part of the Nadwórna Jewish community story.

3. **A second Shimon (NOT Lusia's son)** — p.45. A different Jewish child named Shimon hidden by his mother (not Lusia) in a wooden crate measuring 70 cm × 1.50 m in the shop where Lusia worked. Separate from Lusia's son Shimon b.1937. Important to distinguish — the memoir uses the same name for two different children.

### New places to investigate

1. **"Yaichor" (ייחור)** — p.56. Possibly a small dwelling/room or specific type of housing near the factory. Sonnet flagged as uncertain. Could be transliterated from Polish.

2. **"Yeplatsovka" (יפלאצבקה)** — p.56. Place name near the market in Lwów. Possibly a neighborhood or market area. Could be Polish "ul. Pełczyńska" or similar — needs research.

### Confirmed historical context

- **Page 17 "Moshina"** — Sonnet flagged as "small resort town in the USSR" (uncertain). Our prior research (hypothesis h_mosina_muszyna) ALREADY resolved this to **Muszyna**, a Polish resort town near Krynica. Confirmed by the memoir itself on other pages.

- **Page 7 biblical reference** — Hebrew "הרצחת וגם ירשת?!" = direct quote from **1 Kings 21:19** (Elijah's accusation to Ahab after he stole Naboth's vineyard: "Have you murdered and also inherited?"). Lusia uses this as moral indictment of the Nazis. Haiku translated literally but missed the biblical reference.

- **Page 45 shop type** — confirmed as a **millinery (hat shop)** in Lwów 1943-44. Polish artisan goods, art objects, wooden carvings. Sonnet notes the young Polish girl who came in was likely Armia Krajowa (Polish resistance).

- **Page 42 box-hiding method** — confirmed: Lusia hid her son Shimon in a wooden crate normally used for storing vegetables, modified by removing boards attaching back to wall. Sonnet provides much more mechanical detail than Haiku.

- **Page 50 documents** — confirmed that Maria Ciccelik's birth certificate, which Lusia used as the basis for her false identity, passed multiple Gestapo inspections without flaw.

- **Page 62 Katowice + JDC** — Sonnet correctly identifies "ריפטראציה" as the post-WWII organized repatriation of Polish citizens from Soviet-annexed territories. "Joint" = JDC. Katowice was a major transit point for Jewish refugees post-WWII.

### Translation upgrades summary

The 10 most divergent pages (similarity < 0.4 between Haiku and Sonnet):

| Page | Haiku→Sonnet sim | Key improvement |
|---|---|---|
| 17 | 0.08 | More context about white wedding + Soviet exile circumstances |
| 3 | 0.14 | Identifies Kriminalpolizei + biblical resonance of mass-murder scenes |
| 62 | 0.14 | Joint (JDC), Katowice transit, repatriation terminology |
| 42 | 0.17 | Detailed mechanical description of the box-hiding for Shimon |
| 7 | 0.20 | 1 Kings 21:19 biblical reference identified |
| 45 | 0.24 | Millinery + Armia Krajowa + second-Shimon clarification |
| 56 | 0.32 | Two new place names flagged ("Yaichor" + "Yeplatsovka") |
| 50 | 0.35 | Maria Ciccelik documents — multi-inspection survival detail |
| 48 | 0.37 | NEW people: Doner + Kramer dentist of Nadwórna |
| 63 | 0.38 | Aliyah immigration framework + family-split decision context |

## Action items

1. Add Doner + Kramer-dentist to people.json (as community-of-Nadwórna entries, not family)
2. Research "Yaichor" and "Yeplatsovka" Lwów place names — may be Polish street/neighborhood names
3. Cross-reference p.7 biblical 1 Kings 21:19 reference in memoir_facts.json
4. Update memoir_timeline_verified.json with the new contextual notes from Sonnet's translator_notes
