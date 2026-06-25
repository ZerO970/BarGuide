import requests, io
from pathlib import Path
from PIL import Image

PEXELS_KEY = "IFXtqnyDc6dl8OuIWVvTVqituYOwxEiRrZuVk0TfbNcaJeup1rb8vQfV"
DEST = Path("images/Cocktails/_test_pexels")
DEST.mkdir(parents=True, exist_ok=True)

HEADERS = {"Authorization": PEXELS_KEY}

TEST = [
    ("bees-knees",  "Bee's Knees cocktail", "Bees Knees TEST.jpg"),
    ("jungle-bird", "Jungle Bird cocktail",  "Jungle Bird TEST.jpg"),
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

for cid, query, filename in TEST:
    print(f"\n--- {query} ---")
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&per_page=5&orientation=square"
    r = requests.get(url, headers=HEADERS, timeout=10)
    data = r.json()

    photos = data.get("photos", [])
    if not photos:
        print("  No results")
        continue

    saved = 0
    for i, photo in enumerate(photos):
        img_url = photo["src"]["large"]
        photographer = photo.get("photographer", "?")
        img_r = requests.get(img_url, timeout=15)
        white = is_white_bg(img_r.content)
        status = "WHITE BG" if white else "OK"
        print(f"  [{i+1}] {status} | by {photographer} | {len(img_r.content)//1024} KB | {img_url}")

        if not white and saved == 0:
            p = DEST / filename
            p.write_bytes(img_r.content)
            print(f"       -> saved as {filename}")
            saved += 1
