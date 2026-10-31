#!/usr/bin/env python3
"""Generate licensed landscape backgrounds and Kakao 1200x630 previews for John 7:16-17."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io, math, urllib.request

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
SOURCE="https://images.unsplash.com/photo-1642951536826-969b30cc975a?auto=format&fit=crop&fm=jpg&q=85&w=2400"
req=urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0 (compatible; DailyBibleVersePublisher/1.0)"})
with urllib.request.urlopen(req,timeout=60) as res:
    photo=Image.open(io.BytesIO(res.read())).convert("RGB")

def cover(im,w,h):
    iw,ih=im.size
    scale=max(w/iw,h/ih)
    nw,nh=round(iw*scale),round(ih*scale)
    return im.resize((nw,nh),Image.Resampling.LANCZOS).crop(((nw-w)//2,(nh-h)//2,(nw+w)//2,(nh+h)//2))

bg=cover(photo,1920,1080)
for name,quality in [("bg.jpg",86),("assets/background.jpg",84),("assets/background-v1.jpg",82)]:
    bg.save(ROOT/name,quality=quality,progressive=True,optimize=True)

def font(size,serif=False):
    candidates=(
      ["/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
       "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc"] if serif else
      ["/usr/share/fonts/truetype/nanum/NanumSquareB.ttf",
       "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]
    )
    for name in candidates:
        if Path(name).exists():
            return ImageFont.truetype(name,size)
    raise RuntimeError("Korean CJK font required for thumbnail")

def text_center(draw,text,y,font,color,shadow=4):
    if shadow:
        draw.text((600+shadow,y+shadow),text,font=font,anchor="mm",fill=(0,0,0,245))
    draw.text((600,y),text,font=font,anchor="mm",fill=color)

for variant in (1,2):
    im=cover(photo,1200,630).convert("RGBA")
    overlay=Image.new("RGBA",im.size)
    pix=overlay.load()
    for y in range(630):
        yy=abs((y-315)/315)
        for x in range(1200):
            xx=abs((x-600)/600)
            middle=math.exp(-((xx/.95)**2+(yy/.84)**2)*1.35)
            opacity=int((91 if variant==1 else 122)+71*middle+17*yy)
            pix[x,y]=(2,11,29,min(225,opacity))
    im=Image.alpha_composite(im,overlay)
    draw=ImageDraw.Draw(im)
    gold=(249,220,156,235)
    draw.rounded_rectangle((42,52,1158,582),radius=28,outline=gold,width=3)
    draw.line((367,52,833,52),fill=(9,25,41,245),width=9)
    draw.line((470,582,730,582),fill=(9,25,41,200),width=9)
    draw.rounded_rectangle((352,25,848,87),radius=31,fill=(237,203,132,255),outline=(255,236,184,255),width=2)
    text_center(draw,"TODAY'S BIBLE VERSE  ·  2026.10.31",57,font(24),(24,34,50,255),shadow=0)
    text_center(draw,"하나님의 뜻을 따르는 길",145,font(27),(255,246,225,255))
    lines=["나의 가르침은","내 것이 아니라,","나를 보내신 분의","것이다."]
    ys=[231,305,389,468]
    sizes=([56,60,59,68] if variant==2 else [54,58,57,65])
    for i,(line,y,size) in enumerate(zip(lines,ys,sizes)):
        color=(255,232,163,255) if i>=2 else (255,255,255,255)
        text_center(draw,line,y,font(size,serif=True),color)
    text_center(draw,"— 요한복음서 7:16–17 —",536,font(27,serif=True),(255,228,168,255))
    result=im.convert("RGB")
    result.save(ASSETS/f"thumbnail-v{variant}.jpg",quality=90,subsampling=0,progressive=True,optimize=True)
    result.save(ASSETS/f"thumbnail-v{variant}.png",optimize=True)

for f in sorted(ASSETS.iterdir()):
    print(f.name,f.stat().st_size)
print("SUCCESS: Korean thumbnail and background assets are ready.")
