"""Polish-language version of the Rapaport family summary."""
import sys
sys.path.insert(0, 'scripts')
from generate_summary_docx import build_doc, OUT_DIR

PL = {
    "title": "Badania nad rodziną Rapaport",
    "subtitle": "Stan wiedzy na dzień 1 czerwca 2026",
    "intro": (
        "Niniejszy dokument podsumowuje to, co wiemy o rodzinie Rapaport, na jakiej "
        "podstawie to wiemy oraz które wcześniejsze ustalenia musieliśmy wycofać. "
        "Jest to robocze opracowanie dla Dalii, Dany, Daniela i Doron Rapaportów — "
        "oraz dla Basi, Magdy, Kasi i Pani Kasi, dzięki którym powstały udokumentowane "
        "ustalenia poniżej. Przygotowane przez Claude Code po trzecim imporcie eksportu "
        "z WhatsAppa projektu drzewa genealogicznego. Każde twierdzenie poniżej ma "
        "podane źródło; wnioski oparte na hipotezach są wyraźnie oznaczone."
    ),

    "h1_paternal": "1. Linia ojcowska (od Mojżesza Saula do nas)",
    "paternal_intro": (
        "Możemy obecnie umiejscowić sześć potwierdzonych pokoleń linii ojcowskiej. Do "
        "maja 2026 r. znane było tylko imię Berisza, bez udokumentowanych rodziców; "
        "w ciągu ostatnich sześciu tygodni dodaliśmy parę protoplastów Mojżesza Saula "
        "i Menuchę (prapradziadków) oraz cztery siostry Berisza, wszystko potwierdzone "
        "dokumentami archiwalnymi."
    ),
    "paternal_rows": [
        ("Prapradziadkowie",
         "Mojżesz (Moshe) Saul Rapaport + Menucha",
         "Rodzina kupiecka w Radomyślu Wielkim. Moshe Rappaport zasiadał w Radzie "
         "Gminy Wyznaniowej Żydowskiej w Radomyślu Wielkim w latach 1897–1900 oraz "
         "1901–1905.",
         "Karta świadectwa Yad Vashem dla Berisza (1953); trzy księgi małżeństw "
         "tarnowskie ich córek (1919, 1920, 1923) — każda wymienia wprost „Moses "
         "Rapaport i Menucha\" jako rodziców panny młodej; Księga Pamięci Radomyśla "
         "Wielkiego, część I (lista członków Rady Gminy)."),
        ("Pradziadkowie",
         "Berisz / Bernard / Dov Rapaport (1886–1942) + Rebeka z domu Griffel (1888–1942)",
         "Berisz urodzony 30 lipca 1886 r. w Radomyślu Wielkim. Przemysłowiec w "
         "Stanisławowie od 1918 r. Ślub cywilny z Rebeką w Nadwórnej 21 grudnia "
         "1911 r. W 1939 r. rodzina mieszkała w Przemyślu. Berisz został "
         "deportowany do Auschwitz i tam zamordowany. Rebeka została zabita w "
         "Przemyślu na podstawie sfabrykowanego oskarżenia o podłożenie bomby na "
         "torach kolejowych, prawdopodobnie w 1942 r.",
         "USHMM RG-31.064M (podania paszportowe Berisza ze Stanisławowa 1924 + "
         "1927); karty świadectwa Yad Vashem 90394 + 90395 (1953); rekord ofiary "
         "Muzeum Auschwitz nr 188161, transport nr 689; rodowód „Griffel of "
         "Nadworna\" Edwarda Gellesa, pozycja nr 8; badania Basi nad nadwórniańską "
         "księgą małżeństw; wspomnienia Lusi, strona 24."),
        ("Dziadkowie",
         "Dawid Mendel (Memek) Rapaport (1911–1990) + Lea Lusia z domu Weitzner "
         "(1913 lub 1916 – 1996)",
         "Dawid ur. 25 grudnia 1911 r. w Nadwórnej. Inżynier leśnictwa, poliglota. "
         "Lusia urodzona w Bolechowie. Para zawarła związek małżeński w Bolechowie "
         "w 1935 r. Lusia prowadziła pensjonat Willa „Helin\" w Muszynie przed II "
         "wojną światową; przeżyła wojnę we Lwowie pod fałszywą tożsamością „Marii "
         "Cizlik\". Dawid uciekł z Galicji, dotarł do Brukseli w kwietniu 1946 r., "
         "a następnie statkiem „Theodor Herzl\" w kwietniu 1947 r. do Mandatu "
         "Palestyńskiego.",
         "Akt urodzenia z Nadwórnej 1911; karta DIPIS z Brukseli 1946; akt "
         "małżeństwa z Bolechowa 1935; karta CKŻP Lusi (Katowice 1946); "
         "wspomnienia Lusi; tablica potomków."),
        ("Rodzice",
         "Dov (Bernard) Rapaport (ur. 28 sierpnia 1946 r. w Brukseli) + Dalia z "
         "domu Goldfischer (ur. 1952)",
         "Dov ur. w Brukseli. Ślub z Dalią w Hajfie, 16 stycznia 1974 r.",
         "Karta DIPIS z Brukseli; dokumenty rodzinne."),
        ("Dzieci",
         "Dana (ur. 1979 Hajfa), Doron (ur. 1981 Hajfa), Daniel (ur. 1983 Hajfa)",
         "Żyjący członkowie rodziny.",
         "Dokumenty rodzinne."),
    ],

    "siblings_intro": (
        "Berisz miał cztery udokumentowane siostry, wszystkie urodzone w Radomyślu "
        "Wielkim. Trzy z ich ślubów odbyły się w Tarnowie i każdy wpis w księdze "
        "małżeństw niezależnie wymienia Mojżesza i Menuchę jako rodziców panny "
        "młodej — trzykrotne, niezależne potwierdzenie pary protoplastów to "
        "najmocniejszy dowód, jakim dysponujemy."
    ),
    "siblings_rows": [
        ("Alte Leja Rapaport (1882–1942)",
         "Ur. 28 czerwca 1882. Wyszła za Turkla; rodzina mieszkała w Wiedniu; "
         "siedmioro udokumentowanych dzieci. Zamordowana w Auschwitz w 1942 r.",
         "Rodzinna tablica potomków; korelacja z portalem genealogicznym "
         "Turkel-Tribe (turkel.org.il)."),
        ("Jente Rapaport (ur. 1887)",
         "Owdowiała do 1920 r. (pierwszy mąż nieznany). Ślub powtórny z Mendlem "
         "Eachemem Horowitzem z Sokala w Tarnowie, 12 grudnia 1920 r.",
         "Tarnowska księga małżeństw żydowskich, pozycja 98, 12 grudnia 1920 r. "
         "— Archiwum Narodowe w Krakowie, Oddział w Tarnowie."),
        ("Freida Amalia Rapaport (1888–1942)",
         "Pierwszy mąż o nazwisku Nussbaum, zmarł do połowy 1919 r. (ich syn Zwi "
         "Ayalon Nussbaum urodził się 7 maja 1919 r. w Przemyślu). Ślub powtórny z "
         "Markusem Eliaszem Kleinbaumem w Tarnowie 8 czerwca 1919 r. Zmarła w "
         "Przemyślu w 1942 r.",
         "Tarnowska księga małżeństw żydowskich, pozycja 40, 8 czerwca 1919 r.; "
         "tablica potomków."),
        ("Rebeka Rapaport młodsza (ur. 1896)",
         "Urodzona w Radomyślu Wielkim. Ślub z Sane Zylberfenigiem z Płońska w "
         "Tarnowie, 4 września 1923 r. Później wyjechała do Austrii. NIE należy "
         "mylić z żoną Berisza, Rebeką z domu Griffel.",
         "Tarnowska księga małżeństw żydowskich, pozycja 101, 4 września 1923 r."),
    ],

    "cousin_note": (
        "Udokumentowany kuzyn w pierwszej linii ojcowskiej, który przeżył wojnę: "
        "Zwi (Hirsch Heschel) Ayalon Nussbaum — urodzony 7 maja 1919 r. w "
        "Przemyślu, syn Freidy Amalii, ocalały z Holocaustu, wyemigrował do "
        "Izraela, zmarł 27 listopada 2001 r. w Hajfie. Jego izraelskie nazwisko "
        "„Ayalon\" to hebrajski odpowiednik „Nussbaum\"."
    ),

    "h1_maternal": "2. Linia matczyna — rodzina Griffel",
    "maternal_text": (
        "Dobrze udokumentowana przez opublikowany rodowód Edwarda Gellesa „Griffel "
        "of Nadworna\" (Archiwa Balliol College Oxford). Protoplaści: Dawid Griffel "
        "+ Tauba → Eliezer „Zeida\" Griffel (1850–1918) ślub z Sarą Matel z domu "
        "Chajes (zm. 1940) w Nadwórnej 1892. Eliezer był głową gminy żydowskiej w "
        "Nadwórnej (Av Kehillah) oraz przemysłowcem (drewno, ropa naftowa). Z "
        "jego dziesięciorga dzieci nasza linia biegnie przez Rivkę (ur. 1888) — "
        "naszą prababcię Rebekę, która wyszła za Berisza. Gałąź Griffel obejmuje "
        "również Dr Jakuba Griffela (działacza Vaad ha-Hatzala ratującego Żydów w "
        "Stambule), słynnego autora wspomnień Jehudę Nira oraz dziennikarkę "
        "Sarę Maslin Nir (NYT). Wszystkie te powiązania są udokumentowane przez "
        "Edwarda Gellesa."
    ),

    "h1_holocaust": "3. Holocaust — co jest udokumentowane",
    "holocaust_rows": [
        ("Berisz / Bernard Dov Rapaport",
         "Zamordowany w Auschwitz",
         "Baza ofiar Muzeum Auschwitz, rekord nr 188161, transport nr 689"),
        ("Rebeka z domu Griffel",
         "Zabita w Przemyślu, ok. 1942 r., na podstawie sfabrykowanego oskarżenia "
         "o podłożenie bomby na torach kolejowych",
         "Wspomnienia Lusi, strona 24"),
        ("Lota Rapaport (siostra Dawida)",
         "Wymieniona w getcie krakowskim, 1940 r. (Rolka 13 / Lista 177 / Pozycja "
         "72, baza Ancestry „Ten Ghettos\"). Wg wspomnień Lusi: później zdradzona i "
         "aresztowana we Lwowie wraz z mężem; nie wróciła.",
         "Ancestry / JewishGen „Ten Jewish Ghettos 1939–1942\"; wspomnienia Lusi, "
         "rozdział D"),
        ("Freida Amalia Rapaport-Kleinbaum",
         "Zmarła w Przemyślu 1942 r.",
         "Tablica potomków"),
        ("Alte Leja Rapaport-Turkel",
         "Zamordowana w Auschwitz 1942 r.",
         "Tablica potomków"),
        ("Israel Menachem Turkel",
         "Zabity we Lwowie 1942 r.",
         "Tablica potomków"),
        ("Siegfried Turkl",
         "Zabity w Belgii 12 stycznia 1945 r.",
         "Tablica potomków"),
        ("Michael + Rachel Rosenfeld",
         "Zabici w Przemyślu 1944 r.",
         "Tablica potomków"),
    ],

    "h2_survivors": "Ocalali",
    "survivors_rows": [
        ("Dawid Memek Rapaport",
         "Uciekł z Galicji; dotarł do Brukseli w kwietniu 1946 r.; popłynął do "
         "Palestyny statkiem „Theodor Herzl\" w kwietniu 1947 r. Dokładna trasa "
         "przez ZSRR / Iran / Włochy nie jest w pełni odtworzona."),
        ("Lusia Rapaport",
         "Przeżyła Lwów pod fałszywą polsko-katolicką tożsamością „Maria Cizlik\"."),
        ("Szymon Rapaport (syn Dawida i Lusi, ur. 22 czerwca 1937 r. Lwów)",
         "Przeżył wraz z Lusią. Został starszym dziennikarzem izraelskiego dziennika "
         "„Ma'ariv\", przez wiele lat służył jako korespondent regionu północnego — "
         "relacjonując wydarzenia bezpieczeństwa, przemysł, sprawy społeczne i "
         "gospodarkę regionalną. Zmarły (זכרונו לברכה — błogosławionej pamięci)."),
        ("Zwi Ayalon Nussbaum (bratanek Berisza, ur. 1919 r. Przemyśl)",
         "Przeżył; mieszkał w Hajfie, gdzie zmarł 27 listopada 2001 r."),
    ],

    "h1_places": "4. Miejsca w archiwum — czym jest każde z nich i dlaczego je przechowujemy",
    "places_intro": (
        "Każde miejsce wymienione tutaj jest związane z rodziną przez "
        "udokumentowane zdarzenie. Miejsca dodane w maju 2026 r. w ramach "
        "hipotezy „filozofa Ben-Zion\" (Nowy Sącz, Żmigród, Bełżec, Gorlice, "
        "Kraków jako miejsce zamieszkania Berisza) zostały usunięte po wycofaniu "
        "tej identyfikacji; nie figurują poniżej."
    ),
    "places_rows": [
        ("Radomyśl Wielki, Polska",
         "Miejsce urodzenia Berisza Rapaporta i jego czterech sióstr (Alte Leja "
         "1882, Jente 1887, Freida Amalia 1888, młodsza Rebeka 1896). Mojżesz Saul "
         "Rapaport zasiadał w Radzie Gminy Wyznaniowej Żydowskiej w latach 1897–"
         "1905.",
         "Podanie paszportowe z 1924 r.; trzy akty małżeństwa tarnowskie (1919, "
         "1920, 1923); Księga Pamięci Radomyśla Wielkiego, część I."),
        ("Tarnów, Polska",
         "Miejsce zarejestrowania trzech aktów małżeństwa żydowskich sióstr "
         "Rapaportów (1919 Freida × Kleinbaum, 1920 Jente × Horowitz, 1923 "
         "młodsza Rebeka × Zylberfenig). Dwa nagrobki o nazwisku Mojżesz Saul "
         "Rapaport zachowały się na cmentarzu żydowskim w Tarnowie — dopasowanie "
         "do naszej linii jeszcze nieustalone.",
         "Archiwum Narodowe w Krakowie, Oddział w Tarnowie."),
        ("Stanisławów (dzisiaj Iwano-Frankiwsk, Ukraina)",
         "Główne miejsce zamieszkania Berisza od 1918 r. Adres: Kościuszki 4. "
         "Miejsce złożenia podania paszportowego w 1924 r. i odnowienia dowodu "
         "w 1927 r. Dawid uczęszczał tu do I Państwowego Gimnazjum w 1926 r. (jego "
         "podpis zachował się na karcie dedykacyjnej z okazji 150-lecia "
         "niepodległości USA).",
         "USHMM RG-31.064M; karta podpisów gimnazjum 1926."),
        ("Nadwórna (dzisiaj Nadwirna, Ukraina)",
         "Miejsce urodzenia Dawida Mendla (25 grudnia 1911 r.) i jego matki Rebeki "
         "z domu Griffel (1888 r.). Siedziba rodzin Griffel i Chajes. Nieruchomość "
         "Eliezera Griffela przy ulicy Śródmieście została wystawiona na licytację "
         "w listopadzie 1938 r. (ogłoszenie wymienia 17 spadkobierców, w tym "
         "Rebekę).",
         "Akt urodzenia Nadwórna 1911; ogłoszenie licytacji Akcyjnego Banku "
         "Hipotecznego 1938."),
        ("Bolechów (dzisiaj Bołochiw, Ukraina)",
         "Miejsce urodzenia Lusi Weitzner i jej rodzeństwa (Feige 1911, Lea 1913 "
         "lub 1916, Mojżesz 1916). Rodzina Weitznerów mieszkała w Bolechowie "
         "Ruskim. Miejsce ślubu w 1935 r.: Lea Weitzner × Dawid Mendel Rapaport.",
         "Bolechowskie księgi metrykalne żydowskie poprzez ŻIH w Warszawie; akt "
         "małżeństwa 1935."),
        ("Muszyna, Polska („Mosina\" we wspomnieniach rodziny)",
         "Uzdrowisko, gdzie Lusia prowadziła Willę „Helin\" przed II wojną "
         "światową; Zygmunt Griffel (kuzyn Dawida) prowadził tartak.",
         "Wspomnienia Lusi; protokół Rady Gminy Muszyna 1933; Przegląd Drzewny "
         "1938."),
        ("Przemyśl, Polska",
         "Miejsce zamieszkania Berisza i Rebeki od 1939 r. Po wybuchu wojny Lusia "
         "z małym Szymonem udali się tam, by do nich dołączyć; Dawid przybył "
         "później. Berisz został deportowany z Przemyśla do Auschwitz; Rebeka "
         "została zabita w Przemyślu. Miejsce urodzenia kuzyna Zwi Ayalona "
         "Nussbauma (1919).",
         "Wspomnienia Lusi; karta świadectwa Yad Vashem dla Reginy Riwki; notatki "
         "Basi (Bernard Rapaport w aktach przemyskich ok. 1910)."),
        ("Lwów (dzisiaj Lwiw, Ukraina)",
         "Miejsce zamieszkania Dawida według stanu na 1 stycznia 1938 r. (wg karty "
         "DIPIS z Brukseli). Tutaj Dawid i Lusia przeżyli wojnę pod fałszywymi "
         "tożsamościami. Lusia mieszkała przy ul. Legionów 24 (dzisiaj Prospekt "
         "Swobody 24) jako „Maria Cizlik\". Lota została aresztowana i zaginęła w "
         "tym mieście.",
         "Karta DIPIS z Brukseli; wspomnienia Lusi."),
        ("Olchowce (województwo lwowskie)",
         "Miejsce ślubu religijnego Berisza i Rebeki w 1908 r. wg rodowodu "
         "Gellesa. Ślub cywilny nastąpił w Nadwórnej 21 grudnia 1911 r.",
         "Edward Gelles, „Griffel of Nadworna\"."),
        ("Sokal (dzisiaj Sokalʹ, Ukraina)",
         "Rodzinne miasto Mendla Horowitza, drugiego męża Jente, siostry Berisza.",
         "Tarnowska księga małżeństw 1920, pozycja 98."),
        ("Płońsk, Polska centralna",
         "Rodzinne miasto Sane Zylberfeniga, męża najmłodszej siostry Berisza — "
         "Rebeki.",
         "Tarnowska księga małżeństw 1923, pozycja 101."),
        ("Bruksela, Belgia",
         "Tutaj Dawid zakończył wędrówkę 9 kwietnia 1946 r. (data na karcie "
         "DIPIS). Tutaj urodził się Dov, 28 sierpnia 1946 r.",
         "Karta DIPIS."),
        ("Auschwitz / Oświęcim, Polska",
         "Miejsce zamordowania Berisza (ofiara nr 188161). Jego siostra Alte Leja "
         "również została tam zamordowana w 1942 r.",
         "Baza ofiar Muzeum Auschwitz."),
        ("Sète i Marsylia, Francja",
         "Port wypłynięcia (Sète) i stocznia (Marsylia) statku „Theodor Herzl\" — "
         "statek, który przewiózł Dawida, Lusię, Szymona i niemowlę Dova z "
         "Brukseli do Mandatu Palestyńskiego w kwietniu 1947 r.",
         "Karta DIPIS + pamięć rodzinna + dokumenty Mossadu LeAliyah Bet."),
        ("Cypr (obóz Karaolos)",
         "Brytyjski obóz internowania, gdzie pasażerów statku „Theodor Herzl\" "
         "wraz z Rapaportami przetrzymywano przed wpuszczeniem do Palestyny.",
         "Dokumenty Mossadu LeAliyah Bet."),
        ("Atlit, Mandat Palestyński",
         "Brytyjski obóz lądowania i internowania po przybyciu do Palestyny.",
         "Dokumenty Mossadu LeAliyah Bet."),
        ("Hajfa, Izrael",
         "Tutaj osiedlili się Dawid, Lusia, Szymon i Dov. Dawid zmarł tutaj 29 "
         "sierpnia 1990 r. Lusia zmarła tutaj w 1996 r. Dana, Doron i Daniel "
         "wszyscy się tutaj urodzili.",
         "Dokumenty rodzinne."),
        ("Wiedeń, Austria",
         "Tutaj Alte Leja, siostra Berisza, osiedliła się z mężem Turklem; "
         "potomkowie Turklów urodzili się tutaj (Auersperggasse 9 + "
         "Rembrandtstrasse 3). Berisz odwiedził Wiedeń służbowo w 1924 r.",
         "Podanie paszportowe z 1924 r.; tablica potomków."),
    ],

    "h1_documents": "5. Posiadane dokumenty",
    "documents_text": (
        "39 skatalogowanych dokumentów w archiwum na żywo pod adresem "
        "rapaportfamily.github.io. Najważniejsze:"
    ),
    "documents_bullets": [
        "Podania paszportowe Berisza 1924 + 1927, Stanisławów (USHMM RG-31.064M, klatki 375–380)",
        "Karty świadectwa Yad Vashem złożone w 1953 r.: Bernard Dov Rapaport (akta 90394) i Regina Riwka Rapaport (akta 90395)",
        "Rekord ofiary Muzeum Auschwitz nr 188161, transport nr 689 — Berisz",
        "Ancestry / JewishGen „Ten Jewish Ghettos 1939–1942\" — Lotte Rapaport, getto krakowskie 1940 (Rolka 13, Lista 177, Pozycja 72)",
        "Strony tarnowskiej księgi małżeństw żydowskich — pozycje 40 (1919), 98 (1920), 101 (1923) — trzy małżeństwa sióstr",
        "Akt urodzenia Dawida Mendla Rapaporta, Nadwórna 1911",
        "Akt urodzenia Rebeki Griffel, Nadwórna 1888",
        "Akt małżeństwa z Bolechowa 1935 r. (Lea Weitzner × Dawid Mendel Rapaport)",
        "Akt małżeństwa z Bolechowa 1932 r. (Feige Weitzner × Israel Englander)",
        "Karta podpisów gimnazjum stanisławowskiego 1926 r. — własnoręczny podpis Dawida (klasa IV)",
        "Ogłoszenie licytacji Akcyjnego Banku Hipotecznego 1938 r., wymieniające wszystkich 17 spadkobierców Eliezera Griffela",
        "Album Senatu i Sejmu 1934–35 z artykułem o lwowskim biznesie drzewnym Zygmunta Griffela",
        "Przegląd Drzewny 1938 z artykułem o tartaku Zygmunta Griffela w Muszynie",
        "Karty rejestracyjne CKŻP osób ocalałych: Lusia (nr 151738) + Szymon (nr 151337), Katowice 1 lipca 1946 r.",
        "Karta DIPIS z Brukseli — Dawid Rapaport, 9 kwietnia 1946 r.",
        "90-stronicowe wspomnienia Lusi w języku hebrajskim („Historia Lusi\"), z tłumaczeniami na polski i angielski",
        "Edward Gelles, „Griffel of Nadworna\" + „Facets of My Family History\" części 1 i 2 (Archiwa Balliol College Oxford)",
        "Rodzinne tablice potomków Mojżesza Saula Rapaporta i Dawida Griffela (opracowane przez Basię, maj 2026)",
        "Wpis w archiwum gazety „Ma'ariv\", 30 sierpnia 1990 r. — pod hasłem שמעון רפפורט dzień po śmierci Dawida (Biblioteka Narodowa Izraela)",
    ],

    "h1_retractions": "6. Co uważaliśmy za prawdę, a co okazało się błędne",
    "retractions_intro": (
        "Musieliśmy wycofać kilka wniosków. Każde wycofanie chroniło nas przed "
        "budowaniem na fałszywym fundamencie; nauki płynące z tych pomyłek są "
        "częścią wartości tego projektu."
    ),
    "retractions_rows": [
        ("Berisz urodzony w Tarnowie 6 sierpnia 1884 r. jako „Benzion\", syn "
         "Mojżesza Saula + Rywki Schiff",
         "Własne podanie paszportowe Berisza z 1924 r.: urodzony 30 lipca 1886 r. "
         "w Radomyślu Wielkim, ojciec Moses. Benzion z Tarnowa to inna rodzina "
         "Rapaportów."),
        ("Berisz = opublikowany filozof hebrajski Ben-Zion Rappaport, autor "
         "„Nature and Spirit\" (Mossad Bialik 1953); deportowany z Nowego Sącza "
         "do Bełżca; pierwsza żona z Żmigrodu; syn Mosze Hakohen; siostra Sara "
         "Mahler",
         "Wspomnienia Lusi umiejscawiają Berisza w Przemyślu, nie w Sączu/Bełżcu, "
         "i nigdy nie wspominają o filozofii ani książkach. Ben-Zion z Księgi "
         "Pamięci Tarnowa to inna osoba, dzieląca z naszym Beriszem jedynie "
         "miasto urodzenia i rok. Muzeum Auschwitz potwierdza, że Berisz zginął "
         "w Auschwitz."),
        ("Berisz zginął w Nadwórnej w masowej akcji w lesie Bukowinka 6 "
         "października 1941 r. lub w likwidacji getta 24 października 1942 r.",
         "Rekord ofiary Muzeum Auschwitz nr 188161 — Berisz został deportowany "
         "do Auschwitz i tam zamordowany."),
        ("Rebeka Griffel zginęła w akcji w lesie Bukowinka 1941 r.",
         "Wspomnienia Lusi i karta Yad Vashem oboje umiejscawiają ją w Przemyślu "
         "podczas wojny; została tam zabita."),
        ("Dokument rozwodowy „Lea Rapaport\" z 1941 r. dotyczył naszej Lusi",
         "Bezpośrednia lektura dokumentu: to inna Lea — Lea córka Szymona "
         "Hakohena Rapaporta × Michael Sigal w Petach Tikwa, Mandat Palestyński, "
         "certyfikat nr H 13898. Nasza Lusia przebywała we Lwowie pod fałszywą "
         "tożsamością Marii Cizlik w 1941 r."),
    ],

    "h1_questions": "7. Otwarte pytania, uszeregowane wg wagi",
    "questions_rows": [
        ("Pobrać pełny rekord Lota z bazy Ancestry „Ten Ghettos\"",
         "Rolka 13 / Lista 177 / Pozycja 72 w bazie „Ten Ghettos\" może zawierać "
         "imiona rodziców, męża, adres i zawód — prawdopodobnie wystarczająco, "
         "by w końcu zidentyfikować jej męża."),
        ("Rozstrzygnąć kwestię nagrobka Mojżesza Saula Rapaporta",
         "Dwa nagrobki o nazwisku Moshe Saul Rapaport na cmentarzu w Tarnowie: "
         "jeden zmarł 11 sierpnia 1933 r., drugi 30 października 1931 r. z "
         "Dąbrowy, potomek Szabataja Hakohena („Shach\") w siódmym pokoleniu. "
         "Każdy mógłby być naszym przodkiem — rozstrzygnięcie powiązałoby naszą "
         "linię z konkretnym pochodzeniem rabinackim."),
        ("Prześledzić miejsce zamieszkania Berisza przed Stanisławowem",
         "Berisz mieszkał w Stanisławowie „od 1918 r.\". Gdzie rodzina mieszkała "
         "w latach 1886–1918? Część tych lat w Radomyślu Wielkim (dzieci ur. "
         "tam do 1896 r.); luka 1896–1918 nieudokumentowana."),
        ("Zidentyfikować pierwszych mężów Freidy Amalii (Nussbaum, ok. 1917–18) "
         "i Jente (nieznany, przed 1920)",
         "Akta małżeństw z Tarnowa lub Przemyśla sprzed 1919 r. powinny pomóc."),
    ],

    "h1_status": "8. Stan obecny archiwum na żywo",
    "status_text": (
        "Hostowane pod adresem rapaportfamily.github.io. Uwierzytelnianie przez "
        "linki magiczne dla rodziny; URL dla gości do udostępniania. Na dzień "
        "1 czerwca 2026 r.: 113 osób, 44 miejsc, 39 dokumentów, 541 wiadomości "
        "czatu, wspomnienia Lusi jako interaktywna książka po hebrajsku, "
        "angielsku i polsku. Zainstalowane jako aplikacja Progressive Web App na "
        "telefonach i laptopach, z automatycznym wykrywaniem aktualizacji, by "
        "nowe ustalenia docierały do rodziny bez ręcznego odświeżania."
    ),
    "thanks": (
        "Z wdzięcznością wobec Basi (badania genealogiczne w polskich archiwach), "
        "Magdy (która nas połączyła), Kasi (Żydowski Instytut Historyczny w "
        "Warszawie), Pani Kasi (tłumaczenie francuskie karty DIPIS), Edwarda "
        "Gellesa (opublikowany rodowód Griffelów) oraz wobec śp. Lusi Rapaport, "
        "której wspomnienia podtrzymują historię rodziny."
    ),
}


pl_path = OUT_DIR / "Rapaport_Family_Summary_PL.docx"
build_doc(PL, pl_path)
print(f"wrote: {pl_path}")
