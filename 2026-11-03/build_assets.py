#!/usr/bin/env python3
"""Render 16:9 background and four 1200x630 Kakao thumbnails for Psalm 143:8-10."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,io,urllib.request
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
SOURCES=[
 "https://unsplash.com/photos/a-winding-path-through-a-sun-dappled-autumn-forest-P2JqmdnxATM/download?force=true&w=2400",
 "https://images.unsplash.com/photo-1642951536826-969b30cc975a?auto=format&fit=crop&fm=jpg&w=2400&q=85",
 "https://images.unsplash.com/photo-1767948156556-29e25ccc8d3e?auto=format&fit=crop&fm=jpg&w=2400&q=85",
]
photo=None
for url in SOURCES:
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
  with urllib.request.urlopen(req,timeout=60) as r: data=r.read()
  im=Image.open(io.BytesIO(data)).convert("RGB");im.load()
  if min(im.size)<700:raise ValueError("insufficient resolution")
  photo=im;print("SOURCE:",url,"SIZE:",im.size);break
 except Exception as e:print("SOURCE_RETRY:",str(e)[:200])
if photo is None:raise RuntimeError("Unable to fetch free landscape background")
def cover(im,w,h):
 iw,ih=im.size;s=max(w/iw,h/ih);nw,nh=round(iw*s),round(ih*s)
 src=im.resize((nw,nh),Image.Resampling.LANCZOS);x=(nw-w)//2;y=(nh-h)//2
 return src.crop((x,y,x+w,y+h))
bg=cover(photo,1920,1080)
for path,q in [("bg.jpg",86),("assets/background.jpg",85),("assets/background-v1.jpg",82)]:
 bg.save(ROOT/path,"JPEG",quality=q,progressive=True,optimize=True)
def font(size,serif=False):
 paths=(["/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"] if serif else ["/usr/share/fonts/truetype/nanum/NanumSquareB.ttf","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"])
 for p in paths:
  if Path(p).exists():return ImageFont.truetype(p,size)
 raise RuntimeError("Korean Noto font missing")
def center(d,y,text,face,color,shadow=4):
 if shadow:d.text((604,y+shadow),text,font=face,anchor="mm",fill=(0,0,0,245))
 d.text((600,y),text,font=face,anchor="mm",fill=color)
for version in (1,2):
 im=cover(photo,1200,630).convert("RGBA");layer=Image.new("RGBA",(1200,630));pixels=layer.load()
 for y in range(630):
  ry=abs((y-315)/315)
  for x in range(1200):
   rx=abs((x-600)/600);middle=math.exp(-((rx/.9)**2+(ry/.86)**2)*1.3)
   opacity=min(230,int((90 if version==1 else 117)+75*middle+18*ry))
   pixels[x,y]=(2,12,28,opacity)
 im=Image.alpha_composite(im,layer)
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((42,52,1158,583),radius=28,outline=(255,228,166,237),width=3)
 d.line((355,52,845,52),fill=(6,19,36,245),width=9)
 d.line((460,583,740,583),fill=(6,19,36,220),width=9)
 d.rounded_rectangle((349,25,851,87),radius=31,fill=(236,197,121,255),outline=(255,238,182,255),width=2)
 center(d,57,"TODAY'S BIBLE VERSE  ·  2026.11.03",font(23),(20,32,48,255),0)
 center(d,144,"주님의 선하신 영이 이끄시는 길",font(27),(255,247,225,255))
 lines=["아침마다 주님의 변함없는","사랑의 말씀을 듣게 해주십시오.","주님의 선하신 영으로","평탄한 길로 인도하여 주십시오."]
 ys=[224,303,393,474]
 sizes=[49,48,60,51] if version==2 else [47,46,58,49]
 for i,(line,y,size) in enumerate(zip(lines,ys,sizes)):
  face=font(size,True)
  while d.textbbox((0,0),line,font=face)[2]>1050 and size>30:
   size-=1;face=font(size,True)
  center(d,y,line,face,(255,232,163,255) if i>=2 else (255,255,255,255))
 center(d,545,"— 시편 143:8–10 —",font(28,True),(255,226,158,255))
 jpg=ASSETS/f"thumbnail-v{version}.jpg";png=ASSETS/f"thumbnail-v{version}.png"
 out=im.convert("RGB")
 out.save(jpg,"JPEG",quality=89,subsampling=0,progressive=True,optimize=True)
 out.save(png,"PNG",optimize=True)
 assert Image.open(jpg).size==(1200,630)
required=["bg.jpg","assets/background.jpg","assets/background-v1.jpg","assets/thumbnail-v1.png","assets/thumbnail-v1.jpg","assets/thumbnail-v2.png","assets/thumbnail-v2.jpg"]
for p in required:
 f=ROOT/p
 if not f.is_file() or f.stat().st_size<10000:raise RuntimeError("Failed "+p)
 print(p,f.stat().st_size)
print("SUCCESS")
