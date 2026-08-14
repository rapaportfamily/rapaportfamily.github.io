# -*- coding: utf-8 -*-
"""Build the film manifest — one file that tells a film-maker (or an LLM) everything this
archive holds, generated from the live data rather than written by hand.

The previous manifest was dated 5 August and predated Basia's 1,072-file library, Jacob's
Griffel tree, Berish's face and the exact date of his death, the transport from the prison at
Tarnów, Lotte's Page of Testimony, Dov's four journeys and the tenth chapter. A stale manifest
is worse than none: it looks complete and quietly omits a week of work, which is exactly the
failure Doron asked to avoid.

run:  python scripts/build_film_manifest.py
"""
import io, os, re, sys, json, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'platform')
D = os.path.join(SITE, 'data')


def load(name, default=None):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        return default
    return json.load(io.open(p, encoding='utf-8'))


people = load('people.json', {'people': []})['people']
docs = load('documents.json', {'documents': []})['documents']
narr = load('narrative.json', {'chapters': []})
ext = load('extended_tree.json', {'counts': {}, 'people': {}})
grif = load('griffel_tree.json', {'counts': {}, 'people': {}})
trips = load('dov_trips.json', {'albums': [], 'photographs': []})
unid = load('unidentified_photographs.json', {'photographs': []})
memoir = load('memoir_photographs.json', {'photographs': []})
events = load('events.json', {'events': []})
hyps = load('hypotheses.json', {'hypotheses': []})
places = load('places.json', {'places': []})

by_id = {p['id']: p for p in people}


def nm(pid):
    p = by_id.get(pid) or {}
    return (p.get('primary_name') or {}).get('en') or pid


def person_block(pid):
    p = by_id.get(pid)
    if not p:
        return None
    return {
        'id': pid,
        'name': (p.get('primary_name') or {}),
        'born': (p.get('birth') or {}).get('date'),
        'born_place': (p.get('birth') or {}).get('place_id') or (p.get('birth') or {}).get('place_name'),
        'died': (p.get('death') or {}).get('date'),
        'died_place': (p.get('death') or {}).get('place_id') or (p.get('death') or {}).get('place_name'),
        'portrait': p.get('photo'),
        'portrait_caption': p.get('photo_caption'),
        'note_en': p.get('note_en'),
        'facts': [{'key': f.get('key'),
                   'value': (f.get('value') or {}).get('en') if isinstance(f.get('value'), dict)
                            else f.get('value'),
                   'sources': f.get('sources')} for f in (p.get('facts') or [])],
    }


# every image the site can show, grouped so a film-maker can find pictures by subject
def walk_assets(sub):
    base = os.path.join(SITE, 'assets', 'documents', sub)
    out = []
    for r, _, fs in os.walk(base):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), SITE).replace('\\', '/')
            out.append(rel)
    return sorted(out)


manifest = collections.OrderedDict()
manifest['_readme'] = (
    'EVERYTHING this archive holds, generated from the live data on the day shown in '
    '"generated". It exists so that a film can be made without missing anything. Every path '
    'below is relative to https://rapaportfamily.github.io/ — append it to that address to '
    'fetch the file. Nothing here is a summary: where a number appears, the underlying items '
    'are listed or reachable.')
manifest['generated'] = '2026-08-11'
manifest['site'] = 'https://rapaportfamily.github.io/'
manifest['subject'] = {
    'occasion': 'Dov Bernard Rapaport turns 80 on 28 August 2026.',
    'made_by': 'Dalia, Dana, Daniel and Doron Rapaport, with Basia, Jacob, Magda, Kasia and '
               'Ms. Kasia of the Jewish Historical Institute, Warsaw.',
    'the_four': ['p_david', 'p_leah', 'p_shimon', 'p_dov_bernard'],
}
manifest['hard_rules'] = [
    'Never invent. Every statement in the film must trace to a record in this manifest.',
    'Where sources disagree, SHOW the disagreement — this archive publishes conflicts rather '
    'than resolving them quietly. Examples are in "conflicts".',
    'The memoir is testimony, not proof. Compare it with the documents respectfully: where it '
    'is confirmed say so, where it is uncorroborated say so, and never call it wrong for '
    'lacking paper.',
    'Living people: no birth dates.',
    'A photograph is attributed to a named person ONLY where the archive says the file names '
    'them. Anything in "unidentified" must never be captioned with a name.',
    'Illustrations and AI-generated imagery are allowed but must be visibly marked as '
    'illustration, never mixed with the real photographs without a label.',
]
manifest['counts'] = {
    'curated_people': len(people),
    'people_with_a_portrait': sum(1 for p in people if p.get('photo')),
    'documents': len(docs),
    'document_types': dict(collections.Counter(d['type'] for d in docs)),
    'rapaport_tree': ext.get('counts', {}),
    'griffel_tree': grif.get('counts', {}),
    'memoir_photographs': len(memoir.get('photographs') or []),
    'dov_trip_photographs': len(trips.get('photographs') or []),
    'unidentified_photographs': len(unid.get('photographs') or []),
    'timeline_events': len(events.get('events') or []),
    'open_questions': len(hyps.get('hypotheses') or []),
    'places': len(places.get('places') or []),
}
manifest['data_files'] = {
    'people': 'platform/data/people.json',
    'documents': 'platform/data/documents.json',
    'narrative': 'platform/data/narrative.json',
    'timeline_events': 'platform/data/events.json',
    'places': 'platform/data/places.json',
    'open_questions': 'platform/data/hypotheses.json',
    'memoir_photographs': 'platform/data/memoir_photographs.json',
    'rapaport_wider_tree': 'platform/data/extended_tree.json',
    'griffel_wider_tree': 'platform/data/griffel_tree.json',
    'dov_journeys': 'platform/data/dov_trips.json',
    'unidentified_photographs': 'platform/data/unidentified_photographs.json',
    'auschwitz_rapaport_index': 'platform/data/auschwitz_rapaport_index.json',
}
manifest['principals'] = [person_block(p) for p in
                          ('p_david', 'p_leah', 'p_shimon', 'p_dov_bernard') if by_id.get(p)]
manifest['the_generation_before'] = [person_block(p) for p in
                                     ('p_berisz', 'p_rebeka', 'p_lota', 'p_lajzor_griffel',
                                      'p_sara_matel_chajes', 'p_moses_saul', 'p_abraham_abe_rapaport')
                                     if by_id.get(p)]
manifest['narrative'] = [{
    'n': i, 'id': c.get('id'), 'years': c.get('years'), 'title': c.get('title'),
    'paragraphs': [{'text': p['text'], 'sources': p.get('sources')} for p in c['paragraphs']],
} for i, c in enumerate(narr.get('chapters', []))]

manifest['documents'] = [{
    'id': d['id'], 'type': d['type'], 'title': d.get('title'),
    'summary_en': (d.get('summary') or {}).get('en'),
    'decoded_fields': d.get('decoded_fields'),
    'files': ['platform/assets/documents/' + f for f in (d.get('file_pages') or [])],
    'people': [nm(x) for x in (d.get('related_people') or [])],
    'external': d.get('external_urls'),
    'status': d.get('status'),
    'open_questions': d.get('open_questions'),
} for d in docs]

manifest['memoir_photographs'] = memoir.get('photographs') or []
manifest['dov_journeys'] = {'albums': trips.get('albums') or [],
                            'photographs': trips.get('photographs') or [],
                            'review_note': trips.get('reviewed')}
manifest['unidentified_photographs'] = {
    'note': 'Nobody knows who these are. NEVER caption them with a name.',
    'items': unid.get('photographs') or []}
manifest['timeline_events'] = events.get('events') or []
manifest['places'] = places.get('places') or []
manifest['open_questions'] = hyps.get('hypotheses') or []

manifest['image_folders'] = {
    'memoir_plates': 'platform/assets/research_images/memoir/',
    'basia_rapaport_library': {
        'photographs': 'platform/assets/documents/basia_2026_08/photos/',
        'civil_registers': 'platform/assets/documents/basia_2026_08/registers/',
        'yad_vashem_pages': 'platform/assets/documents/basia_2026_08/yad_vashem/',
        'papers_pdf_doc': 'platform/assets/documents/basia_2026_08/papers/',
        'file_count': len(walk_assets('basia_2026_08')),
    },
    'jacob_griffel_library': {
        'photographs': 'platform/assets/documents/griffel_2026_08/photos/',
        'civil_registers': 'platform/assets/documents/griffel_2026_08/registers/',
        'yad_vashem_pages': 'platform/assets/documents/griffel_2026_08/yad_vashem/',
        'census': 'platform/assets/documents/griffel_2026_08/census/',
        'papers_pdf_doc': 'platform/assets/documents/griffel_2026_08/papers/',
        'file_count': len(walk_assets('griffel_2026_08')),
    },
    'dov_journeys': {'path': 'platform/assets/documents/dov_trips_2026_08/',
                     'file_count': len(walk_assets('dov_trips_2026_08'))},
}

manifest['the_research_story'] = [
    'The archive began with one memoir — Lusia wrote her life down — and a handful of family '
    'papers. Everything else was found.',
    'Basia, a genealogist in Poland, rebuilt the Rapaport line back to Abraham Abe, born 1784 at '
    'Tarnów. On 5 August 2026 she sent the tree as a GEDCOM: 1,442 people, 480 families. On '
    '6 August she sent her whole media library — 1,072 files, 1.1 GB.',
    'Jacob sent the other side: the GRIFFEL line, David’s mother’s family, 390 people and 569 '
    'files. Not one of his files appears in Basia’s. Two researchers, two families, meeting at '
    'Rebeka Griffel.',
    'Ms. Kasia at the Jewish Historical Institute in Warsaw found David’s birth certificate in '
    'Nadwórna on 15 May 2026, which corrected a birthplace the 1946 Brussels DP card had wrong.',
    'The archive read its own holdings against the free internet: the Auschwitz-Birkenau '
    'Memorial’s victim database confirmed Berish’s prisoner number and death date at source, and '
    'its transport page revealed where he was taken FROM — the prison at Tarnów.',
    'The archive corrected itself in public more than once. It had claimed no Page of Testimony '
    'was ever filed for Berish or Rebeka while holding both of them in its own document list. '
    'It had filed a 1924 certificate as "a different family" when the form names Mendel aged 12 '
    'and Lotte aged 8. Both corrections are on the site, with the reasoning.',
    'Every file we were given has been walked against what the site serves, in both directions. '
    'Two things are missing and both are named on the site.',
]

manifest['conflicts'] = [
    'Berish’s death: the Auschwitz Museum and the camp Sterbebücher both say 29 March 1942; the '
    'Yad Vashem page David filed in 1953 says 1940. Both are published.',
    'Rebeka: this archive holds born 1888, died 1942; her Yad Vashem page says 1892 and 1943; '
    'Jacob’s tree says "1942?" with the question mark. All three are published.',
    'Lotte: born 27 September 1915 per the trees, 1914 per her Yad Vashem page. Her cousin '
    'Charlotte Horowitz was born 21 November 1914 in the same city — do not merge them.',
    'David’s birthplace: Nadwórna per the birth certificate; "Cieszyn/Tesin" on the 1946 DP card, '
    'most likely a clerk mishearing.',
    'A birth register filed 1849 where this archive holds 1850, published as a conflict.',
]

out = os.path.join(D, 'film_manifest.json')
json.dump(manifest, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
io.open(out, 'a', encoding='utf-8').write('\n')
size = os.path.getsize(out) / 1024.0
print('film_manifest.json rebuilt — %.0f KB' % size)
for k, v in manifest['counts'].items():
    print('   %-28s %s' % (k, v))
