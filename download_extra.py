import requests, io
from pathlib import Path
from PIL import Image

DEST = Path("images/Cocktails")

to_dl = [
    ("godfather",          "https://www.thecocktaildb.com/images/media/drink/e5zgao1582582378.jpg",  "Godfather.jpg"),
    ("vesper-martini",     "https://www.thecocktaildb.com/images/media/drink/mtdxpa1504374514.jpg",  "Vesper Martini.jpg"),
    ("daiquiri-hemingway", "https://www.thecocktaildb.com/images/media/drink/jfcvps1504369888.jpg",  "Hemingway Daiquiri.jpg"),
    ("stinger",            "https://www.thecocktaildb.com/images/media/drink/2ahv791504352433.jpg",  "Stinger.jpg"),
    ("bb-cocktail",        "https://www.thecocktaildb.com/images/media/drink/sqxsxp1478820236.jpg",  "B&B.jpg"),
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
            region = img.crop(box).getdata()
            pixels = list(region)
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

ok = []
for cid, url, fn in to_dl:
    p = DEST / fn
    r = requests.get(url, timeout=15)
    if is_white_bg(r.content):
        print(f"WHITE BG -> {fn}")
    else:
        p.write_bytes(r.content)
        print(f"OK  {cid} -> {fn}  ({len(r.content)//1024} KB)")
        ok.append((cid, fn))

print("\nNew COCKTAIL_IMG entries:")
for cid, fn in ok:
    print(f"  '{cid}': '{fn}',")
