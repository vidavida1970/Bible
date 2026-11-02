#!/usr/bin/env python3
"""Create November 2 John 14:16–18 backgrounds + Kakao thumbnails (1200x630)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import math
import urllib.request

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
SOURCES = [
    "https://images.unsplash.com/photo-1767948156556-29e25ccc8d3e?auto=format&fit=crop&fm=jpg&w=2400&q=87",
    "https://images.unsplash.com/photo-1531029824729-9dc4d6313233?auto=format&fit=crop&fm=jpg&w=2400&q=87",
]
photo = None
for source in SOURCES:
    try:
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=50) as res:
            data = res.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img.load()
        if min(img.size) < 700:
            raise ValueError("image dimensions insufficient")
        photo = img
        print("SOURCE:", source, "SIZE:", photo.size)
        break
    except Exception as exc:
        print("RETRY:", str(exc)[:150])
if photo is None:
    raise RuntimeError("No available pastoral Unsplash image source")

def cover(im, width, height):
    w, h = im.size
    s = max(width / w, height / h)
    nw, nh = round(w*s), round(h*s)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x, y = (nw-width)//2, (nh-height)//2
    return im.crop((x, y, x+width, y+height))

web_bg = cover(photo, 1920, 1080)
for filename, quality in [("bg.jpg", 86), ("assets/background.jpg", 85), ("assets/background-v1.jpg", 82)]:
    web_bg.save(ROOT / filename, format="JPEG", quality=quality,
                optimize=True, progressive=True)

def font(size, serif=False):
    options = ([
       "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
       "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc",
    ] if serif else [
       "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf",
       "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ])
    for path in options:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError("Korean font missing")

def centered(draw, text, y, face, fill, shadow=4):
    if shadow:
        draw.text((604,y+4),text,font=face,anchor="mm",fill=(0,0,0,245))
    draw.text((600,y),text,font=face,anchor="mm",fill=fill)

for variant in (1,2):
    canvas = cover(photo, 1200, 630).convert("RGBA")
    layer = Image.new("RGBA", canvas.size)
    pixels = layer.load()
    for y in range(630):
        ry = abs((y-316)/316)
        for x in range(1200):
            rx = abs((x-600)/600)
            center = math.exp(-((rx/.91)**2+(ry/.87)**2)*1.40)
            opacity = min(230,int((87 if variant==1 else 116)+72*center+20*ry))
            pixels[x,y]=(2,13,29,opacity)
    canvas=Image.alpha_composite(canvas,layer)
    draw=ImageDraw.Draw(canvas)
    border_gold=(250,221,157,245)
    draw.rounded_rectangle((42,52,1158,583),radius=28,outline=border_gold,width=3)
    draw.line((349,52,851,52),fill=(7,23,42,255),width=9)
    draw.line((475,583,725,583),fill=(7,23,42,226),width=9)
    draw.rounded_rectangle((348,25,852,87),radius=31,
                           fill=(235,197,124,255),
                           outline=(255,237,183,255),width=2)
    centered(draw,"TODAY'S BIBLE VERSE  ·  2026.11.02",57,font(24),(24,36,53,255),0)
    centered(draw,"영원히 함께하시는 진리의 영",144,font(26),(255,246,222,255))
    lines=[
      "아버지께서 다른 보혜사를",
      "너희에게 보내셔서,",
      "영원히 너희와 함께",
      "계시게 하실 것이다.",
    ]
    positions=[228,307,393,475]
    sizes=([53,60,65,63] if variant==2 else [51,57,62,60])
    for i,(line,yy,size) in enumerate(zip(lines,positions,sizes)):
        face=font(size,serif=True)
        while draw.textbbox((0,0),line,font=face)[2]>1030 and size>34:
            size-=1
            face=font(size,serif=True)
        color=(255,232,163,255) if i>=2 else (255,255,255,255)
        centered(draw,line,yy,face,color)
    centered(draw,"— 요한복음서 14:16–18 —",543,font(26,serif=True),(255,228,168,255))
    out=canvas.convert("RGB")
    jpg=ASSETS/f"thumbnail-v{variant}.jpg"
    png=ASSETS/f"thumbnail-v{variant}.png"
    out.save(jpg,"JPEG",quality=89,subsampling=0,progressive=True,optimize=True)
    out.save(png,"PNG",optimize=True)
    assert Image.open(jpg).size == (1200,630)
    assert Image.open(png).size == (1200,630)

needed=[ROOT/"bg.jpg",ASSETS/"background.jpg",ASSETS/"background-v1.jpg",
        ASSETS/"thumbnail-v1.png",ASSETS/"thumbnail-v1.jpg",
        ASSETS/"thumbnail-v2.png",ASSETS/"thumbnail-v2.jpg"]
for asset in needed:
    if not asset.is_file() or asset.stat().st_size < 10000:
        raise RuntimeError("Asset not generated: "+str(asset))
    print("OK",asset.relative_to(ROOT),asset.stat().st_size)
print("SUCCESS: Background and 4 Kakao images are complete")
