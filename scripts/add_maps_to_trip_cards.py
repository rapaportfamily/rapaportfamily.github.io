"""Add Google Maps + Street View + OpenStreetMap embed coordinates
to every Virtual Trip card so each card has a 'View on map / Street View'
button cluster + an embedded mini-map.

Coordinates are exact for known buildings (Legionów 24 = Prospekt
Svobody 24 Lviv, Moriah 93 Haifa, Baron Hirsch Cemetery Staten Island,
etc.) and town-centre for the rest."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RC = REPO / 'platform' / 'data' / 'research_center.json'

# (card_id) -> (lat, lng, optional google_maps_search_string, optional street_view_marker)
COORDS = {
    "trip_nadworna":            (48.6378, 24.5708, "Nadvirna, Ukraine"),
    "trip_bolechow":            (49.0658, 23.8531, "Bolekhiv, Ukraine"),
    "trip_skole":               (49.0367, 23.5108, "Skole, Ukraine"),
    "trip_muszyna":             (49.3528, 20.9050, "Muszyna, Poland"),
    "trip_nadworna_ghetto":     (48.6378, 24.5708, "Nadvirna, Ukraine"),
    "trip_lwow_legionow":       (49.8419, 24.0259, "Prospekt Svobody 24, Lviv, Ukraine"),
    "trip_lwow_rynek_shop":     (49.8419, 24.0316, "Rynok Square, Lviv, Ukraine"),
    "trip_brussels_1946":       (50.8467, 4.3525,  "Grand-Place, Brussels, Belgium"),
    "trip_sete_theodor_herzl":  (43.4045, 3.6963,  "Port of Sète, France"),
    "trip_cyprus_karaolos":     (35.1265, 33.9430, "Karaolos camp area, Famagusta, Cyprus"),
    "trip_atlit":               (32.7264, 34.9389, "Atlit Detainee Camp Heritage Site, Israel"),
    "trip_haifa_moriah":        (32.8050, 34.9889, "Moriah Street 93, Haifa, Israel"),
    "trip_haifa_sde_yehoshua":  (32.8050, 35.0181, "Sde Yehoshua Cemetery, Haifa, Israel"),
    "trip_porto_italy":         (45.8506, 12.5453, "Portobuffolè, Italy"),
    "trip_mallorca_1305":       (39.5696, 2.6502,  "Palma de Mallorca, Spain"),
    "trip_padua_venice":        (45.4064, 11.8768, "Padua, Italy"),
}

data = json.loads(RC.read_text(encoding='utf-8'))
trip = next(s for s in data['sections'] if s['id'] == 'virtual_trip')

added = 0
for card in trip['cards']:
    cid = card['id']
    if cid not in COORDS:
        continue
    lat, lng, label = COORDS[cid]
    card['map'] = {
        "coords": [lat, lng],
        "label": label,
        "google_maps": f"https://www.google.com/maps/search/?api=1&query={lat},{lng}",
        # Pegman / Street View URL — opens panorama if available
        "street_view": f"https://www.google.com/maps/@{lat},{lng},3a,75y,180h,90t/data=!3m1!1e3",
        # OpenStreetMap iframe embed (works inline without API key)
        "osm_embed": (
            f"https://www.openstreetmap.org/export/embed.html?"
            f"bbox={lng-0.01},{lat-0.01},{lng+0.01},{lat+0.01}"
            f"&layer=mapnik&marker={lat},{lng}"
        ),
    }
    added += 1

data['build_version'] = "2026-05-21-T7-maps-streetview-embeds"
RC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"[OK] Added Google Maps + Street View + OSM embed to {added}/{len(trip['cards'])} Trip cards.")
