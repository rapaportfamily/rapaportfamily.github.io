"""Update documents.json to reflect the corrected Radomyśl-Wielki picture.

- Delete the doc_berisz_birth_tarnow_1884 entry (different family)
- Replace doc_berisz_passport_1924 with the proper 1924 Stanisławów Vienna application
- Replace the old "Moshe Rapaport descendants table" with the new "Moses Saul Rapaport" tree
- Add: doc_bernard_dov_yv_pot, doc_regina_rivka_yv_pot, doc_auschwitz_victim_188161,
       doc_griffel_dawid_descendants_tree, doc_lea_dawid_marriage_1935,
       doc_feige_englander_marriage_1932, doc_lea_rapaport_divorce_1941,
       doc_facets_family_history, doc_gelles_horowitz_chajes, doc_gelles_shapiro_friedman,
       doc_zvi_ayalon_nussbaum_photo
"""
import json

with open('platform/data/documents.json', encoding='utf-8') as f:
    d = json.load(f)

DELETE_IDS = {'doc_berisz_birth_tarnow_1884'}
d['documents'] = [doc for doc in d['documents'] if doc.get('id') not in DELETE_IDS]

# Update doc_berisz_passport_1924 — split it into the new (correct) document
for doc in d['documents']:
    if doc.get('id') == 'doc_berisz_passport_1924':
        doc['id'] = 'doc_berisz_swiadectwo_kwalifikacyjne_1924'
        doc['title']['en'] = ("'Świadectwo kwalifikacyjne' (Qualification Certificate) attached to a 1924 passport "
                              "file — ⚠ likely a DIFFERENT Benzion Rapaport, not our Berisz")
        doc['summary']['en'] = ("Basia (23 May 2026) transcribed this 'Świadectwo kwalifikacyjne' (qualification "
                                "certificate) as identifying Berisz Rapaport, son of Mojżesz Saul Rapaport, born "
                                "Tarnów 6 Aug 1884 as 'Benzion'. On 25 May 2026 Basia found the actual passport "
                                "application of our Berisz Rapaport (Stanisławów, August 1924, USHMM RG-31.064M) "
                                "which states he was born 30 July 1886 in Radomyśl Wielki — different city and "
                                "year. The original 1924 'Świadectwo' transcribed here therefore belongs to a "
                                "different Benzion Rapaport. Photo and details retained here for audit; "
                                "should NOT be linked to our Berisz.")
        doc['status'] = 'flagged_different_family'
        doc['related_people'] = []
        break

# Update old descendants tree to reference the v1 (kept as historical) — point at it
for doc in d['documents']:
    if doc.get('id') == 'doc_moshe_rapaport_descendants_table':
        doc['title']['en'] = "Descendants table of Moshe Rapaport (early version, superseded by 'Moses Saul Rapaport' tree)"
        doc['summary']['en'] = ("Original family-built genealogy chart shared by Basia on 23 May 2026. "
                                "Superseded by the more detailed 'Tablica potomków Moses Saul Rapaport' shared 31 May 2026.")
        doc['status'] = 'superseded'

NEW_DOCS = [
    {
        'id': 'doc_bernard_dov_yv_pot',
        'file_pages': ['Bernard Dov Rapaport.pdf'],
        'kind': 'pdf',
        'type': 'page_of_testimony',
        'primary_language': 'he',
        'title': {
            'en': "Yad Vashem Page of Testimony — Bernard Dov Rapaport (filed 1953)",
            'he': "דף עד יד ושם — ברנרד דב רפפורט (1953)",
            'pl': "Karta świadectwa Yad Vashem — Bernard Dov Rapaport (1953)",
            'fr': "Page de témoignage Yad Vashem — Bernard Dov Rapaport (1953)"
        },
        'source_archive': "Yad Vashem Central Database of Shoah Victims' Names, record file 90394",
        'decoded_fields': {
            'name': 'Bernard Dov Rapaport',
            'year_of_birth': 1888,
            'place_of_birth': 'Radomyśl, Poland',
            'father': 'Moshe',
            'mother': 'Menukha',
            'occupation': 'merchant',
            'pre_war_residence': 'Tarnów, Poland',
            'during_war': 'Przemyśl, Poland',
            'place_and_year_of_death': 'Auschwitz, 1940',
            'submitter': 'family member, 1953'
        },
        'summary': {
            'en': ("Primary documentary confirmation of Berisz's parents (Moshe + Menukha) and Holocaust fate "
                   "(Auschwitz). PoT year of birth (1888) differs from passport application (1886) — the passport "
                   "is a contemporary primary document and is the more reliable source for date.")
        },
        'related_people': ['p_berisz', 'p_moses_saul_rapaport', 'p_menukha'],
        'status': 'verified'
    },
    {
        'id': 'doc_regina_rivka_yv_pot',
        'file_pages': ['Regina Rivka Rapaport.pdf'],
        'kind': 'pdf',
        'type': 'page_of_testimony',
        'primary_language': 'he',
        'title': {
            'en': "Yad Vashem Page of Testimony — Regina Rivka Rapaport (filed 1953)",
            'he': "דף עד יד ושם — רגינה רבקה רפפורט (1953)",
            'pl': "Karta świadectwa Yad Vashem — Regina Rivka Rapaport (1953)",
            'fr': "Page de témoignage Yad Vashem — Regina Rivka Rapaport (1953)"
        },
        'source_archive': "Yad Vashem Central Database of Shoah Victims' Names, record file 90395",
        'decoded_fields': {
            'name': 'Regina Rivka Rapaport',
            'year_of_birth': 1892,
            'place_of_birth': 'Nadworna, Poland',
            'father': 'Leizer',
            'mother': 'Sara',
            'occupation': 'household',
            'pre_war_residence': 'Przemyśl, Poland',
            'during_war': 'Przemyśl, Poland',
            'place_and_year_of_death': 'unknown, 1943',
            'submitter': 'family member, 1953'
        },
        'summary': {
            'en': ("Primary documentary confirmation that Rebecca (Regina Rivka née Griffel) lived in Przemyśl "
                   "before and during the war, and perished in the Shoah. Year of birth (1892) differs from the "
                   "Griffel pedigree (1888) — likely an error by the 1953 submitter.")
        },
        'related_people': ['p_rebeka', 'p_leizor_griffel', 'p_sara_chajes'],
        'status': 'verified'
    },
    {
        'id': 'doc_berisz_passport_application_1924',
        'file_pages': [
            'RG-31.064M.0075.00000375-S.JPG',
            'RG-31.064M.0075.00000378-S.JPG',
            'RG-31.064M.0075.00000379-S.JPG',
            'RG-31.064M.0075.00000380-S.JPG'
        ],
        'kind': 'composite',
        'type': 'passport_application',
        'primary_language': 'pl',
        'title': {
            'en': "Berisch Rapaport — passport application + ID renewal (Stanisławów 1924-1927)",
            'he': "בריש רפפורט — בקשת דרכון וחידוש תעודת זהות (סטניסלאבוב 1924-1927)",
            'pl': "Berisch Rapaport — podanie o paszport i odnowienie dowodu (Stanisławów 1924-1927)",
            'fr': "Berisch Rapaport — demande de passeport et renouvellement de carte d'identité"
        },
        'source_archive': "USHMM, microfilm collection RG-31.064M, file 0075 (frames 375, 378, 379, 380). Located 25 May 2026 by Basia.",
        'decoded_fields': {
            'document_1': "Application for permission to travel abroad, Stanisławów 26 August 1924: 'I, the undersigned Berisch Rapaport, an industrialist residing in Stanisławów since 1918, declare that I am a citizen of the Republic of Poland of the Jewish faith, born in Radomyśl Wielki on July 30, 1886, in proof of which I have my ID card: Stanisławów, November 16, 1922 L/9376/22, and request the issuance of a foreign passport for travel to Vienna. Reason for travel: business.'",
            'document_2': "Identity-card application, Stanisławów 27 January 1927: 'Bernard Rapaport, born July 30, 1886 in Radomyśl, son of Moses and [illegible mother]. Average height, average build, square face, black eyes, proportionate mouth, healthy teeth.'",
            'document_3': "Reference docs: '1) Birth certificate dated 25 Feb 1916, Nos. 97. Volume V [illegible] 231 Sp 104. 2) Certificate of membership from Nadwórna 29 Jan 1927, no. 505/27.'",
            'document_4': "Receipt for passport fee payment.",
            'address': 'Berisch Rapaport, Kościuszki 4, Stanisławów',
            'occupation': 'industrialist (przemyślowiec)',
            'birthplace': 'Radomyśl Wielki',
            'birth_date': '30 July 1886',
            'father_name': 'Moses',
            'mother_name': 'illegible on document'
        },
        'summary': {
            'en': ("DEFINITIVE PRIMARY DOCUMENT establishing Berisz / Bernard Rapaport's identity: born 30 July "
                   "1886 in Radomyśl Wielki, son of Moses, industrialist, resident of Stanisławów since 1918, "
                   "address Kościuszki 4. Located by Basia at USHMM 25 May 2026; this is the source that "
                   "corrected the earlier confusion with the Tarnów-1884 'Benzion' birth certificate "
                   "(different family).")
        },
        'related_people': ['p_berisz', 'p_moses_saul_rapaport'],
        'related_events': [],
        'status': 'verified'
    },
    {
        'id': 'doc_auschwitz_victim_188161',
        'file_pages': [],
        'kind': 'external_source',
        'type': 'auschwitz_victim_record',
        'primary_language': 'pl',
        'title': {
            'en': "Auschwitz Museum victim record — Bernard Rapaport #188161",
            'he': "רישום קורבן מוזיאון אושוויץ — ברנרד רפפורט #188161",
            'pl': "Rekord ofiary Muzeum Auschwitz — Bernard Rapaport #188161",
            'fr': "Fiche de victime du Musée d'Auschwitz — Bernard Rapaport n° 188161"
        },
        'source_archive': "Auschwitz-Birkenau State Museum, Database of victims",
        'external_urls': [
            "https://victims.auschwitz.org/victims/188161",
            "https://victims.auschwitz.org/transports/689"
        ],
        'summary': {
            'en': ("Berisz / Bernard Rapaport listed as victim #188161 on transport #689 to Auschwitz. Located by "
                   "Basia 25 May 2026. The specific date of arrival and death will be available from the museum "
                   "record once accessed in detail.")
        },
        'related_people': ['p_berisz'],
        'status': 'verified'
    },
    {
        'id': 'doc_moses_saul_descendants_tree',
        'file_pages': [
            '6_Tablica potomkow Moses Saul Rapaport.pdf',
            'Tablica potomkow Moses Saul Rapaport 2.pdf'
        ],
        'kind': 'pdf',
        'type': 'family_tree_chart',
        'primary_language': 'pl',
        'title': {
            'en': "Descendants table of Moses Saul Rapaport (Basia, 31 May 2026)",
            'he': "לוח צאצאי משה שאול רפפורט (בסיה, 31 במאי 2026)",
            'pl': "Tablica potomków Moses Saul Rapaport (Basia, 31.05.2026)",
            'fr': "Tableau des descendants de Moses Saul Rapaport (Basia, 31 mai 2026)"
        },
        'source_archive': "Family-built genealogy chart compiled by Basia 31 May 2026 from primary documents and family research. Apical couple: Moses Saul Rapaport (merchant) + Menukha. Five children all born in Radomyśl Wielki: Alte Leja (1882, m. Turkel, Vienna branch), Berish (1886, our line), Jente (1887), Freida Amalia (1888, d. Przemyśl 1942, descendants Nussbaum + Rosenfeld), Rebeka (1896, Austria).",
        'summary': {
            'en': ("AUTHORITATIVE FAMILY TREE for the paternal Rapaport line: documents Moses Saul Rapaport as "
                   "patriarch, his 5 children (all born Radomyśl Wielki), and their descendants including David "
                   "Memek's first cousin Zwi Ayalon Nussbaum (b.1919 Przemyśl, survived to Israel d.2001 Haifa). "
                   "The Turkel branch (Alte Leja's descendants) lived in Vienna; some perished in the Holocaust "
                   "(Israel Menachem d.1942 Lwów; Siegfried d.1945 Belgium); others survived (Mordechai/Max "
                   "d.1997, Rachel/Rosie d.1999).")
        },
        'related_people': [
            'p_moses_saul_rapaport', 'p_menukha', 'p_berisz',
            'p_alte_leja_rapaport', 'p_jente_rapaport',
            'p_freida_amalia_rapaport', 'p_rebeka_rapaport_sister',
            'p_zwi_ayalon_nussbaum'
        ],
        'status': 'verified'
    },
    {
        'id': 'doc_griffel_dawid_descendants_tree',
        'file_pages': ['Tablica potomkow Dawid Griffel.pdf'],
        'kind': 'pdf',
        'type': 'family_tree_chart',
        'primary_language': 'pl',
        'title': {
            'en': "Descendants table of Dawid Griffel (Basia, 24 May 2026)",
            'he': "לוח צאצאי דוד גריפל (24 במאי 2026)",
            'pl': "Tablica potomków Dawid Griffel (Basia, 24.05.2026)",
            'fr': "Tableau des descendants de Dawid Griffel"
        },
        'source_archive': "Family-built genealogy chart compiled by Basia 24 May 2026, integrating Edward Gelles's published Griffel-of-Nadworna pedigree with newly-found Polish archival data.",
        'summary': {
            'en': ("Complete maternal-line tree: Dawid Griffel + Tauba → their son Lajzor Griffel (*1850, d.1918) "
                   "m. 1892 Nadwórna → Sara Matel Chajes (*1851.03.05, d.1940), with 10+ children including "
                   "Rivka (b.1888) who married Berish Rapaport at Olchowce, woj. lwowskie, in 1908. Connects to "
                   "well-known Griffel descendants: Yehuda Nir (1930-2014 Manhattan), Sarah Maslin Nir (NYT "
                   "journalist), Edward Gelles (genealogist).")
        },
        'related_people': ['p_rebeka', 'p_leizor_griffel', 'p_sara_chajes'],
        'status': 'verified'
    },
    {
        'id': 'doc_lea_dawid_marriage_1935',
        'file_pages': ['M_1935_Lea_Weitzner_Dawid_Mendel_Rapoport_B.jpg'],
        'kind': 'image',
        'type': 'marriage_record',
        'primary_language': 'pl',
        'title': {
            'en': "Marriage record — Lea Weitzner × Dawid Mendel Rapoport, 1935 (Bolechów)",
            'he': "תעודת נישואין — לאה וייצנר × דוד מנדל רפפורט, 1935 (בולוכוב)",
            'pl': "Akt małżeństwa — Lea Weitzner × Dawid Mendel Rapoport, 1935",
            'fr': "Acte de mariage — Lea Weitzner × Dawid Mendel Rapoport, 1935"
        },
        'source_archive': 'Polish vital records, located by Basia May 2026',
        'summary': {
            'en': "Primary documentary record of David Memek's marriage to Leah Lusia Weitzner in 1935. Confirms Lusia's memoir account of their marriage."
        },
        'related_people': ['p_david', 'p_leah'],
        'status': 'needs_translation'
    },
    {
        'id': 'doc_feige_englander_marriage_1932',
        'file_pages': ['M_ 1932_Feige_Weitzner_Israel_Englander_B.jpg'],
        'kind': 'image',
        'type': 'marriage_record',
        'primary_language': 'pl',
        'title': {
            'en': "Marriage record — Feige Weitzner × Israel Englander, 1932 (Bolechów)",
            'he': "תעודת נישואין — פייגה וייצנר × ישראל אנגלנדר, 1932",
            'pl': "Akt małżeństwa — Feige Weitzner × Israel Englander, 1932",
            'fr': "Acte de mariage — Feige Weitzner × Israel Englander, 1932"
        },
        'source_archive': 'Polish vital records, located by Basia May 2026',
        'summary': {
            'en': "Primary documentary record of Lusia's elder sister Feige (Tzipora) Weitzner marrying Israel Englander in 1932 in Bolechów."
        },
        'related_people': ['p_feige'],
        'status': 'needs_translation'
    },
    {
        'id': 'doc_lea_rapaport_divorce_1941',
        'file_pages': ['1941 rozwod Lea Rapaport.jpg'],
        'kind': 'image',
        'type': 'court_record',
        'primary_language': 'pl',
        'title': {
            'en': "1941 divorce record — Lea Rapaport (?)",
            'he': "תעודת גירושין 1941 — לאה רפפורט (?)",
            'pl': "1941 rozwód — Lea Rapaport (?)",
            'fr': "Divorce 1941 — Lea Rapaport (?)"
        },
        'source_archive': 'Polish records, shared by Basia May 2026',
        'summary': {
            'en': ("A 1941 divorce document for a 'Lea Rapaport'. Identity of the Lea has NOT been verified — "
                   "may or may not refer to Leah Lusia Weitzner-Rapaport (our family). Awaiting Basia's review.")
        },
        'related_people': [],
        'status': 'unverified'
    },
    {
        'id': 'doc_facets_family_history',
        'file_pages': ['Facets of my Family History. Part 2.pdf'],
        'kind': 'pdf',
        'type': 'genealogical_paper',
        'primary_language': 'en',
        'title': {
            'en': "Facets of my Family History, Part 2 (Edward Gelles)",
            'he': "פנים בתולדות משפחתי, חלק 2 (אדוארד גלס)",
            'pl': "Facets of my Family History, Part 2 (Edward Gelles)",
            'fr': "Facets of my Family History, Part 2 (Edward Gelles)"
        },
        'source_archive': "Edward Gelles, published genealogical paper (Balliol College Oxford archives)",
        'summary': {
            'en': "Edward Gelles's published genealogical research on the extended Griffel-Chajes family, which includes the Rapaport branch via Berisz × Rebeka Griffel."
        },
        'related_people': ['p_rebeka', 'p_leizor_griffel'],
        'status': 'verified'
    },
    {
        'id': 'doc_gelles_horowitz_chajes',
        'file_pages': ['GellesHorowitzChajes.pdf'],
        'kind': 'pdf',
        'type': 'genealogical_paper',
        'primary_language': 'en',
        'title': {
            'en': "Gelles — Horowitz–Chajes connections",
            'he': "גלס — קשרי משפחות הורוביץ–חיות",
            'pl': "Gelles — Horowitz-Chajes",
            'fr': "Gelles — Horowitz-Chajes"
        },
        'source_archive': "Edward Gelles, published genealogical paper",
        'summary': {
            'en': "Edward Gelles's research on the Horowitz and Chajes rabbinical families. Sara Matel Chajes (Rebeka's mother) was from this line."
        },
        'related_people': ['p_sara_chajes'],
        'status': 'verified'
    },
    {
        'id': 'doc_gelles_shapiro_friedman',
        'file_pages': ['GellesShapiroFriedman.pdf'],
        'kind': 'pdf',
        'type': 'genealogical_paper',
        'primary_language': 'en',
        'title': {
            'en': "Gelles — Shapiro–Friedman connections",
            'he': "גלס — קשרי משפחות שפירא–פרידמן",
            'pl': "Gelles — Shapiro-Friedman",
            'fr': "Gelles — Shapiro-Friedman"
        },
        'source_archive': "Edward Gelles, published genealogical paper",
        'summary': {
            'en': "Edward Gelles's research on the Shapiro and Friedman rabbinical families and their connections to the Griffel-Chajes-Rapaport network."
        },
        'related_people': [],
        'status': 'verified'
    },
    {
        'id': 'doc_zvi_ayalon_nussbaum_photo',
        'file_pages': ['Zvi Hirsch Heschu Ayalon (Nussbaum).jfif'],
        'kind': 'image',
        'type': 'photograph',
        'primary_language': 'he',
        'title': {
            'en': "Photo — Zwi (Hirsch Heschel) Ayalon Nussbaum, David Memek's first cousin",
            'he': "תמונה — צבי איילון (נוסבאום), בן דודו של דוד ממק",
            'pl': "Zdjęcie — Zwi Ayalon Nussbaum, kuzyn Dawida",
            'fr': "Photo — Zwi Ayalon Nussbaum"
        },
        'source_archive': "Israeli family archive",
        'summary': {
            'en': "Photograph of Zwi Ayalon (born Nussbaum) — David Memek's paternal first cousin, b.1919 Przemyśl, d.2001 Haifa. Son of Berisz's sister Freida Amalia Rapaport."
        },
        'related_people': ['p_zwi_ayalon_nussbaum', 'p_freida_amalia_rapaport'],
        'status': 'verified'
    }
]

# Insert new docs before additional_files section
d['documents'].extend(NEW_DOCS)

with open('platform/data/documents.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f'documents now: {len(d["documents"])}')
