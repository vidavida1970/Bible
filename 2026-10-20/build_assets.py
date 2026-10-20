#!/usr/bin/env python3
"""Build 2026-10-20 Luke 9:23-24 sunrise pathway background and Kakao 1200×630 images."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter,ImageOps
import urllib.request,shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';ASSETS.mkdir(exist_ok=True,parents=True)
PHOTOS=[
 'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=2400&q=89',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=89',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=89'
]
def fetch():
 for ix,url in enumerate(PHOTOS):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=36) as resp: buf=resp.read()
   im=Image.open(BytesIO(buf)).convert('RGB')
   if min(im.size)<650: raise RuntimeError('Low resolution')
   print('Chosen image source',ix, 'dimensions',im.size)
   return im
  except Exception as e:
   print('Background source failed',ix,str(e)[:160])
 raise RuntimeError('Could not download a usable background image')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(0.50,0.54))
def font(size,bold=False):
 paths=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
 ]
 for path in paths:
  if Path(path).exists():return ImageFont.truetype(path,size)
 raise RuntimeError('Missing Korean font: install fonts-noto-cjk')
photo=fetch()
background=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.12)
warm=Image.new('RGBA',(1920,1080),(237,175,82,21))
background=Image.alpha_composite(background.convert('RGBA'),warm).convert('RGB')
background.save(ROOT/'bg.jpg','JPEG',quality=91,optimize=True,progressive=True)
for f in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/f)
LINES=[
 ("TODAY'S WORD  ·  2026.10.20",105,100,23,False,False),
 ("날마다 자기 십자가를 지고",105,181,51,True,False),
 ("나를 따라오너라",105,268,65,True,True),
 ("자기를 부인하고",105,375,30,False,False),
 ("주님의 길을 따르는 믿음",105,422,30,False,False),
 ("누가복음서 9:23–24",105,522,27,False,False)
]
def make(v):
 bg=crop(background,1200,630).convert('RGBA')
 shade=Image.new('RGBA',bg.size,(0,0,0,0))
 d=ImageDraw.Draw(shade)
 for x in range(1200):
  a=round(40+73*(1-x/1199))
  d.line((x,0,x,629),fill=(7,17,32,a))
 bg=Image.alpha_composite(bg,shade)
 glass=Image.new('RGBA',bg.size,(0,0,0,0));d=ImageDraw.Draw(glass)
 d.rectangle((60,53,1140,578),fill=(7,20,38,184),outline=(204,213,220,223),width=2)
 d.rectangle((60,53,79,578),fill=(85,164,184,243))
 bg=Image.alpha_composite(bg,glass)
 drop=Image.new('RGBA',bg.size,(0,0,0,0));ds=ImageDraw.Draw(drop)
 measured=[]
 for string,x,y,size,bold,accent in LINES:
  f=font(size,bold)
  while ds.textbbox((0,0),string,font=f)[2]>925 and size>19:
   size-=1;f=font(size,bold)
  measured.append((string,x,y,f,accent))
  ds.text((x+3,y+3),string,font=f,fill=(0,0,0,211),stroke_width=1,stroke_fill=(0,0,0,145))
 bg=Image.alpha_composite(bg,drop.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(bg)
 for string,x,y,f,accent in measured:
  d.text((x,y),string,font=f,fill=(255,232,163,255) if accent and v==2 else (255,255,255,255))
 d.line((105,489,561,489),fill=(238,194,151,255),width=3)
 out=bg.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg'
 png=ASSETS/f'thumbnail-v{v}.png'
 out.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 out.save(png,'PNG',optimize=True)
 with Image.open(jpg) as test: assert test.size==(1200,630)
 print('Thumbnail',v,jpg.stat().st_size,'bytes')
for i in (1,2):make(i)
for p in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v2.jpg',ASSETS/'thumbnail-v2.png']:
 assert p.exists() and p.stat().st_size>5000,p
print('All Luke 9:23-24 image assets ready')
