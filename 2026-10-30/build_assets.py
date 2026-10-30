#!/usr/bin/env python3
"""Generate copyright-cleared Unsplash scenery and Kakao images for John 6:67-69."""
import io, math, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
SOURCE="https://images.unsplash.com/photo-1743309411498-a0f4f4b96b65?auto=format&fit=crop&fm=jpg&q=84&w=2400"
req=urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=45) as res: photo=Image.open(io.BytesIO(res.read())).convert("RGB")
def cover(im,w,h):
  iw,ih=im.size; sc=max(w/iw,h/ih); nw,nh=round(iw*sc),round(ih*sc)
  return im.resize((nw,nh),Image.Resampling.LANCZOS).crop(((nw-w)//2,(nh-h)//2,(nw+w)//2,(nh+h)//2))
bg=cover(photo,1920,1080)
for name,q in [("bg.jpg",85),("assets/background.jpg",84),("assets/background-v1.jpg",82)]:
  bg.save(ROOT/name,quality=q,progressive=True,optimize=True)
def font(size,serif=False):
  paths=(["/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"] if serif else ["/usr/share/fonts/truetype/nanum/NanumSquareB.ttf","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"])
  for p in paths:
    if Path(p).exists():return ImageFont.truetype(p,size)
  raise RuntimeError("Korean fonts missing")
def center(d,x,y,t,f,col,shadow=4):
  if shadow:d.text((x+shadow,y+shadow),t,font=f,anchor="mm",fill=(0,0,0,245))
  d.text((x,y),t,font=f,anchor="mm",fill=col,stroke_width=0)
for v in (1,2):
  im=cover(photo,1200,630).convert("RGBA")
  overlay=Image.new("RGBA",im.size); p=overlay.load()
  for y in range(630):
    yy=abs((y-317)/317)
    for x in range(1200):
      xx=abs((x-600)/600); mid=math.exp(-((xx/.94)**2+(yy/.84)**2)*1.36)
      a=int((87 if v==1 else 118)+72*mid+20*yy)
      p[x,y]=(1,10,25,min(225,a))
  im=Image.alpha_composite(im,overlay)
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((42,52,1158,583),radius=28,outline=(239,210,145,210),width=3)
  d.line((386,52,814,52),fill=(7,22,40,245),width=9)
  d.line((480,583,720,583),fill=(7,22,40,180),width=9)
  d.rounded_rectangle((352,25,848,87),radius=31,fill=(233,196,124,255),outline=(255,232,173,255),width=2)
  center(d,600,58,"TODAY'S BIBLE VERSE  ·  2026.10.30",font(24),(22,33,51,255),0)
  center(d,600,143,"말씀 앞에 머무는 오늘",font(25),(255,245,223,255))
  lines=["주님, 우리가 누구에게로","가겠습니까?","선생님께는 영생의","말씀이 있습니다."]
  ys=[226,297,382,460]
  sizes=[43,51,53,62] if v==2 else [42,50,51,59]
  for i,t in enumerate(lines):center(d,600,ys[i],t,font(sizes[i],True),(255,232,163,255) if i>=2 else (255,255,255,255))
  center(d,600,533,"— 요한복음서 6:67–69 —",font(26,True),(255,226,163,255))
  image=im.convert("RGB")
  image.save(ASSETS/f"thumbnail-v{v}.jpg",quality=89,progressive=True,optimize=True,subsampling=0)
  image.save(ASSETS/f"thumbnail-v{v}.png",optimize=True)
print("Generated",list(ASSETS.iterdir()))
