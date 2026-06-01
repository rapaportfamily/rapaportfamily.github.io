"""Add the three Tarnów marriage records' findings to people.json + places.json."""
import json

with open('platform/data/people.json', encoding='utf-8') as f:
    d = json.load(f)

# Update Freida Amalia — second marriage 1919
for p in d['people']:
    if p.get('id') == 'p_freida_amalia_rapaport':
        p['note_en'] = (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Sibling of Berisz Rapaport. Born ~November '
            '1889 in Radomyśl Wielki (the descendants tree gives 1888; her 1919 second-marriage record gives '
            'age 29 years 7 months in June 1919 → ~Nov 1889). She married TWICE: a first husband (likely a '
            'Nussbaum, since her son took the Nussbaum surname) who died by early 1919 — possibly in WWI — '
            'leaving her to raise their newborn son Zwi Ayalon Nussbaum (b. 7 May 1919 Przemyśl); then she '
            'remarried Markus Elias Kleinbaum in Tarnów on 8 June 1919 (just one month after Zwi\'s birth), '
            'per entry 40 of the Tarnów Jewish marriage register held at the Archiwum Narodowe w Krakowie / '
            'Tarnów branch (CC discovered via Claude vision OCR, 2026-06-01). Died 1942 in Przemyśl per the '
            'family-built descendants tree. Documented children: Zwi Ayalon Nussbaum (b.1919 Przemyśl, '
            'survived to Israel, d.2001 Haifa); the descendants tree also shows Michael Rosenfeld (b.1929) '
            'and Rachel Rosenfeld (b.1930) both killed Przemyśl 1944 — these would be grandchildren via a '
            'Rosenfeld daughter, OR children of a third marriage; relationship not yet certain.'
        )
        p['facts'] = [
            {
                'key': '1919_second_marriage',
                'value': '8 June 1919 in Tarnów — second marriage to Markus Elias Kleinbaum (age 27, also widower, residing at "u domu Bauer in Przemyśl"). Witness rabbi: Josef Chaim Kirschenbaum. Per entry 40 of the 1919 Tarnów Jewish marriage register.',
                'confidence': 'documented',
                'sources': ['doc_freida_amalia_marriage_1919']
            },
            {
                'key': 'first_husband_nussbaum',
                'value': 'Inferred from her son Zwi Ayalon\'s surname Nussbaum at birth (7 May 1919 Przemyśl) — her first husband must have been a Nussbaum. He had died by the time of the 8 June 1919 remarriage. Most likely a WWI casualty.',
                'confidence': 'hypothesis',
                'sources': ['doc_freida_amalia_marriage_1919', 'doc_moses_saul_descendants_tree']
            }
        ]
        p['spouse_ids'] = ['p_nussbaum_first_husband_freida', 'p_markus_elias_kleinbaum']
        break

# Update Jente — second marriage 1920
for p in d['people']:
    if p.get('id') == 'p_jente_rapaport':
        p['note_en'] = (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Sibling of Berisz Rapaport. Born 1887 in '
            'Radomyśl Wielki per the family-built descendants tree (corroborated: her 1920 second-marriage '
            'record states age 33 in December 1920). She married TWICE: a first husband whose name is not '
            'yet documented (she was a widow by 1920); then on 12 December 1920 in Tarnów she remarried '
            'Mendel Eachem Horowitz of Sokal (age 28, kawaler, son of Pinches Horowitz). Per entry 98 of '
            'the 1920 Tarnów Jewish marriage register, which explicitly names her parents as "Moses '
            'Rapaport and Menucha". Subsequent life trajectory not yet documented.'
        )
        p['facts'] = [
            {
                'key': '1920_second_marriage',
                'value': '12 December 1920 in Tarnów — second marriage to Mendel Eachem Horowitz of Sokal (age 28, bachelor, son of Pinches Horowitz). Witness rabbi: Josef Chaim Kirschenbaum. Per entry 98 of the 1920 Tarnów Jewish marriage register. The record explicitly names her parents as "Moses Rapaport and Menucha".',
                'confidence': 'documented',
                'sources': ['doc_jente_marriage_1920']
            },
            {
                'key': 'first_marriage',
                'value': 'Was a widow by December 1920. First husband\'s identity not yet documented.',
                'confidence': 'documented',
                'sources': ['doc_jente_marriage_1920']
            }
        ]
        p['spouse_ids'] = ['p_jente_first_husband_unknown', 'p_mendel_horowitz']
        break

# Update younger Rebeka — first marriage 1923
for p in d['people']:
    if p.get('id') == 'p_rebeka_rapaport_sister':
        p['note_en'] = (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Youngest known sibling of Berisz Rapaport. '
            'Born 1896 in Radomyśl Wielki (per the family-built descendants tree, corroborated: her 1923 '
            'marriage record gives age 27 in September 1923 and explicitly states "urodzona w Radomyślu '
            'Wielkim"). She married Sane Zylberfenig of Płońsk on 4 September 1923 in Tarnów (entry 101 of '
            'the Tarnów Jewish marriage register). The record explicitly names her parents as "Moses '
            'Rapaport and Menucha". The descendants tree notes that she "went to Austria" after the marriage. '
            'NOT to be confused with Berisz\'s wife Rebeka née Griffel of Nadwórna.'
        )
        p['facts'] = [
            {
                'key': '1923_marriage',
                'value': '4 September 1923 in Tarnów — married Sane Zylberfenig of Płońsk (age 34 years 10 months, bachelor, son of Abram + Pesi Zylberfenig of Płońsk). Witnesses: Maier Krak, David Erbg, Israel Marche. Per entry 101 of the 1923 Tarnów Jewish marriage register. The record explicitly names her parents as "Moses Rapaport and Menucha".',
                'confidence': 'documented',
                'sources': ['doc_rebeka_younger_marriage_1923']
            },
            {
                'key': 'subsequent_migration',
                'value': 'Went to Austria (per family-built descendants tree) — date unknown but presumably post-1923 marriage. Could have moved with husband Sane Zylberfenig, or solo.',
                'confidence': 'family_oral',
                'sources': ['doc_moses_saul_descendants_tree']
            }
        ]
        p['spouse_id'] = 'p_sane_zylberfenig'
        break

# Add three new in-law people
NEW_INLAWS = [
    {
        'id': 'p_markus_elias_kleinbaum',
        'primary_name': {
            'en': 'Markus Elias Kleinbaum',
            'he': 'מרקוס אליאש קליינבאום',
            'pl': 'Markus Elias Kleinbaum',
            'fr': 'Markus Elias Kleinbaum'
        },
        'role': 'great_grand_uncle_by_marriage',
        'note_en': (
            'Second husband of Freida Amalia Rapaport (Berisz\'s sister). Married her in Tarnów on 8 June '
            '1919 (entry 40 of the Tarnów Jewish marriage register). Age 27 at marriage → born ~1892. '
            'Was a widower at the time of marriage. Residence noted in document as "u domu Bauer in Przemyśl" '
            '— probable Przemyśl residence after marriage. Further details not yet documented.'
        ),
        'birth': {
            'date': '1892',
            'date_precision': 'estimated_year',
            'confidence': 'estimated',
            'sources': ['doc_freida_amalia_marriage_1919']
        },
        'spouse_id': 'p_freida_amalia_rapaport',
        'facts': []
    },
    {
        'id': 'p_mendel_horowitz',
        'primary_name': {
            'en': 'Mendel Eachem Horowitz',
            'he': 'מנדל הורוויץ',
            'pl': 'Mendel Eachem Horowitz',
            'fr': 'Mendel Eachem Horowitz'
        },
        'role': 'great_grand_uncle_by_marriage',
        'note_en': (
            'Second husband of Jente Rapaport (Berisz\'s sister). Married her in Tarnów on 12 December 1920 '
            '(entry 98 of the Tarnów Jewish marriage register). Age 28 at marriage → born ~1892. Status: '
            'kawaler (bachelor) — first marriage for him. Resident of Sokal (now Sokal/Sokaľ in Lviv Oblast, '
            'Ukraine; pre-WWII in Eastern Galicia). Son of Pinches Horowitz.'
        ),
        'birth': {
            'date': '1892',
            'date_precision': 'estimated_year',
            'place_id': 'pl_sokal',
            'confidence': 'estimated',
            'sources': ['doc_jente_marriage_1920']
        },
        'father_id': 'p_pinches_horowitz',
        'spouse_id': 'p_jente_rapaport',
        'facts': []
    },
    {
        'id': 'p_sane_zylberfenig',
        'primary_name': {
            'en': 'Sane Zylberfenig',
            'he': 'סנה זילברפניג',
            'pl': 'Sane Zylberfenig',
            'fr': 'Sane Zylberfenig'
        },
        'role': 'great_grand_uncle_by_marriage',
        'note_en': (
            'Husband of the younger Rebeka Rapaport (Berisz\'s sister, b.1896 Radomyśl Wielki — not to be '
            'confused with Berisz\'s wife Rebeka née Griffel). Married her in Tarnów on 4 September 1923 '
            '(entry 101 of the Tarnów Jewish marriage register). Age 34 years 10 months at marriage → born '
            '~November 1888. Status: kawaler (bachelor) — first marriage. Born in Płońsk (Polish town '
            'NW of Warsaw). Son of Abram and Pesi Zylberfenig of Płońsk.'
        ),
        'birth': {
            'date': '1888-11',
            'date_precision': 'month',
            'place_id': 'pl_plonsk',
            'confidence': 'documented',
            'sources': ['doc_rebeka_younger_marriage_1923']
        },
        'spouse_id': 'p_rebeka_rapaport_sister',
        'facts': []
    },
    {
        'id': 'p_pinches_horowitz',
        'primary_name': {
            'en': 'Pinches Horowitz',
            'he': 'פנחס הורוויץ',
            'pl': 'Pinches Horowitz',
            'fr': 'Pinches Horowitz'
        },
        'role': 'in_law_grand_relative',
        'note_en': (
            'Father of Mendel Eachem Horowitz (who married Jente Rapaport in Tarnów 1920). Resident of Sokal '
            '(Eastern Galicia, today Ukraine). Per entry 98 of the 1920 Tarnów Jewish marriage register.'
        ),
        'children_ids': ['p_mendel_horowitz'],
        'facts': []
    },
    {
        'id': 'p_nussbaum_first_husband_freida',
        'primary_name': {
            'en': '[unknown given name] Nussbaum (Freida Amalia Rapaport\'s first husband)',
            'he': '[שם פרטי לא ידוע] נוסבאום (בעלה הראשון של פריידה אמליה)',
            'pl': '[nieznane imię] Nussbaum (pierwszy mąż Freidy Amalii)',
            'fr': '[prénom inconnu] Nussbaum'
        },
        'role': 'great_grand_uncle_by_marriage_unverified',
        'note_en': (
            '⚠ INFERRED. First husband of Freida Amalia Rapaport — surname Nussbaum inferred from his son '
            'Zwi Ayalon\'s surname at birth (Nussbaum). Father of Zwi Ayalon Nussbaum (b. 7 May 1919 '
            'Przemyśl). Died by 8 June 1919 (when Freida remarried Kleinbaum). Most likely WWI casualty. '
            'Given name not yet documented.'
        ),
        'spouse_id': 'p_freida_amalia_rapaport',
        'children_ids': ['p_zwi_ayalon_nussbaum'],
        'facts': []
    },
    {
        'id': 'p_jente_first_husband_unknown',
        'primary_name': {
            'en': '[unknown] (Jente Rapaport\'s first husband)',
            'he': '[לא ידוע] (בעלה הראשון של יענטה)',
            'pl': '[nieznany] (pierwszy mąż Jente Rapaport)',
            'fr': '[inconnu] (premier mari de Jente)'
        },
        'role': 'great_grand_uncle_by_marriage_unverified',
        'note_en': (
            '⚠ INFERRED. First husband of Jente Rapaport — his identity is unknown. We know he existed '
            'because Jente is described as a widow (wdowa) in the 1920 Tarnów marriage register (entry 98). '
            'He had died by 12 December 1920.'
        ),
        'spouse_id': 'p_jente_rapaport',
        'facts': []
    }
]

# Insert after p_rebeka_rapaport_sister
for i, p in enumerate(d['people']):
    if p.get('id') == 'p_rebeka_rapaport_sister':
        d['people'][i+1:i+1] = NEW_INLAWS
        break

# Now Moses Saul + Menukha get the corroboration fact
for p in d['people']:
    if p.get('id') == 'p_moses_saul_rapaport':
        p['facts'].append({
            'key': 'three_daughters_marriages_corroborate',
            'value': 'Named as parent in three independent Tarnów marriage registers — entry 40 (1919, Freida Amalia), entry 98 (1920, Jente), entry 101 (1923, younger Rebeka). All three records explicitly state "Moses Rapaport and Menucha" as the bride\'s parents. This is independent primary-source corroboration of the apical couple identified in the family-built descendants tree.',
            'confidence': 'documented',
            'sources': ['doc_freida_amalia_marriage_1919', 'doc_jente_marriage_1920', 'doc_rebeka_younger_marriage_1923']
        })
        break
for p in d['people']:
    if p.get('id') == 'p_menukha':
        p['note_en'] = (
            'Paternal great-great-grandmother of Doron, Dana and Daniel. Wife of Moses Saul Rapaport, '
            'mother of Berisz / Bernard Dov + his four sisters. Name is now corroborated by THREE primary '
            'Tarnów marriage records of her daughters (Freida Amalia 1919, Jente 1920, younger Rebeka 1923) '
            'in addition to her son Berisz\'s 1953 Yad Vashem Page of Testimony. The 1923 Rebeka marriage '
            'record gives the form "Menuchy" (genitive of "Menucha"). Maiden name not yet known.'
        )
        p['facts'] = [{
            'key': 'three_independent_sources',
            'value': 'Named as mother in Yad Vashem PoT 90394 (1953, for Berisz) + Tarnów marriage register entries 40 (1919, Freida), 98 (1920, Jente), 101 (1923, younger Rebeka).',
            'confidence': 'documented',
            'sources': ['doc_bernard_dov_yv_pot', 'doc_freida_amalia_marriage_1919', 'doc_jente_marriage_1920', 'doc_rebeka_younger_marriage_1923']
        }]
        break

with open('platform/data/people.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f'people now: {len(d["people"])}')

# Add places Sokal + Płońsk
with open('platform/data/places.json', encoding='utf-8') as f:
    pl = json.load(f)
NEW_PLACES = [
    {
        'id': 'pl_sokal',
        'names': {'en': 'Sokal (now Sokalʹ, Ukraine)', 'he': 'סוקאל', 'pl': 'Sokal', 'fr': 'Sokal', 'uk': 'Сокаль'},
        'coords': [50.4870, 24.2851],
        'era_context': {
            '1920': 'Town in Eastern Galicia (interwar Lwów Voivodeship, Poland). Home of Mendel Eachem Horowitz, second husband of Jente Rapaport (1920 marriage in Tarnów).'
        },
        'note_en': 'Home of the Horowitz family who married into our paternal line (Mendel × Jente Rapaport, 1920).'
    },
    {
        'id': 'pl_plonsk',
        'names': {'en': 'Płońsk, Poland', 'he': 'פלוצק', 'pl': 'Płońsk', 'fr': 'Płońsk'},
        'coords': [52.6242, 20.3729],
        'era_context': {
            '1888': 'Town in central Poland NW of Warsaw, Mazovian Voivodeship. Home of the Zylberfenig family who married into our paternal line (Sane × younger Rebeka Rapaport, 1923).'
        },
        'note_en': 'Home of the Zylberfenig family. Sane Zylberfenig (b. Nov 1888 Płońsk, son of Abram + Pesi) married Berisz\'s sister Rebeka in Tarnów 1923.'
    }
]
pl['places'].extend(NEW_PLACES)
with open('platform/data/places.json', 'w', encoding='utf-8') as f:
    json.dump(pl, f, ensure_ascii=False, indent=2)
print(f'places now: {len(pl["places"])}')

# Add the three new doc records
with open('platform/data/documents.json', encoding='utf-8') as f:
    docs = json.load(f)
NEW_DOCS = [
    {
        'id': 'doc_freida_amalia_marriage_1919',
        'file_pages': ['1919 Nussbaum Rapaport T.jpg'],
        'kind': 'image',
        'type': 'marriage_record',
        'primary_language': 'pl',
        'title': {
            'en': "Marriage register Tarnów 1919, entry 40 — Freida Amalia Rapaport (widow) × Markus Elias Kleinbaum, 8 June 1919",
            'he': "תעודת נישואין טרנוב 1919, רשומה 40 — פריידה אמליה רפפורט (אלמנה) × מרקוס אליאש קליינבאום, 8 ביוני 1919",
            'pl': "Akt małżeństwa Tarnów 1919, poz. 40 — Freida Amalia Rapaport (wdowa) × Markus Elias Kleinbaum, 8.06.1919",
            'fr': "Acte de mariage Tarnów 1919, n° 40"
        },
        'source_archive': 'Archiwum Narodowe w Krakowie, Oddział w Tarnowie — Tarnów Jewish marriage register, page including entries 40-42',
        'decoded_fields': {
            'entry_number': 40,
            'date': '8 June 1919, Tarnów',
            'bride': 'Freida Amalia Rapaport, wdowa (widow), age 29 years 7 months',
            'groom': 'Markus Elias Kleinbaum, widower, age 27, "u domu Bauer in Przemyśl"',
            'witness_rabbi': 'Josef Chaim Kirschenbaum, rabbi in Tarnów'
        },
        'summary': {
            'en': "Second marriage of Berisz's sister Freida Amalia Rapaport. Read via Claude vision OCR (Tesseract handled handwriting poorly). Confirms her widowed status as of June 1919 — her first husband (likely a Nussbaum, since her son Zwi Ayalon kept that surname) had died by then, possibly in WWI."
        },
        'related_people': ['p_freida_amalia_rapaport', 'p_markus_elias_kleinbaum'],
        'status': 'verified'
    },
    {
        'id': 'doc_jente_marriage_1920',
        'file_pages': ['1920 Horowitz Rapaport T.jpg'],
        'kind': 'image',
        'type': 'marriage_record',
        'primary_language': 'pl',
        'title': {
            'en': "Marriage register Tarnów 1920, entry 98 — Jente Rapaport (widow) × Mendel Horowitz of Sokal, 12 December 1920",
            'he': "תעודת נישואין טרנוב 1920, רשומה 98 — יענטה רפפורט (אלמנה) × מנדל הורוויץ מסוקאל, 12 בדצמבר 1920",
            'pl': "Akt małżeństwa Tarnów 1920, poz. 98 — Jente Rapaport (wdowa) × Mendel Horowitz z Sokala, 12.12.1920",
            'fr': "Acte de mariage Tarnów 1920, n° 98"
        },
        'source_archive': 'Archiwum Narodowe w Krakowie, Oddział w Tarnowie — Tarnów Jewish marriage register, page including entries 97-99',
        'decoded_fields': {
            'entry_number': 98,
            'date': '12 December 1920, Tarnów',
            'bride': "Jente Rapaport, wdowa (widow), age 33, daughter of 'Moses Rapaport and Menucha'",
            'groom': 'Mendel Eachem Horowitz, kawaler (bachelor), age 28, son of Pinches Horowitz, resident of Sokal',
            'witness_rabbi': 'Josef Chaim Kirschenbaum, rabbi in Tarnów'
        },
        'summary': {
            'en': "Second marriage of Berisz's sister Jente Rapaport. CRITICAL: explicitly names her parents as 'Moses Rapaport and Menucha' — direct primary-source corroboration of our apical couple."
        },
        'related_people': ['p_jente_rapaport', 'p_mendel_horowitz', 'p_moses_saul_rapaport', 'p_menukha'],
        'status': 'verified'
    },
    {
        'id': 'doc_rebeka_younger_marriage_1923',
        'file_pages': ['1923 Zylberfenig Rapaport T.jpg'],
        'kind': 'image',
        'type': 'marriage_record',
        'primary_language': 'pl',
        'title': {
            'en': "Marriage register Tarnów 1923, entry 101 — Rebeka Rapaport (b. Radomyśl Wielki) × Sane Zylberfenig of Płońsk, 4 September 1923",
            'he': "תעודת נישואין טרנוב 1923, רשומה 101 — רבקה רפפורט × סנה זילברפניג מפלוצק, 4 בספטמבר 1923",
            'pl': "Akt małżeństwa Tarnów 1923, poz. 101 — Rebeka Rapaport × Sane Zylberfenig z Płońska, 4.09.1923",
            'fr': "Acte de mariage Tarnów 1923, n° 101"
        },
        'source_archive': 'Archiwum Narodowe w Krakowie, Oddział w Tarnowie — Tarnów Jewish marriage register, page including entries 100-102',
        'decoded_fields': {
            'entry_number': 101,
            'date': '4 September 1923, Tarnów',
            'bride': "Rebeka Rapaport, wolna (single), age 27, born Radomyśl Wielki, daughter of 'Moses Rapaport and Menucha'",
            'groom': 'Sane Zylberfenig, kawaler (bachelor), age 34 years 10 months, born Płońsk, son of Abram + Pesi Zylberfenig',
            'witnesses': ['Maier Krak', 'David Erbg', 'Israel Marche']
        },
        'summary': {
            'en': "First marriage of Berisz's youngest sister Rebeka (b.1896, NOT to be confused with Berisz's wife Rebeka née Griffel). Explicitly confirms her birth at Radomyśl Wielki AND names her parents as 'Moses Rapaport and Menucha'. Third independent primary-source confirmation of our apical couple."
        },
        'related_people': ['p_rebeka_rapaport_sister', 'p_sane_zylberfenig', 'p_moses_saul_rapaport', 'p_menukha'],
        'status': 'verified'
    }
]
docs['documents'].extend(NEW_DOCS)
with open('platform/data/documents.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
print(f'documents now: {len(docs["documents"])}')
