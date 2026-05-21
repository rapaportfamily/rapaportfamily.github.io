"""Embed the Wikipedia lead images into every Virtual Trip card so each
place has at least one actual photo, not just URL links."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC = REPO / 'platform' / 'data' / 'research_center.json'

# Map each trip card id to (image filename, caption_en, credit)
EMBED = {
    "trip_nadworna": [
        ("trip/nadwirna_lead.jpg", "Nadvirna (Nadwórna) today — David Memek's birthplace.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_bolechow": [
        ("trip/bolekhiv_lead.jpg", "Bolekhiv (Bolechów) today — Lusia's birthplace.", "Wikipedia Commons"),
    ],
    "trip_skole": [
        ("trip/stryj_lead.jpg", "Stryj — regional centre near Skole, the birthplace of S. Goldfischer (1909). Same Carpathian-foothills world as Bolechów + Nadwórna.", "Wikipedia Commons"),
    ],
    "trip_muszyna": [
        # already has 8 Muszyna photos; nothing extra needed
    ],
    "trip_nadworna_ghetto": [
        ("trip/nadwirna_lead.jpg", "Nadvirna today — the wartime sawmill site is now built over.", "Wikipedia Commons"),
    ],
    "trip_lwow_legionow": [
        ("trip/lviv_opera_lead.jpg", "The Lviv Opera House (Lviv Theatre of Opera and Ballet, Svobody 28) — DIRECTLY UP THE STREET from Lusia's apartment at Legionów 24. During the Nazi occupation 1941-44 the Opera served as 'Operntheater Lemberg', Wehrmacht entertainment HQ.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_lwow_rynek_shop": [
        ("trip/lviv_rynek_square_lead.jpg", "Lviv Rynek Square (Площа Ринок) — the UNESCO-listed medieval merchant square. Lusia worked as manager of an art-objects shop in this commercial complex during 1943-1944.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_brussels_1946": [
        ("trip/brussels_grand_place_lead.jpg", "Brussels Grand-Place — central Brussels square. David, Lusia and Shimon transited Brussels in April 1946; their son Dov 'Bernard' (Doron's father) was born here later that year.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_sete_theodor_herzl": [
        ("trip/sete_lead.jpg", "The French port of Sète — where the Theodor Herzl sailed from on 2 April 1947 with 2,641 Holocaust-survivor Ma'apilim including David, Lusia, Shimon and infant Dov.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_cyprus_karaolos": [
        ("trip/cyprus_caraolos_lead.jpg", "Cyprus internment camps map — held 53,510 Jews from 1946-1949. The Rapaport family was at Karaolos (near Famagusta) ~8 months.", "Wikipedia Commons"),
    ],
    "trip_atlit": [
        ("trip/atlit_lead.jpg", "Atlit detainee camp, British Mandate Palestine — where Shimon Rapaport was held (per memoir p.65 his release document came from Atlit).", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_haifa_moriah": [
        ("trip/haifa_lead.jpg", "Haifa today, viewed from the Carmel ridge.", "Wikipedia Commons (CC-BY-SA)"),
        ("trip/mount_carmel_lead.jpg", "Mount Carmel, Haifa — David and Lusia's apartment at Moriah Street 93 sat on this ridge. Bought with German Wiedergutmachung reparations.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_haifa_sde_yehoshua": [
        ("trip/mount_carmel_lead.jpg", "Sde Yehoshua cemetery (formerly Kfar Samir) sits on Haifa's Carmel ridge. David's grave 102ד and Lusia's adjacent grave 102ג are in Section ו, Row 22.", "Wikipedia Commons"),
    ],
    "trip_porto_italy": [
        ("trip/portobuffole_lead.jpg", "Portobuffolè, Italy — where R. Yechiel Michael ha-Kohen Rapa was born in 1502. His son Isaac 'HaMoel' was the first to use 'Rapa-Porto' as a surname around 1550.", "Wikipedia Commons (CC-BY-SA)"),
        ("trip/verona_lead.jpg", "Verona, Italy — where R. Avraham Menachem ha-Kohen Rapa-Porto (1520-1596) published Mincha Belulah in 1594 with the iconic raven + priestly-blessing family emblem.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_mallorca_1305": [
        ("trip/mallorca_lead.jpg", "Palma de Mallorca, Spain — birthplace of Dr Vidal Rapapa (1305) and Dr Jucef Salomon Rapapa (court physician to King Jaime III, 1311-1345), the earliest documented Rapaport ancestors.", "Wikipedia Commons (CC-BY-SA)"),
    ],
    "trip_padua_venice": [
        ("trip/padua_lead.jpg", "Padua, Italy — where R. Meir Katzenellenbogen 'MaHaRaM Padua' (1482-1565) served as Chief Rabbi. His descendant Saul Wahl Katzenellenbogen (1541-1617) became the legendary 'King of Poland for one night'. Connected to our family via Chawa Wahl.", "Wikipedia Commons (CC-BY-SA)"),
    ],
}

data = json.loads(RC.read_text(encoding='utf-8'))
trip_section = next(s for s in data['sections'] if s['id'] == 'virtual_trip')

added_total = 0
for card in trip_section['cards']:
    new_images = EMBED.get(card['id'], [])
    if not new_images:
        continue
    existing = card.get('images', []) or []
    existing_srcs = {img.get('src') for img in existing}
    for filename, caption, credit in new_images:
        src = f"assets/research_images/{filename}"
        if src in existing_srcs:
            continue
        # Prepend so the lead photo shows first
        existing.insert(0, {"src": src, "caption_en": caption, "credit": credit})
        added_total += 1
    card['images'] = existing

data['build_version'] = "2026-05-21-T6-trip-photos-embedded"
RC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"[OK] Added {added_total} lead images to Virtual Trip cards.")
total = sum(len(s['cards']) for s in data['sections'])
print(f"[OK] Research Center: {len(data['sections'])} sections, {total} cards.")
# Count cards with images
img_count = sum(1 for c in trip_section['cards'] if c.get('images'))
print(f"[OK] {img_count}/{len(trip_section['cards'])} Virtual Trip cards now have embedded images.")
