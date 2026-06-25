"""
Download cocktail images from TheCocktailDB.
Skips images with white/transparent backgrounds (boring product shots).
Run from: D:\Claude\whisky-guide\
"""

import requests
import time
import io
from pathlib import Path
from PIL import Image

DEST = Path("images/Cocktails")
DEST.mkdir(parents=True, exist_ok=True)

# cocktail id -> (display name for search, filename to save as)
COCKTAILS = [
    ("irish-coffee",         "Irish Coffee",           "Irish Coffee.jpg"),
    ("new-york-sour",        "New York Sour",          "New York Sour.jpg"),
    ("rusty-nail",           "Rusty Nail",             "Rusty Nail.jpg"),
    ("blood-and-sand",       "Blood and Sand",         "Blood and Sand.jpg"),
    ("godfather",            "Godfather cocktail",     "Godfather.jpg"),
    ("negroni",              "Negroni",                "Negroni.jpg"),
    ("gin-and-tonic",        "Gin and Tonic",          "Gin and Tonic.jpg"),
    ("tom-collins",          "Tom Collins",            "Tom Collins.jpg"),
    ("gimlet",               "Gimlet",                 "Gimlet.jpg"),
    ("bees-knees",           "Bee's Knees",            "Bees Knees.jpg"),
    ("last-word",            "Last Word",              "Last Word.jpg"),
    ("french-75",            "French 75",              "French 75.jpg"),
    ("southside",            "Southside cocktail",     "Southside.jpg"),
    ("aviation",             "Aviation",               "Aviation.jpg"),
    ("martinez",             "Martinez cocktail",      "Martinez.jpg"),
    ("clover-club",          "Clover Club",            "Clover Club.jpg"),
    ("vesper-martini",       "Vesper Martini",         "Vesper Martini.jpg"),
    ("corpse-reviver-2",     "Corpse Reviver",         "Corpse Reviver No2.jpg"),
    ("margarita",            "Margarita",              "Margarita.jpg"),
    ("paloma",               "Paloma",                 "Paloma.jpg"),
    ("spicy-margarita",      "Spicy Margarita",        "Spicy Margarita.jpg"),
    ("tequila-sunrise",      "Tequila Sunrise",        "Tequila Sunrise.jpg"),
    ("oaxacan-old-fashioned","Oaxacan Old Fashioned",  "Oaxacan Old Fashioned.jpg"),
    ("el-diablo",            "El Diablo",              "El Diablo.jpg"),
    ("mezcal-mule",          "Mezcal Mule",            "Mezcal Mule.jpg"),
    ("naked-and-famous",     "Naked and Famous",       "Naked and Famous.jpg"),
    ("batanga",              "Batanga",                "Batanga.jpg"),
    ("tommy-margarita",      "Tommy's Margarita",      "Tommys Margarita.jpg"),
    ("mojito",               "Mojito",                 "Mojito.jpg"),
    ("daiquiri",             "Daiquiri",               "Daiquiri.jpg"),
    ("dark-and-stormy",      "Dark and Stormy",        "Dark and Stormy.jpg"),
    ("mai-tai",              "Mai Tai",                "Mai Tai.jpg"),
    ("jungle-bird",          "Jungle Bird",            "Jungle Bird.jpg"),
    ("daiquiri-hemingway",   "Hemingway Daiquiri",     "Hemingway Daiquiri.jpg"),
    ("rum-old-fashioned",    "Rum Old Fashioned",      "Rum Old Fashioned.jpg"),
    ("el-presidente",        "El Presidente",          "El Presidente.jpg"),
    ("pina-colada",          "Pina Colada",            "Pina Colada.jpg"),
    ("painkiller",           "Painkiller cocktail",    "Painkiller.jpg"),
    ("espresso-martini",     "Espresso Martini",       "Espresso Martini.jpg"),
    ("moscow-mule",          "Moscow Mule",            "Moscow Mule.jpg"),
    ("cosmopolitan",         "Cosmopolitan",           "Cosmopolitan.jpg"),
    ("bloody-mary",          "Bloody Mary",            "Bloody Mary.jpg"),
    ("white-russian",        "White Russian",          "White Russian.jpg"),
    ("vodka-martini",        "Vodka Martini",          "Vodka Martini.jpg"),
    ("black-russian",        "Black Russian",          "Black Russian.jpg"),
    ("harvey-wallbanger",    "Harvey Wallbanger",      "Harvey Wallbanger.jpg"),
    ("sidecar",              "Sidecar",                "Sidecar.jpg"),
    ("brandy-alexander",     "Brandy Alexander",       "Brandy Alexander.jpg"),
    ("between-the-sheets",   "Between the Sheets",     "Between the Sheets.jpg"),
    ("stinger",              "Stinger cocktail",       "Stinger.jpg"),
    ("french-connection",    "French Connection",      "French Connection.jpg"),
    ("bb-cocktail",          "Benedictine cocktail",   "B&B.jpg"),
]

def is_white_background(img_bytes, threshold=235, corner_pct=0.12):
    """
    Returns True if image has a white/near-white background.
    Samples corners + edges of the image.
    """
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        w, h = img.size
        margin_x = int(w * corner_pct)
        margin_y = int(h * corner_pct)

        # Sample 4 corners + 4 edge midpoints
        sample_boxes = [
            (0, 0, margin_x, margin_y),              # top-left
            (w - margin_x, 0, w, margin_y),           # top-right
            (0, h - margin_y, margin_x, h),           # bottom-left
            (w - margin_x, h - margin_y, w, h),       # bottom-right
            (w//2 - margin_x, 0, w//2 + margin_x, margin_y),           # top-mid
            (w//2 - margin_x, h - margin_y, w//2 + margin_x, h),       # bottom-mid
            (0, h//2 - margin_y, margin_x, h//2 + margin_y),           # left-mid
            (w - margin_x, h//2 - margin_y, w, h//2 + margin_y),       # right-mid
        ]

        white_count = 0
        for box in sample_boxes:
            region = img.crop(box)
            avg = [sum(c) / len(list(region.getdata())) for c in zip(*region.getdata())]
            if all(c >= threshold for c in avg):
                white_count += 1

        # If 5+ of 8 sample zones are near-white → reject
        return white_count >= 5
    except Exception:
        return False


def search_cocktail(name):
    """Search TheCocktailDB, return (img_url, drink_name) of first result or None."""
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={requests.utils.quote(name)}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("drinks"):
            drink = data["drinks"][0]
            return drink.get("strDrinkThumb"), drink.get("strDrink")
    except Exception as e:
        print(f"  API error: {e}")
    return None, None


def download_image(url):
    """Download image bytes."""
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        print(f"  Download error: {e}")
    return None


results_ok = []
results_skipped = []
results_not_found = []

print(f"\nSearching {len(COCKTAILS)} cocktails on TheCocktailDB...\n")

for cid, search_name, filename in COCKTAILS:
    dest_path = DEST / filename
    if dest_path.exists():
        print(f"  SKIP (exists)  {filename}")
        results_ok.append((cid, filename))
        continue

    img_url, found_name = search_cocktail(search_name)
    if not img_url:
        print(f"  NOT FOUND      {search_name}")
        results_not_found.append((cid, search_name))
        time.sleep(0.3)
        continue

    img_bytes = download_image(img_url)
    if not img_bytes:
        print(f"  DL FAILED      {search_name}")
        results_not_found.append((cid, search_name))
        time.sleep(0.3)
        continue

    if is_white_background(img_bytes):
        print(f"  WHITE BG skip  {found_name} -> {filename}")
        results_skipped.append((cid, filename, img_url))
        time.sleep(0.3)
        continue

    dest_path.write_bytes(img_bytes)
    size_kb = len(img_bytes) // 1024
    print(f"  OK  {found_name:35s} -> {filename}  ({size_kb} KB)")
    results_ok.append((cid, filename))
    time.sleep(0.3)


print("\n" + "="*60)
print(f"Downloaded:   {len(results_ok)}")
print(f"White BG skip:{len(results_skipped)}")
print(f"Not found:    {len(results_not_found)}")

if results_skipped:
    print("\nWhite-bg skipped (save URLs for manual review):")
    for cid, fn, url in results_skipped:
        print(f"  {cid}: {url}")

if results_not_found:
    print("\nNot found on TheCocktailDB:")
    for cid, name in results_not_found:
        print(f"  {cid}: {name}")

print("\n=== COCKTAIL_IMG entries to add ===")
for cid, filename in results_ok:
    print(f"  '{cid}': '{filename}',")
