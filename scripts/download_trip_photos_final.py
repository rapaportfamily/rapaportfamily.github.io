"""Download photos for the remaining Virtual Trip cards via Wikimedia API.
Each location uses Wikipedia REST API to get the page's lead image, which
guarantees a CC-BY-SA / public-domain image we can embed."""
import urllib.request
import urllib.parse
import json
import time
from pathlib import Path

OUT = Path(r"C:\Users\User\rapaport-family-tree\platform\assets\research_images\trip")
OUT.mkdir(parents=True, exist_ok=True)

UA = "RapaportFamilyTreeBot/1.0 (genealogy archive; contact doronrpa@gmail.com)"
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', UA), ('Accept', 'image/*,*/*')]
urllib.request.install_opener(opener)

def fetch_lead_image_url(wiki_title, lang='en'):
    """Get the lead image URL for a Wikipedia article via REST API."""
    api = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_title)}"
    req = urllib.request.Request(api, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    # originalimage.source has the full-resolution URL
    if 'originalimage' in data:
        return data['originalimage']['source']
    if 'thumbnail' in data:
        return data['thumbnail']['source']
    return None

def download_image(url, name):
    out = OUT / name
    if out.exists() and out.stat().st_size > 5000:
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'image/*'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        if len(data) < 5000:
            return False
        if not (data[:4].startswith(b'\xff\xd8\xff') or data[:8].startswith(b'\x89PNG\r\n\x1a\n')):
            return False
        if data[:4].startswith(b'\xff\xd8\xff'):
            out.write_bytes(data)
        else:
            png = out.with_suffix('.png')
            png.write_bytes(data)
            out = png
        print(f"OK  {out.name:55} ({len(data)//1024} KB)")
        return True
    except Exception as e:
        print(f"ERR {name:55} {e.__class__.__name__}: {str(e)[:60]}")
        return False

# Map each card to a Wikipedia article whose lead image we want
TARGETS = [
    ("lviv_opera_lead.jpg",           "Lviv_Theatre_of_Opera_and_Ballet"),
    ("lviv_rynek_square_lead.jpg",    "Lviv_Old_Town"),
    ("brussels_grand_place_lead.jpg", "Grand-Place"),
    ("sete_lead.jpg",                 "Sète"),
    ("cyprus_caraolos_lead.jpg",      "Cyprus_internment_camps"),
    ("atlit_lead.jpg",                "Atlit_detainee_camp"),
    ("haifa_lead.jpg",                "Haifa"),
    ("mount_carmel_lead.jpg",         "Mount_Carmel"),
    ("kolomyia_lead.jpg",             "Kolomyia"),
    ("padua_lead.jpg",                "Padua"),
    ("portobuffole_lead.jpg",         "Portobuffolè"),
    ("verona_lead.jpg",               "Verona"),
    ("tarnobrzeg_lead.jpg",           "Tarnobrzeg"),
    ("mallorca_lead.jpg",             "Palma_de_Mallorca"),
    ("nadwirna_lead.jpg",             "Nadvirna"),
    ("bolekhiv_lead.jpg",             "Bolekhiv"),
    ("stryj_lead.jpg",                "Stryi"),
    ("ivano_frankivsk_lead.jpg",      "Ivano-Frankivsk"),
    ("skole_lead.jpg",                "Skole,_Ukraine"),
    ("london_lead.jpg",               "London"),
    ("vienna_lead.jpg",               "Vienna"),
    ("staten_island_baron_hirsch.jpg","Baron_Hirsch_Cemetery"),
]

print(f"Resolving + downloading {len(TARGETS)} Wikipedia lead images...")
success, fail = 0, 0
for name, title in TARGETS:
    out = OUT / name
    if out.exists() and out.stat().st_size > 5000:
        success += 1
        continue
    try:
        time.sleep(1.5)  # polite
        url = fetch_lead_image_url(title)
        if not url:
            print(f"--  {name:55} (no lead image)")
            fail += 1
            continue
        ok = download_image(url, name)
        if ok: success += 1
        else: fail += 1
    except Exception as e:
        print(f"ERR {name:55} {e.__class__.__name__}: {str(e)[:60]}")
        fail += 1

print(f"\n{success} downloaded, {fail} failed.")
