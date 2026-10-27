#!/usr/bin/env python3
"""Psalm 37:5-7, 2026-10-27: scenic trail background and 1200x630 Kakao previews."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request,shutil
P=Path(__file__).resolve().parent
A=P/'assets'
A.mkdir(exist_ok=True,parents=True)
# Primary photograph: Torsten Dederichs, Unsplash License; confirmed real Unsplash image URL.
SOURCES=[
 'https://images.unsplash.com/photo-1642951536826-969b30cc975a?auto=format&fit=crop&w=2500&q=89',
 'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=2500&q=89',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2500&q=89'
]
def acquire():
 for i,url in enumerate(SOURCES):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=36) as response:data=response.read()
   image=Image.open(BytesIO(data)).convert('RGB')
   if min(image.size)<700:raise ValueError('Source image is too small')
   print('Selected source index',i,'pixel size',image.size)
   return image
  except Exception as exc:print('Image source retry',i,str(exc)[:160])
 raise RuntimeError('All landscape photo sources failed')
def cover(image,w,h):
 return ImageOps.fit(image,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.49))
def font(size,bold=False):
 paths=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
 ]
 for f in paths:
  if Path(f).is_file():return ImageFont.truetype(f,size)
 raise RuntimeError('Install fonts-noto-cjk')
source=acquire()
bg=ImageEnhance.Color(cover(source,1920,1080)).enhance(1.03)
bg.save(P/'bg.jpg','JPEG',quality=91,optimize=True,progressive=True)
for name in ['background.jpg','background-v1.jpg']:
 shutil.copyfile(P/'bg.jpg',A/name)
LINES=[
 ("TODAY'S WORD  ·  2026.10.27",106,101,23,False,False),
 ("네 갈 길을 주님께 맡기고",106,183,56,True,False),
 ("주님만 의지하여라",106,267,63,True,True),
 ("주님께서 이루어 주실 것이다",106,382,31,False,False),
 ("잠잠히 주님을 바라며 기다려라",106,426,30,False,False),
 ("시편 37:5–7",106,522,29,False,False)
]
def render(n):
 im=cover(bg,1200,630).convert('RGBA')
 gradient=Image.new('RGBA',im.size,(0,0,0,0))
 gd=ImageDraw.Draw(gradient)
 for x in range(1200):
  gd.line((x,0,x,629),fill=(7,15,32,round(42+78*(1-x/1199))))
 im=Image.alpha_composite(im,gradient)
 panel=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(6,17,37,189),outline=(203,215,224,222),width=2)
 d.rectangle((60,53,79,578),fill=(105,160,188,244))
 im=Image.alpha_composite(im,panel)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));sd=ImageDraw.Draw(shadow);prepared=[]
 for text,x,y,size,bold,accent in LINES:
  f=font(size,bold)
  while sd.textbbox((0,0),text,font=f)[2]>922 and size>19:
   size-=1;f=font(size,bold)
  w=sd.textbbox((0,0),text,font=f)[2]
  assert x+w<=1136,('overflow',text,x+w)
  prepared.append((text,x,y,f,accent))
  sd.text((x+3,y+4),text,font=f,fill=(0,0,0,218),stroke_width=1,stroke_fill=(0,0,0,150))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(im)
 for text,x,y,f,accent in prepared:
  d.text((x,y),text,font=f,fill=(255,232,163,255) if accent and n==2 else (255,255,255,255))
 d.line((106,489,557,489),fill=(238,201,151,255),width=3)
 rgb=im.convert('RGB')
 jpg=A/f'thumbnail-v{n}.jpg';png=A/f'thumbnail-v{n}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as test:assert test.size==(1200,630)
 print(jpg.name,jpg.stat().st_size)
for i in (1,2):render(i)
for path in [P/'bg.jpg',A/'background.jpg',A/'background-v1.jpg',A/'thumbnail-v1.jpg',A/'thumbnail-v1.png',A/'thumbnail-v2.jpg',A/'thumbnail-v2.png']:
 assert path.is_file() and path.stat().st_size>5000,path
print('All Psalm 37:5–7 assets generated')
