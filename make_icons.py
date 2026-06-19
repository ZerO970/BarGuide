from PIL import Image, ImageDraw
import os, math

os.makedirs('icons', exist_ok=True)

def make_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background circle — dark amber/brown
    pad = int(size * 0.04)
    d.ellipse([pad, pad, size-pad, size-pad], fill=(24, 18, 10, 255))

    # Outer ring
    ring = int(size * 0.04)
    d.ellipse([pad+ring, pad+ring, size-pad-ring, size-pad-ring],
              outline=(180, 130, 50, 200), width=max(2, int(size*0.018)))

    # Glass silhouette (whisky tumbler)
    cx = size // 2
    s = size / 512  # scale factor

    # Tumbler: trapezoid body
    tw = int(100 * s)   # top half-width
    bw = int(80 * s)    # bottom half-width
    top_y  = int(130 * s)
    bot_y  = int(370 * s)
    d.polygon([
        (cx - tw, top_y),
        (cx + tw, top_y),
        (cx + bw, bot_y),
        (cx - bw, bot_y),
    ], fill=(180, 130, 50, 230))

    # Liquid fill (darker amber inside glass)
    liq_top = int(220 * s)
    liq_pad = int(8 * s)
    # interpolate width at liq_top
    ratio = (liq_top - top_y) / (bot_y - top_y)
    liq_hw = int(tw + (bw - tw) * ratio) - liq_pad
    d.polygon([
        (cx - liq_hw, liq_top),
        (cx + liq_hw, liq_top),
        (cx + bw - liq_pad, bot_y - liq_pad),
        (cx - bw + liq_pad, bot_y - liq_pad),
    ], fill=(120, 70, 15, 240))

    # Base / foot
    base_h = int(20 * s)
    d.rectangle([cx - bw - int(10*s), bot_y, cx + bw + int(10*s), bot_y + base_h],
                fill=(180, 130, 50, 230))

    return img

for sz in [192, 512]:
    make_icon(sz).save(f'icons/icon-{sz}.png')
    print(f'icon-{sz}.png created')
