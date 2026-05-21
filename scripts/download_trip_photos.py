"""Download Wikimedia Commons photos for the Virtual Trip section.
All photos are CC-BY-SA or PD."""
import urllib.request
import urllib.error
from pathlib import Path

OUT = Path(r"C:\Users\User\rapaport-family-tree\platform\assets\research_images\trip")
OUT.mkdir(parents=True, exist_ok=True)

# Wipe broken HTML files first
for f in OUT.glob('*.jpg'):
    if f.stat().st_size < 5000:  # html error pages are tiny
        f.unlink()
    else:
        with open(f, 'rb') as fp:
            first = fp.read(100)
            if b'<html' in first.lower() or b'<!doctype' in first.lower():
                f.unlink()

PHOTOS = {
    # Muszyna — pre-war resort hotel town
    "muszyna_town_hall_market.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Town_Hall%2C_Market_Square._Muszyna%2C_Poland.jpg",
    "muszyna_panorama.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Panorama_Muszyny.jpg",
    "muszyna_mineral_springs_pijalnia.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Pijalnia_Anna_BS27.jpg",
    "muszyna_promenade.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Promenades_and_sidewalks_in_Muszyna%2C_with_Muszyna_Castle_in_the_background%2C_Muszyna%2C_Poland.jpg",
    # Bolechów — Lusia's birthplace + Weitzner tannery
    "bolechow_town_hall.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/03/Будинок_ратуші_у_Болехові.JPG",
    "bolechow_greek_catholic_church.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/70/Bolekhiv_Greek_Catholic_church-02.jpg",
    # Lviv / Lwów — wartime apartment + shop on Rynek
    "lwow_opera.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Lvov_DSC_2526_53-101-1278.jpg",
    "lwow_rynek_square.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Площа_Ринок_у_Львові.JPG",
    "lwow_prospekt_svobody.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Prospekt_Svobody_Lviv_4.jpg",
    "lwow_old_postcard.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Lwów_-_Plac_Mariacki.jpg",
    # Stanisławów (now Ivano-Frankivsk) — regional capital
    "stanislawow_market.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Ivano-Frankivsk_Rynkowa_Square.jpg",
    # Brussels — refugee destination April 1946
    "brussels_grand_place.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/02/Grand-Place_de_Bruxelles_-_Belgique.jpg",
    # Sète — port of departure for Theodor Herzl, 2 April 1947
    "sete_port.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Port_de_Sète_-_panoramio.jpg",
    # Cyprus Karaolos camp
    "cyprus_caraolos_camp.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/41/Cyprus_internment_camp.jpg",
    "cyprus_famagusta_bay.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Famagusta_Bay.jpg",
    # Haifa — port of arrival + Moriah Street 93 + Carmel
    "haifa_port_aerial.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Aerial_view_of_Haifa_Port.jpg",
    "haifa_bahai_carmel.jpg": "https://upload.wikimedia.org/wikipedia/commons/6/68/Haifa_Bahai_Gardens_by_David_Shankbone.jpg",
    "haifa_moriah_carmel.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Moriah_Avenue_in_Haifa.jpg",
    # Atlit detention camp
    "atlit_detention_camp.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Atlit_detention_camp_-_aerial.jpg",
    # Berlin (East) — Hitler's grave anomaly
    "berlin_brandenburg_pre_war.jpg": "https://upload.wikimedia.org/wikipedia/commons/6/63/Bundesarchiv_Bild_146-1992-001-19%2C_Berlin%2C_Brandenburger_Tor.jpg",
    # Portobuffolè — where the Rapa-Porto surname was born
    "portobuffole_view.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Portobuffole.jpg",
    # Verona — where the 1594 family emblem was published
    "verona_arena.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Verona_-_Arena.jpg",
    # Kolomea — Sarah Matel Chajes birthplace
    "kolomea_view.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/89/Kolomyia_-_Old_town.jpg",
    # Padua — Katzenellenbogen dynasty origin
    "padua_basilica.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Basilica_di_Sant%27Antonio_da_Padova%2C_Padova.jpg",
    # Tarnobrzeg — Wahl family origin
    "tarnobrzeg_synagogue.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/94/Tarnobrzeg-Stara_Synagoga.jpg",
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'rapaport-family-tree/1.0 (research, contact doronrpa@gmail.com)')]
urllib.request.install_opener(opener)

success, fail = 0, 0
for name, url in PHOTOS.items():
    out = OUT / name
    if out.exists() and out.stat().st_size > 5000:
        success += 1
        continue
    try:
        urllib.request.urlretrieve(url, out)
        size = out.stat().st_size
        # validate it's actually a JPEG
        with open(out, 'rb') as f:
            magic = f.read(4)
        if magic.startswith(b'\xff\xd8\xff') and size > 5000:
            print(f"OK  {name:50} ({size//1024} KB)")
            success += 1
        elif magic.startswith(b'\x89PNG') and size > 5000:
            new = out.with_suffix('.png')
            out.rename(new)
            print(f"OK  {new.name:50} ({size//1024} KB, PNG)")
            success += 1
        else:
            out.unlink()
            print(f"BAD {name:50} (not JPEG/PNG: {magic[:4]!r})")
            fail += 1
    except Exception as e:
        print(f"ERR {name:50} {e.__class__.__name__}: {str(e)[:80]}")
        fail += 1

print(f"\n{success} downloaded, {fail} failed.")
