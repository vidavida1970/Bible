#!/usr/bin/env python3
"""Create 16:9 web scenery and Kakao-ready 1200x630 thumbnails for John 10:3-5."""
import io
import math
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
SOURCES = [
    "https://images.unsplash.com/photo-1758707686634-60415a54ee68?auto=format&fit=crop&fm=jpg&q=87&w=2400",
    "https://images.unsplash.com/photo-1759302307422-77dcb26e8161?auto=format&fit=crop&fm=jpg&q=87&w=2400",
]
photo = None
for source in SOURCES:
    try:
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=50) as response:
            content = response.read()
        test = Image.open(io.BytesIO(content)).convert("RGB")
        test.load()
        if min(test.size) < 600:
            raise ValueError("Unsplash image is too small")
        photo = test
        print("BACKGROUND_OK", source, photo.size)
        break
    except Exception as exc:
        print("Background source retry:", str(exc)[:140])
if photo is None:
    raise RuntimeError("Could not download verified pastoral photo")

def cover(im, width, height):
    w, h = im.size
    scale = max(width / w, height / h)
    new_w, new_h = round(w * scale), round(h * scale)
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x = (new_w - width) // 2
    y = (new_h - height) // 2
    return resized.crop((x, y, x + width, y + height))

bg = cover(photo, 1920, 1080)
for filename, quality in [
    ("bg.jpg", 87),
    ("assets/background.jpg", 86),
    ("assets/background-v1.jpg", 82),
]:
    bg.save(ROOT / filename, format="JPEG", quality=quality,
            optimize=True, progressive=True)

def font(size, serif=False):
    if serif:
        paths = ["/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
                 "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc"]
    else:
        paths = ["/usr/share/fonts/truetype/nanum/NanumSquareB.ttf",
                 "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    raise RuntimeError("Required Noto or Nanum Korean font is missing")

def draw_text(draw, y, message, text_font, fill, shadow=4):
    if shadow:
        draw.text((600 + shadow, y + shadow), message, font=text_font,
                  anchor="mm", fill=(0, 0, 0, 239))
    draw.text((600, y), message, font=text_font, anchor="mm", fill=fill)

for version in (1, 2):
    canvas = cover(photo, 1200, 630).convert("RGBA")
    shade = Image.new("RGBA", canvas.size)
    px = shade.load()
    for y in range(630):
        ry = abs((y - 316) / 316)
        for x in range(1200):
            rx = abs((x - 600) / 600)
            center = math.exp(-((rx / .91) ** 2 + (ry / .87) ** 2) * 1.40)
            opacity = min(231, int((89 if version == 1 else 120)
                                   + 72 * center + 18 * ry))
            px[x, y] = (3, 13, 29, opacity)
    canvas = Image.alpha_composite(canvas, shade)
    d = ImageDraw.Draw(canvas)
    gold = (251, 226, 165, 245)
    d.rounded_rectangle((42, 52, 1158, 583), radius=28,
                        outline=gold, width=3)
    # Two intentional border gaps occupied by the badge and foot treatment.
    d.line((361, 52, 839, 52), fill=(9, 27, 44, 255), width=9)
    d.line((478, 583, 722, 583), fill=(9, 27, 44, 235), width=9)
    d.rounded_rectangle((350, 25, 850, 87), radius=31,
                        fill=(232, 194, 120, 255),
                        outline=(255, 236, 186, 255), width=2)
    draw_text(d, 57, "TODAY'S BIBLE VERSE  ·  2026.11.01",
              font(23), (26, 36, 48, 255), shadow=0)
    draw_text(d, 144, "목자의 음성을 아는 양들",
              font(27), (255, 247, 227, 255))
    lines = [
        "목자는 자기 양들의 이름을",
        "하나하나 불러서 이끌고 나간다.",
        "양들이 목자의 목소리를",
        "알고 있기 때문이다.",
    ]
    y_positions = [232, 310, 396, 475]
    sizes = [51, 51, 57, 62] if version == 2 else [49, 49, 55, 60]
    for idx, (line, yy, size) in enumerate(zip(lines, y_positions, sizes)):
        face = font(size, serif=True)
        width = d.textbbox((0, 0), line, font=face)[2]
        while width > 1035 and size > 32:
            size -= 1
            face = font(size, serif=True)
            width = d.textbbox((0, 0), line, font=face)[2]
        ink = (255, 232, 163, 255) if idx >= 2 else (255, 255, 255, 255)
        draw_text(d, yy, line, face, ink)
    draw_text(d, 544, "— 요한복음서 10:3–5 —",
              font(26, serif=True), (255, 228, 167, 255))
    result = canvas.convert("RGB")
    jpg = ASSETS / f"thumbnail-v{version}.jpg"
    png = ASSETS / f"thumbnail-v{version}.png"
    result.save(jpg, "JPEG", quality=91, optimize=True,
                subsampling=0, progressive=True)
    result.save(png, "PNG", optimize=True)
    assert result.size == (1200, 630)

for asset in [ROOT / "bg.jpg", *sorted(ASSETS.glob("*"))]:
    if not asset.is_file() or asset.stat().st_size < 10_000:
        raise RuntimeError("Missing or unexpectedly small image: " + str(asset))
    print(asset.relative_to(ROOT), asset.stat().st_size)
print("SUCCESS: 7 image files produced, Korean font verified.")
