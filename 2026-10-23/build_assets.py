#!/usr/bin/env python3
"""Create Hebrews 11:6 meditation backgrounds and 1200x630 Kakao previews."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from io import BytesIO
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; ASSETS.mkdir(exist_ok=True,parents=True)
# Evocative golden sunrise as a metaphor for faith and drawing near.
IMAGES=[
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2500&q=88',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2500&q=88',
 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2500&q=88',
]
def get_photo():
 for i,url in enumerate(IMAGES):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as response:
    b=response.read()
   im=Image.open(BytesIO(b)).convert('RGB')
   if min(im.size)<650: raise RuntimeError('Photo resolution too low')
   print('Using Unsplash source index',i, 'dimensions',im.size)
   return im
  except Exception as e:
   print('Photo retry',i,str(e)[:155])
 raise RuntimeError('Cannot download a background photo')
def crop(image,w,h):
 return ImageOps.fit(image,(w,h),Image.Resampling.LANCZOS,centering=(.5,.48))
def font(size,bold=False):
 options=[
  '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
  '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
 ]
 for p in options:
  if Path(p).is_file(): return ImageFont.truetype(p,size)
 raise RuntimeError('Install fonts-noto-cjk to draw Hangul')
photo=get_photo()
bg=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.05)
bg.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for p in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/p)
WORDS=[
 ("TODAY'S WORD  ·  2026.10.23",105,100,23,False,False),
 ("믿음이 없이는",105,179,66,True,False),
 ("주님을 기쁘시게",105,272,60,True,True),
 ("믿음으로 주님께 나아갑니다",105,382,30,False,False),
 ("주님을 찾는 자의 소망",105,430,29,False,False),
 ("히브리서 11:6",105,524,29,False,False),
]
def render(v):
 img=crop(bg,1200,630).convert('RGBA')
 veil=Image.new('RGBA',img.size,(0,0,0,0))
 vd=ImageDraw.Draw(veil)
 for x in range(1200):
  a=round(35+76*(1-x/1199))
  vd.line((x,0,x,629),fill=(4,10,29,a))
 img=Image.alpha_composite(img,veil)
 panel=Image.new('RGBA',img.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(6,18,37,185),outline=(206,216,227,222),width=2)
 d.rectangle((60,53,79,578),fill=(91,162,190,241))
 img=Image.alpha_composite(img,panel)
 shad=Image.new('RGBA',img.size,(0,0,0,0));sd=ImageDraw.Draw(shad)
 prepared=[]
 for text,x,y,size,bold,accent in WORDS:
  f=font(size,bold)
  while sd.textbbox((0,0),text,font=f)[2]>900 and size>18:
   size-=1; f=font(size,bold)
  prepared.append((text,x,y,f,accent))
  sd.text((x+3,y+3),text,font=f,fill=(0,0,0,225),stroke_width=1,stroke_fill=(0,0,0,160))
 img=Image.alpha_composite(img,shad.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(img)
 for text,x,y,f,accent in prepared:
  d.text((x,y),text,font=f,fill=(255,232,163,255) if accent and v==2 else (255,255,255,255))
 d.line((105,489,566,489),fill=(244,202,158,255),width=3)
 rgb=img.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg';png=ASSETS/f'thumbnail-v{v}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as test:
  assert test.size==(1200,630)
 print('Created',jpg.name,jpg.stat().st_size,'bytes')
for i in (1,2):render(i)
for f in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v2.jpg',ASSETS/'thumbnail-v2.png']:
 assert f.is_file() and f.stat().st_size>5000,f
print('2026-10-23 Bible assets complete')
