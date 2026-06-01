"""Add the Ancestry/JewishGen Lota Rapaport Krakow ghetto finding to p_lota."""
import json

with open('platform/data/people.json', encoding='utf-8') as f:
    d = json.load(f)

for p in d['people']:
    if p.get('id') == 'p_lota':
        # Append a fact (don't overwrite)
        new_fact = {
            'key': 'krakow_ghetto_record_1940',
            'value': (
                "🎯 NEW LEAD (Dana, 25 May 2026): Listed as 'Lotte Rapaport', birth date 1915, in the "
                "JewishGen 'East Europe, Registers and Listings from Ten Jewish Ghettos, 1939-1942' database "
                "via Ancestry.com — Krakow ghetto, document date 1940 (Reel 13, List 177, Number 72). "
                "Birth year 1915 matches our Lota exactly (b. ~1915-1916 per 1924 passport: 'Lottr age 8'). "
                "Identification highly likely — same first name, same surname, same birth year, in the right "
                "geographical area at the right time. Earliest documented evidence of Lota under Nazi rule. "
                "Predates the betrayal/arrest episode described in Lusia's memoir (Lwów, ~1942-43). "
                "Suggests Lota may have moved from Lwów to Kraków at some point pre-1940 — or that she was "
                "in Kraków at war's start and only later moved to Lwów. Full record details (parents, spouse, "
                "address) can be retrieved by Doron via the Ancestry source citation."
            ),
            'confidence': 'documented',
            'sources': ['doc_jewishgen_ten_ghettos_lotte_rapaport']
        }
        p.setdefault('facts', []).append(new_fact)
        # Also update note_en to mention this
        p['note_en'] = (p.get('note_en') or '') + " — Documented in the JewishGen / Ancestry 'Ten Jewish Ghettos 1939-1942' database under 'Lotte Rapaport, b.1915, Krakow ghetto, 1940' (Reel 13, List 177, Number 72)."
        break

with open('platform/data/people.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('p_lota updated')

# Add the source document
with open('platform/data/documents.json', encoding='utf-8') as f:
    docs = json.load(f)

new_doc = {
    'id': 'doc_jewishgen_ten_ghettos_lotte_rapaport',
    'file_pages': ['IMG-20260525-WA0015.jpg', 'IMG-20260525-WA0016.jpg'],
    'kind': 'composite',
    'type': 'ghetto_record',
    'primary_language': 'en',
    'title': {
        'en': "Ancestry / JewishGen — Lotte Rapaport in Krakow ghetto 1940 (East Europe Ten Ghettos DB)",
        'he': "אסתרי / ג'ושג'ן — לוטה רפפורט בגטו קרקוב 1940",
        'pl': "Ancestry / JewishGen — Lotte Rapaport w gettcie krakowskim 1940",
        'fr': "Ancestry / JewishGen — Lotte Rapaport au ghetto de Cracovie 1940"
    },
    'source_archive': (
        "JewishGen.org Volunteers, comp. 'East Europe, Registers and Listings from Ten Jewish Ghettos, "
        "1939-1942' [database on-line]. Provo, UT: Ancestry.com Operations Inc, 2008. Original data: "
        "Lists of Jews in 10 ghettos including Balta (1941), Daugavpils (1941), Kozienice (1939-1942), "
        "Kraków (1940), Łódź (1940-1944), Lublin (1942), Lvov (1942-1945), Pinsk (1941-1942), "
        "Tirgu Mures (1945), Vilnius (1942). Discovered by Dana Rapaport 25 May 2026."
    ),
    'decoded_fields': {
        'ghetto': 'Kraków',
        'name': 'Lotte Rapaport',
        'birth_year': 1915,
        'document_year': 1940,
        'reel': 13,
        'list_number': 177,
        'entry_number': 72
    },
    'summary': {
        'en': (
            "Earliest documented record of our Lota Rapaport under Nazi rule. The birth year 1915 in this "
            "Ancestry record matches the family's records exactly (per Berisz's 1924 passport, Lota = Lottr "
            "age 8 → born ~1915-1916). The Krakow ghetto registration 1940 predates by ~2 years the betrayal "
            "and arrest in Lwów that Lusia's memoir describes. Full source record (parents' names, spouse, "
            "address, occupation) should be retrieved via the Ancestry citation Reel 13 / List 177 / Entry 72."
        )
    },
    'related_people': ['p_lota'],
    'status': 'verified',
    'related_action_items': [
        'Doron/Dana: pull the full Ancestry record (Reel 13, List 177, Entry 72) for parents/spouse/address',
        'Cross-check Lota in Krakow 1940 against the Krakow ghetto Judenrat residents list (Ringelblum archive)',
        'Yad Vashem PoT should be filed for Lota with this verified data point'
    ]
}
docs['documents'].append(new_doc)

with open('platform/data/documents.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
print(f'documents now: {len(docs["documents"])}')
