#!/usr/bin/env python3
"""Build 16:9 golden sunlight rays over misty mountain lake, eternal comfort and hope background and 1200×630 Korean Kakao previews for 2 Thessalonians 2:16–17."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import io,math,urllib.request
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
SOURCES=[
 "https://images.unsplash.com/photo-1591861208572-175bab50a83f?auto=format&fit=crop&w=2400&q=86",
 "https://images.unsplash.com/photo-1564152280426-90fc7cf82cc8?auto=format&fit=crop&w=2400&q=86",
 "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=86"
]
photo=None
for source in SOURCES:
 try:
  request=urllib.request.Request(source,headers={"User-Agent":"Mozilla/5.0"})
  with urllib.request.urlopen(request,timeout=45) as resp: content=resp.read()
  pic=Image.open(io.BytesIO(content)).convert("RGB");pic.load()
  if min(pic.size)<700:raise ValueError("Image not high resolution")
  photo=pic
  print("SOURCE:",source,"SIZE:",photo.size)
  break
 except Exception as exc: print("RETRY",str(exc)[:160])
if photo is None:raise RuntimeError("No background source downloaded")

def cover(im,w,h):
 iw,ih=im.size;s=max(w/iw,h/ih);nw,nh=round(iw*s),round(ih*s)
 photo=im.resize((nw,nh),Image.Resampling.LANCZOS)
 xx=(nw-w)//2;yy=(nh-h)//2
 return photo.crop((xx,yy,xx+w,yy+h))
bg=cover(photo,1920,1080)
for filename,q in [("bg.jpg",87),("assets/background.jpg",85),("assets/background-v1.jpg",82)]:
 bg.save(ROOT/filename,"JPEG",quality=q,progressive=True,optimize=True)

def font(size,serif=False):
 options=(["/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"] if serif else ["/usr/share/fonts/truetype/nanum/NanumSquareB.ttf","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"])
 for p in options:
  if Path(p).exists():return ImageFont.truetype(p,size)
 raise RuntimeError("Korean CJK font unavailable")

def center(d,y,txt,f,color,shadow=4):
 if shadow:d.text((600+shadow,y+shadow),txt,font=f,anchor="mm",fill=(0,0,0,248))
 d.text((600,y),txt,font=f,anchor="mm",fill=color)
for v in (1,2):
 im=cover(photo,1200,630).convert("RGBA")
 overlay=Image.new("RGBA",(1200,630));p=overlay.load()
 for yy in range(630):
  ry=abs((yy-315)/315)
  for xx in range(1200):
   rx=abs((xx-600)/600)
   glow=math.exp(-((rx/.95)**2+(ry/.85)**2)*1.40)
   alpha=min(232,int((95 if v==1 else 120)+72*glow+20*ry))
   p[xx,yy]=(2,12,29,alpha)
 im=Image.alpha_composite(im,overlay);d=ImageDraw.Draw(im)
 d.rounded_rectangle((42,52,1158,583),radius=28,outline=(248,223,165,245),width=3)
 d.line((345,52,855,52),fill=(8,22,43,235),width=9)
 d.line((462,583,738,583),fill=(8,22,43,223),width=9)
 d.rounded_rectangle((345,25,855,87),radius=31,fill=(237,201,126,255),outline=(255,237,184,255),width=2)
 center(d,57,"TODAY'S BIBLE VERSE  ·  2026.11.17",font(23),(24,36,53,255),0)
 center(d,143,"영원한 위로와 선한 소망",font(27),(255,245,221,255))
 lines=[
  "영원한 위로와 선한 소망을",
  "주시는 하나님 우리 아버지와",
  "여러분의 마음을 격려하시고,",
  "모든 선한 일과 말에 굳세게 해 주시기를"
 ]
 ys=[222,305,396,477]
 sizes=([58,54,55,45] if v==2 else [55,52,53,43])
 for i,(s,yy,size) in enumerate(zip(lines,ys,sizes)):
  f=font(size,True)
  while d.textbbox((0,0),s,font=f)[2]>1040 and size>30:
   size-=1;f=font(size,True)
  center(d,yy,s,f,(255,232,163,255) if i in (0,2,3) else (255,255,255,255))
 center(d,544,"— 데살로니가후서 2:16–17 —",font(26,True),(255,226,157,255))
 out=im.convert("RGB")
 out.save(ASSETS/f"thumbnail-v{v}.jpg","JPEG",quality=89,subsampling=0,progressive=True,optimize=True)
 out.save(ASSETS/f"thumbnail-v{v}.png","PNG",optimize=True)
 assert out.size==(1200,630)
for f in [ROOT/"bg.jpg",*sorted(ASSETS.glob("*"))]:
 assert f.exists() and f.stat().st_size>10000,str(f)
 print("OK",f.name,f.stat().st_size)
print("SUCCESS")
