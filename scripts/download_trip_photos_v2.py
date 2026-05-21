"""Round 2: download remaining Virtual Trip photos with corrected URLs.
URL-encodes unicode characters and uses verified Wikimedia paths."""
import urllib.request
import urllib.parse
from pathlib import Path
import time

OUT = Path(r"C:\Users\User\rapaport-family-tree\platform\assets\research_images\trip")
OUT.mkdir(parents=True, exist_ok=True)

# These are confirmed via Wikipedia/Commons that they exist
# Original URLs (may contain non-ASCII chars that need encoding)
PHOTOS_RAW = {
    "lwow_opera.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/6/67/Львівський_Національний_академічний_театр_опери_та_балету_імені_Соломії_Крушельницької_13.jpg",
    "bolechow_town_hall_alt.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/0/03/Будинок_ратуші_у_Болехові.JPG",
    "lwow_rynek_square.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/8/8a/Площа_Ринок_у_Львові.JPG",
    "sete_port.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/b/b1/Port_de_Sète_-_panoramio.jpg",
}

def encode_url(url):
    """Encode unicode characters in the path portion of a URL."""
    parts = urllib.parse.urlsplit(url)
    # Encode non-ASCII characters in the path
    path = urllib.parse.quote(parts.path, safe='/%')
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'RapaportFamilyTreeBot/1.0 (genealogy research; contact doronrpa@gmail.com)')]
urllib.request.install_opener(opener)

success, fail = 0, 0
for name, url in PHOTOS_RAW.items():
    out = OUT / name
    if out.exists() and out.stat().st_size > 5000:
        success += 1
        continue
    encoded = encode_url(url)
    try:
        time.sleep(2)  # be nice
        req = urllib.request.Request(encoded)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) > 5000 and (data[:4].startswith(b'\xff\xd8\xff') or data[:4].startswith(b'\x89PNG')):
            out.write_bytes(data)
            print(f"OK  {name:50} ({len(data)//1024} KB)")
            success += 1
        else:
            print(f"BAD {name:50} ({len(data)} bytes, magic {data[:4]!r})")
            fail += 1
    except Exception as e:
        print(f"ERR {name:50} {e.__class__.__name__}: {str(e)[:80]}")
        fail += 1

print(f"\n{success} downloaded, {fail} failed.")
