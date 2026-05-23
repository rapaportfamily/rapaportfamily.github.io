# RETRACTION — Ben-Zion Rappaport philosopher misidentification

**Date**: 2026-05-23
**Trigger**: Doron's pushback after I built up a large speculative narrative.
**Affected commits**: T36 (7ee3b72), T37 (1c8131b)
**Affected entries**: p_berisz_first_wife_zmigrod, p_moshe_hacohen_rappoport, p_sarah_mahler, p_mordechai_mahler; pl_nowy_sacz, pl_zmigrod (kept as places, removed from Berisz's biography); doc_tarnow_yizkor_berisz_biography, doc_nowy_sacz_yizkor_berisz, doc_berisz_last_letter_1942, doc_berisz_published_books.

## What I claimed

Based on Tarnów + Nowy Sącz Yizkor Books, I identified our Berisz Rapaport (1884 Tarnów) with **Ben-Zion Rappaport, the published Hebrew philosopher** — author of *Consciousness and Reality* (1924), *Thinkers and Logic* (1936), *Nature and Spirit* (1953 posthumous, Mossad Bialik Jerusalem). Built a whole storyline: mother died at age 3, family moved to Nowy Sącz, sister Sarah Mahler arranged a first marriage in Żmigród, son Moshe Hacohen Rappoport, deported from Sącz ghetto to Bełżec August 1942.

## What proves it wrong

**Lusia's memoir, page 23-24 (Hebrew, written by Lusia Rapaport herself, primary family source)**:

> עם חמה וחמתה בפשמשל

= "With her father-in-law and her mother-in-law in Przemyśl"

> לוסיה ושמעון הקטן נסעו לחמה וחמתה שהתגוררו בעיר פשמשל

= "Lusia and little Shimon traveled to her father-in-law and mother-in-law who lived in the city of Przemyśl."

> צחוק הגורל: הם נותרו תחת שלטון גרמני וכעבור חודשים מספר הרגו הללו את חמה בהאשימם אותו שהניח, כביכול, פצצה על מסילת הברזל שבקירבתה התגוררו

= "Irony of fate: they remained under German rule and after several months the latter killed her father-in-law, accusing him of allegedly placing a bomb on the railway near which they lived."

So our Berisz:
- Lived in **Przemyśl** in 1939, with Rebeka and David's grandmother
- Was killed by Germans in **Przemyśl** on a fabricated railway-bomb charge, in late 1941 or 1942

This contradicts the Yizkor philosopher's documented life — Kraków Hebrew Gymnasium teacher, deported from **Nowy Sącz** ghetto to **Bełżec**.

A search of the full Lusia memoir for keywords found ZERO mentions of: Tarnów-as-residence, Nowy Sącz, Kraków, Hebrew Gymnasium, philosopher, books. If Berisz had been the philosopher Ben-Zion Rappaport, the memoir would have referenced his published works — that detail is too prominent to omit.

## Why the false-positive happened

Both Berisz and the Yizkor's Ben-Zion shared three identifiers: Tarnów + 1884 + teacher father. I treated this as definitive when it was coincidental. **Tarnów's Jewish community in the 1880s included multiple Rapaport families. Two Benzions could easily have been born in Tarnów in 1884 with teacher fathers — the Yizkor's "R. Moshe Gorlitzer" (toponym = of Gorlice) and our "Mojżesz Saul Rapaport" are likely different men.**

I also failed to cross-check against Lusia's memoir — a primary family source already in our database that directly contradicts the Yizkor narrative. I should have run this check before building the storyline.

## What's actually known about Berisz (primary documents + memoir)

| Fact | Source |
|---|---|
| Born Tarnów 6 Aug 1884, registered as "Benzion" | Tarnów birth cert row 323 (Basia) |
| Father: Mojżesz Saul Rapaport, private teacher in Tarnów | Tarnów birth cert |
| Mother: Rywka Schiff, daughter of Michał + Cywie Schiff of Tarnów | Tarnów birth cert |
| Hebrew name Issachar Berish | Edward Gelles "Griffel of Nadworna" |
| Married Rebeka Griffel of Nadwórna ~1908-10 | Gelles pedigree entry #8 + David's 1911 Nadwórna birth cert |
| Family in Stanisławów Kościuszki 4 by 1924, passport application | 1924 Świadectwo kwalifikacyjne |
| Children: David Mendel (b.1911 Nadwórna), Lota (b.~1916) | 1924 passport + David's birth cert |
| In Przemyśl by ~1910 (per Basia 13-May letter "Bernard Rapaport appears in Przemyśl records") + by 1939 (per memoir) | Basia + memoir |
| Killed in Przemyśl by Germans on railway-bomb charge, late 1941 / early 1942 | Lusia memoir page 24 |
| Kohen | family tradition |

No connection to Hebrew Gymnasium, philosophy books, Nowy Sącz, or Bełżec.

## What I've changed in the data

- `p_berisz.death`: now Przemyśl (was Bełżec), sourced to memoir page 24, with the false hypothesis recorded in an `earlier_hypothesis` field.
- `p_berisz.note_en`: rewritten to use only what's documented + retract the philosopher identification.
- `p_berisz.children_ids`: David + Lota only (removed Moshe Hacohen).
- `p_berisz.works`: removed entirely (the 3 books were not his).
- `p_mojzesz_saul_rapaport`: stripped of the "R. Moshe Gorlitzer" identification, the Gorlice origin claim, and the rabbinic-dynasty descent claim (latter downgraded to family-oral confidence).
- `p_berisz_first_wife_zmigrod`, `p_moshe_hacohen_rappoport`, `p_sarah_mahler`, `p_mordechai_mahler`: status set to "WITHDRAWN" with explanatory note.
- `doc_tarnow_yizkor_berisz_biography`, `doc_nowy_sacz_yizkor_berisz`, `doc_berisz_last_letter_1942`, `doc_berisz_published_books`: status set to "WITHDRAWN_AS_FAMILY_DOC".
- `pl_nowy_sacz`, `pl_zmigrod`, `pl_belzec`, `pl_gorlice`: places kept (they are real places) but Berisz's biography no longer references them as part of his life.

## Lessons for future research

1. **Lusia's memoir is the primary family source** — always cross-check Yizkor claims against it. If memoir doesn't mention something extraordinary (like "Berisz published 3 philosophy books"), assume it didn't happen.
2. **Coincidence on three markers is not identification.** Tarnów + 1884 + teacher father is suggestive but not proof. The standard for confirming a Yizkor identification should be: explicit name match + at least one other unique marker (specific address, named relative, dated event) that ties to our primary documents.
3. **Build hypotheses, don't commit them as facts until cross-verified.** I wrote the philosopher identification into `p_berisz.note_en` as if confirmed. Should have used `confidence: hypothesis` and a separate research-track entry.

## Open follow-up

The actual research question — **how did Berisz end up in Przemyśl, and what did he do for a living there?** — remains open. Basia noted on 13 May that a "Bernard Rapaport" appears in Przemyśl records around 1910, suggesting the family had a long-established Przemyśl presence. This is consistent with the memoir: by 1939 Berisz, Rebeka, and David's grandmother were settled there. The 1924 Stanisławów residence may have been a temporary location.

Suggested next steps:
- Basia: search Przemyśl Jewish records 1910-1939 for Berisz/Bernard Rapaport — birth/marriage/property/business
- Search Yad Vashem for any Pages of Testimony for Berisz Rapaport, Przemyśl, 1941-42
- File a new Page of Testimony for Berisz with the memoir's details: Przemyśl, ~late 1941/early 1942, fabricated bomb charge
- Investigate David's grandmother who was in Przemyśl: most likely Rywka Schiff (Berisz's mother, would have been ~75-80 in 1939) — though it could be Sara Chajes (Rebeka's mother)
