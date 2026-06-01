"""Update people.json with verified Radomyśl Wielki facts (run once).

- Rename p_mojzesz_saul_rapaport -> p_moses_saul_rapaport, strip Tarnów-Benzion attribution
- Delete p_rywka_schiff, p_michal_schiff, p_cywie_schiff (belong to a different Tarnów Rapaport family)
- Update p_rebeka with documented 1911 marriage and PoT info
- Add p_menukha, p_alte_leja_rapaport, p_jente_rapaport, p_freida_amalia_rapaport,
  p_rebeka_rapaport_sister, p_zwi_ayalon_nussbaum
"""
import json

with open('platform/data/people.json', encoding='utf-8') as f:
    d = json.load(f)

idx_by_id = {p['id']: i for i, p in enumerate(d['people'])}

# Rename + clean Moses Saul Rapaport
if 'p_mojzesz_saul_rapaport' in idx_by_id:
    p = d['people'][idx_by_id['p_mojzesz_saul_rapaport']]
    p['id'] = 'p_moses_saul_rapaport'
    p['primary_name'] = {
        'en': 'Moses (Moshe) Saul Rapaport',
        'he': 'משה שאול רפפורט',
        'pl': 'Moses Saul Rapaport',
        'fr': 'Moïse Saul Rapaport',
    }
    p['aliases'] = ['Moshe Saul', 'Moses Saul']
    p['role'] = 'great_great_grandfather_paternal'
    p['note_en'] = (
        'Paternal great-great-grandfather of Doron, Dana and Daniel. Father of Berisz / Bernard Dov Rapaport '
        'per his 1924 passport application (USHMM RG-31.064M) and Yad Vashem Page of Testimony. Listed as kupiec '
        '(merchant) on the family-built descendants tree shared by Basia May 2026. Berisz was born in Radomyśl '
        'Wielki — Moses Saul was presumably resident there. Two stones in the preserved Tarnów Jewish cemetery '
        'bear the name Moshe Saul Rapaport (one d. 11/08/1933, the other d. 30/10/1931 from Dąbrowa, '
        '7th-generation descendant of Shabtai HaKohen / "the Shah") — it is not yet established which (if either) '
        'is our Moses Saul. Spouse: Menukha (per Yad Vashem Page of Testimony of his son Berisz).'
    )
    p['spouse_id'] = 'p_menukha'
    p['children_ids'] = [
        'p_alte_leja_rapaport', 'p_berisz', 'p_jente_rapaport',
        'p_freida_amalia_rapaport', 'p_rebeka_rapaport_sister'
    ]
    if 'birth' in p:
        del p['birth']
    if 'mother_id' in p:
        del p['mother_id']
    if 'father_id' in p:
        del p['father_id']
    p['facts'] = [
        {
            'key': 'occupation',
            'value': 'Merchant (kupiec) per the family-built descendants tree shared by Basia May 2026.',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        {
            'key': 'kohanic_lineage',
            'value': 'Kohen (priestly descent) per family tradition; consistent with the "ha-Cohen" patronymic on related Rapaport tombstones in Tarnów.',
            'confidence': 'family_oral',
            'sources': ['src_family_tradition_kohen']
        }
    ]

# Delete Schiff entries (those belonged to a different Tarnów Rapaport family)
DELETE_IDS = {'p_rywka_schiff', 'p_michal_schiff', 'p_cywie_schiff'}
d['people'] = [p for p in d['people'] if p.get('id') not in DELETE_IDS]

# Clean dangling refs: rename + drop
def clean_value(v):
    if v == 'p_mojzesz_saul_rapaport':
        return 'p_moses_saul_rapaport'
    return v

def clean_node(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if isinstance(v, str) and v in DELETE_IDS:
                continue
            out[k] = clean_node(v)
        return out
    if isinstance(node, list):
        return [clean_node(x) for x in node if not (isinstance(x, str) and x in DELETE_IDS)]
    return clean_value(node)

d = clean_node(d)

# Update Rebeka
for p in d['people']:
    if p.get('id') == 'p_rebeka':
        p['note_en'] = (
            'Paternal great-grandmother of Doron, Dana and Daniel. Mother of David Mendel and Lota. Born 1888 in '
            'Nadwórna, daughter of Eliezer "Zeida" Griffel and Sara Matel Chajes. Yad Vashem Page of Testimony '
            'filed 1953 by family lists year of birth as 1892 — likely a memory error by the submitter; the '
            'Griffel-family pedigree confirms 1888. Civilly married Berisz Rapaport in Nadwórna on 21 December '
            '1911, four days before son David Mendel was born. The 1890-1914 Nadwórna marriage register was lost '
            'in WWI; only a notation on David\'s birth certificate confirms the marriage. Edward Gelles\'s '
            '"Griffel of Nadworna" pedigree records a religious marriage at Olchowce, województwo lwowskie in '
            '1908 — likely an earlier ritual wedding before civil registration. Pre-war residence: Przemyśl. '
            'War: Przemyśl. Per Lusia\'s memoir page 24 (Basia\'s Polish reading), killed by Germans in Przemyśl, '
            'accused of allegedly placing a bomb on the railway near where the family lived — fabricated charge, '
            'likely 1942. Yad Vashem PoT lists 1943 as year of death, place unknown.'
        )
        p['birth'] = {
            'date': '1888',
            'date_precision': 'year',
            'place_id': 'pl_nadworna',
            'confidence': 'documented',
            'sources': ['src_gelles_griffel_nadworna_pdf', 'doc_regina_rivka_yv_pot']
        }
        p['death'] = {
            'date': '1942',
            'date_precision': 'year',
            'place_id': 'pl_przemysl',
            'confidence': 'documented',
            'sources': ['src_lusia_memoir_page_24', 'doc_regina_rivka_yv_pot'],
            'note_en': (
                'Killed in Przemyśl by Germans on a fabricated bomb-on-railway accusation, per Lusia\'s memoir '
                'page 24 — Basia\'s Polish reading interprets the ambiguous Hebrew חמה/חמותה as "mother-in-law". '
                'Yad Vashem PoT filed 1953 lists year 1943 place unknown — discrepancy attributed to 1953 '
                'submitter\'s incomplete knowledge.'
            )
        }
        break

NEW_PEOPLE = [
    {
        'id': 'p_menukha',
        'primary_name': {
            'en': 'Menukha Rapaport',
            'he': 'מנוחה רפפורט',
            'pl': 'Menukha Rapaport',
            'fr': 'Menukha Rapaport'
        },
        'role': 'great_great_grandmother_paternal',
        'note_en': (
            'Paternal great-great-grandmother of Doron, Dana and Daniel. Wife of Moses Saul Rapaport, mother '
            'of Berisz / Bernard Dov. Name documented on the Yad Vashem Page of Testimony filed 1953 for her '
            'son Berisz. Maiden name not yet known.'
        ),
        'spouse_id': 'p_moses_saul_rapaport',
        'children_ids': [
            'p_alte_leja_rapaport', 'p_berisz', 'p_jente_rapaport',
            'p_freida_amalia_rapaport', 'p_rebeka_rapaport_sister'
        ],
        'facts': []
    },
    {
        'id': 'p_alte_leja_rapaport',
        'primary_name': {
            'en': 'Alte Leja Rapaport (m. Turkel)',
            'he': 'אלטה לאה רפפורט (טורקל)',
            'pl': 'Alte Leja Rapaport (zam. Turkel)',
            'fr': 'Alte Leja Rapaport (ép. Turkel)'
        },
        'aliases': ['Alta Leah', 'Alta Leja'],
        'role': 'great_grand_aunt_paternal',
        'note_en': (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Eldest known sibling of Berisz Rapaport. '
            'Born 28 June 1882 in Radomyśl Wielki; murdered at Auschwitz 1942 per the family-built descendants '
            'tree. Married Turkel; family lived in Vienna with multiple children (Turkel branch: Hertha Noa, '
            'Lotte, Israel Menachem, Mordechai/Max, Rachel/Rosie, Siegfried, Chana).'
        ),
        'birth': {
            'date': '1882-06-28',
            'date_precision': 'day',
            'place_id': 'pl_radomysl_wielki',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'death': {
            'date': '1942',
            'date_precision': 'year',
            'place_id': 'pl_auschwitz',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'father_id': 'p_moses_saul_rapaport',
        'mother_id': 'p_menukha',
        'siblings_ids': ['p_berisz', 'p_jente_rapaport', 'p_freida_amalia_rapaport', 'p_rebeka_rapaport_sister'],
        'facts': []
    },
    {
        'id': 'p_jente_rapaport',
        'primary_name': {
            'en': 'Jente Rapaport',
            'he': 'יענטה רפפורט',
            'pl': 'Jente Rapaport',
            'fr': 'Jente Rapaport'
        },
        'role': 'great_grand_aunt_paternal',
        'note_en': (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Sibling of Berisz Rapaport. Born 1887 in '
            'Radomyśl Wielki per the family-built descendants tree. Further details not yet documented.'
        ),
        'birth': {
            'date': '1887',
            'date_precision': 'year',
            'place_id': 'pl_radomysl_wielki',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'father_id': 'p_moses_saul_rapaport',
        'mother_id': 'p_menukha',
        'siblings_ids': ['p_alte_leja_rapaport', 'p_berisz', 'p_freida_amalia_rapaport', 'p_rebeka_rapaport_sister'],
        'facts': []
    },
    {
        'id': 'p_freida_amalia_rapaport',
        'primary_name': {
            'en': 'Freida Amalia Rapaport',
            'he': 'פריידה אמליה רפפורט',
            'pl': 'Freida Amalia Rapaport',
            'fr': 'Freida Amalia Rapaport'
        },
        'aliases': ['Frieda', 'Amalia'],
        'role': 'great_grand_aunt_paternal',
        'note_en': (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Sibling of Berisz Rapaport. Born 1888 in '
            'Radomyśl Wielki; died 1942 in Przemyśl per the family-built descendants tree (so was with Berisz '
            'and Rebecca in Przemyśl during the war). Documented children: Zwi Ayalon Nussbaum (b.1919 Przemyśl, '
            'survived to Israel, d.2001 Haifa), Michael Rosenfeld (b.1929, killed Przemyśl 1944), Rachel '
            'Rosenfeld (b.1930, killed Przemyśl 1944).'
        ),
        'birth': {
            'date': '1888',
            'date_precision': 'year',
            'place_id': 'pl_radomysl_wielki',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'death': {
            'date': '1942',
            'date_precision': 'year',
            'place_id': 'pl_przemysl',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'father_id': 'p_moses_saul_rapaport',
        'mother_id': 'p_menukha',
        'siblings_ids': ['p_alte_leja_rapaport', 'p_berisz', 'p_jente_rapaport', 'p_rebeka_rapaport_sister'],
        'children_ids': ['p_zwi_ayalon_nussbaum'],
        'facts': []
    },
    {
        'id': 'p_rebeka_rapaport_sister',
        'primary_name': {
            'en': 'Rebeka Rapaport (Berisz\'s sister)',
            'he': 'רבקה רפפורט (אחותו של בריש)',
            'pl': 'Rebeka Rapaport (siostra Berisza)',
            'fr': 'Rebeka Rapaport (sœur de Berisz)'
        },
        'role': 'great_grand_aunt_paternal',
        'note_en': (
            'Paternal great-grand-aunt of Doron, Dana and Daniel. Youngest known sibling of Berisz Rapaport. '
            'Born 1896 in Radomyśl Wielki; subsequently lived in Austria per the family-built descendants tree. '
            'NOT to be confused with Berisz\'s wife Rebeka née Griffel.'
        ),
        'birth': {
            'date': '1896',
            'date_precision': 'year',
            'place_id': 'pl_radomysl_wielki',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'father_id': 'p_moses_saul_rapaport',
        'mother_id': 'p_menukha',
        'siblings_ids': ['p_alte_leja_rapaport', 'p_berisz', 'p_jente_rapaport', 'p_freida_amalia_rapaport'],
        'facts': []
    },
    {
        'id': 'p_zwi_ayalon_nussbaum',
        'primary_name': {
            'en': 'Zwi (Hersh Heschel) Ayalon Nussbaum',
            'he': 'צבי הירש העשל איילון (נוסבאום)',
            'pl': 'Zwi Hirsch Heschu Ayalon (Nussbaum)',
            'fr': 'Zwi Ayalon Nussbaum'
        },
        'aliases': ['Zvi Ayalon', 'Hirsch', 'Heschel'],
        'role': 'first_cousin_once_removed_paternal',
        'note_en': (
            'Paternal first cousin once removed of Doron, Dana and Daniel — first cousin of David Memek. Son '
            'of Freida Amalia Rapaport. Born 7 May 1919 in Przemyśl; survived the Holocaust and emigrated to '
            'Israel; died 27 November 2001 in Haifa. Photographed in the family archive '
            '("Zvi Hirsch Heschu Ayalon (Nussbaum).jfif"). His Israeli surname "Ayalon" is a Hebraization of '
            'the German-origin "Nussbaum".'
        ),
        'birth': {
            'date': '1919-05-07',
            'date_precision': 'day',
            'place_id': 'pl_przemysl',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'death': {
            'date': '2001-11-27',
            'date_precision': 'day',
            'place_id': 'pl_haifa',
            'confidence': 'documented',
            'sources': ['doc_moses_saul_descendants_tree']
        },
        'mother_id': 'p_freida_amalia_rapaport',
        'facts': []
    }
]

insert_after = None
for i, p in enumerate(d['people']):
    if p['id'] == 'p_berisz':
        insert_after = i + 1
        break
if insert_after is None:
    raise SystemExit('p_berisz not found')
d['people'][insert_after:insert_after] = NEW_PEOPLE

with open('platform/data/people.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f'total people now: {len(d["people"])}')
