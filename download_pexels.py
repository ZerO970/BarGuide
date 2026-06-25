"""
Download remaining cocktail images via Pexels API.
Uses visual descriptions for cocktails with ambiguous names.
"""
import requests, io, time
from pathlib import Path
from PIL import Image

PEXELS_KEY = "IFXtqnyDc6dl8OuIWVvTVqituYOwxEiRrZuVk0TfbNcaJeup1rb8vQfV"
HEADERS = {"Authorization": PEXELS_KEY}
DEST = Path("images/Cocktails")

# id -> (search query, filename)
# Query = visual description when cocktail name alone is misleading
COCKTAILS = [
    ("rusty-nail",           "scotch whisky cocktail dark glass",         "Rusty Nail.jpg"),
    ("blood-and-sand",       "scotch whisky orange cherry cocktail coupe","Blood and Sand.jpg"),
    ("bees-knees",           "honey lemon gin cocktail coupe glass",      "Bees Knees.jpg"),
    ("southside",            "mint lime gin cocktail coupe",              "Southside.jpg"),
    ("spicy-margarita",      "spicy margarita chili tequila cocktail",    "Spicy Margarita.jpg"),
    ("oaxacan-old-fashioned","mezcal tequila old fashioned cocktail",     "Oaxacan Old Fashioned.jpg"),
    ("el-diablo",            "tequila ginger beer cocktail dark",         "El Diablo.jpg"),
    ("mezcal-mule",          "mezcal mule ginger beer cocktail copper",   "Mezcal Mule.jpg"),
    ("naked-and-famous",     "equal parts mezcal cocktail coupe yellow",  "Naked and Famous.jpg"),
    ("batanga",              "tequila cola cocktail highball mexico",      "Batanga.jpg"),
    ("tommy-margarita",      "margarita agave lime cocktail rocks glass", "Tommys Margarita.jpg"),
    ("jungle-bird",          "Jungle Bird cocktail",                      "Jungle Bird.jpg"),
    ("rum-old-fashioned",    "rum old fashioned cocktail rocks glass",    "Rum Old Fashioned.jpg"),
    ("el-presidente",        "rum cocktail orange coupe vintage",         "El Presidente.jpg"),
    ("painkiller",           "painkiller rum pineapple tropical cocktail","Painkiller.jpg"),
]

def is_white_bg(img_bytes, threshold=235, corner_pct=0.12):
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        w, h = img.size
        mx, my = int(w * corner_pct), int(h * corner_pct)
        boxes = [
            (0, 0, mx, my), (w-mx, 0, w, my),
            (0, h-my, mx, h), (w-mx, h-my, w, h),
            (w//2-mx, 0, w//2+mx, my), (w//2-mx, h-my, w//2+mx, h),
            (0, h//2-my, mx, h//2+my), (w-mx, h//2-my, w, h//2+my),
        ]
        white = 0
        for box in boxes:
            pixels = list(img.crop(box).getdata())
            if not pixels:
                continue
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            if avg_r >= threshold and avg_g >= threshold and avg_b >= threshold:
                white += 1
        return white >= 5
    except Exception:
        return False

def try_pexels(query, filename):
    """Try up to 8 results, return first non-white-bg image bytes, or None."""
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&per_page=8&orientation=square"
    r = requests.get(url, headers=HEADERS, timeout=10)
    photos = r.json().get("photos", [])
    for photo in photos:
        img_url = photo["src"]["large"]
        img_r = requests.get(img_url, timeout=15)
        if not is_white_bg(img_r.content):
            return img_r.content, photo.get("photographer", "?"), img_url
    return None, None, None

ok = []
skipped = []

print(f"Downloading {len(COCKTAILS)} cocktails via Pexels...\n")

for cid, query, filename in COCKTAILS:
    dest_path = DEST / filename
    if dest_path.exists():
        print(f"  EXISTS  {filename}")
        ok.append((cid, filename))
        continue

    img_bytes, photographer, img_url = try_pexels(query, filename)
    if img_bytes:
        dest_path.write_bytes(img_bytes)
        print(f"  OK   {cid:30s} -> {filename}  (by {photographer})")
        ok.append((cid, filename))
    else:
        print(f"  FAIL {cid:30s} -> no usable photo for: {query}")
        skipped.append((cid, filename))

    time.sleep(0.4)

print(f"\nDone: {len(ok)} saved, {len(skipped)} failed")

if skipped:
    print("\nStill missing:")
    for cid, fn in skipped:
        print(f"  {cid}")

print("\n=== Add to COCKTAIL_IMG ===")
for cid, fn in ok:
    print(f"  '{cid}': '{fn}',")
