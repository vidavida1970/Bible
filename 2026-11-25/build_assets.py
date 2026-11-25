#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
import io,urllib.request
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"; ASSETS.mkdir(parents=True,exist_ok=True)
SOURCES=[
"https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=85",
"https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=85",
"https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=2400&q=85"
]
photo=None
for u in SOURCES:
 try:
  req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
  with urllib.request.urlopen(req,timeout=45) as response: blob=response.read()
  candidate=Image.open(io.BytesIO(blob)).convert("RGB")
  if min(candidate.size)<700:raise ValueError("source too small")
  photo=candidate
  print("BACKGROUND SOURCE",u,candidate.size)
  break
 except Exception as e:print("BACKGROUND RETRY",str(e)[:180])
if photo is None:
 print("Creating offline dawn gradient")
 photo=Image.new("RGB",(1920,1080))
 d=ImageDraw.Draw(photo)
 for y in range(1080):
  k=y/1080
  d.line((0,y,1920,y),fill=(int(8+150*k),int(22+105*k),int(49+36*k)))
 for x,y,r in [(420,310,220),(1300,580,350)]:
  d.ellipse((x-r,y-r,x+r,y+r),fill=(206,155,88))
def crop(im,w,h):
 s=max(w/im.width,h/im.height);nw=round(im.width*s);nh=round(im.height*s)
 im=im.resize((nw,nh),Image.Resampling.LANCZOS)
 return im.crop(((nw-w)//2,(nh-h)//2,(nw+w)//2,(nh+h)//2))
bg=crop(photo,1920,1080)
for target,q in [(ROOT/"bg.jpg",88),(ASSETS/"background.jpg",85),(ASSETS/"background-v1.jpg",82)]:
 bg.save(target,"JPEG",quality=q,optimize=True)
SERIF="/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def f(n,serif=True): return ImageFont.truetype(SERIF if serif else SANS,n)
def fit(d,s,n,width):
 while n>24 and d.textbbox((0,0),s,font=f(n))[2]>width:n-=1
 return f(n)
lines=[
 ("사람에게 복종하는 것보다,",False),
 ("하나님께 복종하는 것이",True),
 ("마땅합니다.",True),
 ("우리는 이 모든 일의 증인입니다.",False)]
for v in (1,2):
 im=crop(bg,1200,630).filter(ImageFilter.GaussianBlur(4))
 im=ImageEnhance.Brightness(im).enhance(.65 if v==1 else .58).convert("RGBA")
 im=Image.alpha_composite(im,Image.new("RGBA",(1200,630),(3,13,30,126 if v==1 else 148)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((45,47,1155,581),radius=24,outline=(250,221,149,230),width=3)
 d.line((348,48,852,48),fill=(8,22,43,255),width=9)
 d.line((460,580,740,580),fill=(8,22,43,255),width=9)
 d.rounded_rectangle((343,22,857,80),radius=29,fill=(228,189,117,255),outline=(255,239,188,255),width=2)
 d.text((600,51),"TODAY'S BIBLE VERSE  ·  2026.11.25",font=f(23,False),fill=(24,34,51),anchor="mm")
 for i,(t,em) in enumerate(lines):
  y=[176,272,363,452][i]; ft=fit(d,t,56 if em else 44,1025)
  d.text((603,y+4),t,font=ft,fill=(0,0,0,235),anchor="mm",stroke_width=3,stroke_fill=(0,0,0,220))
  d.text((600,y),t,font=ft,fill=(255,232,163) if em else (255,255,255),anchor="mm")
 d.text((600,548),"— 사도행전 5:29–32 —",font=f(28,False),fill=(255,232,163),anchor="mm")
 out=im.convert("RGB")
 out.save(ASSETS/f"thumbnail-v{v}.jpg","JPEG",quality=90,optimize=True,subsampling=0)
 out.save(ASSETS/f"thumbnail-v{v}.png","PNG",optimize=True)
for p in [ROOT/"bg.jpg",*ASSETS.iterdir()]:
 assert p.stat().st_size>10000
 print("ASSET OK",p.name,p.stat().st_size)
