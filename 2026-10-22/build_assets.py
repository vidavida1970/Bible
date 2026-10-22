#!/usr/bin/env python3
"""Psalm 131:1–3 | Create tranquil lake background and Kakao share thumbnails (1200x630)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from io import BytesIO
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';ASSETS.mkdir(exist_ok=True,parents=True)
# First photo corresponds to the free Unsplash lake image credited on the webpage.
PHOTOS=[
 'https://images.unsplash.com/photo-1505887837284-44dc0a2c058b?auto=format&fit=crop&w=2500&q=90',
 'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=2500&q=90',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2500&q=90',
]
def download():
 for index,url in enumerate(PHOTOS):
  try:
   request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(request,timeout=35) as res: blob=res.read()
   image=Image.open(BytesIO(blob)).convert('RGB')
   if min(image.size)<650:raise ValueError('Downloaded image too small')
   print('PHOTO_SOURCE_INDEX:',index,'dimensions:',image.size)
   return image
  except Exception as e: print('PHOTO_RETRY:',index,str(e)[:180])
 raise RuntimeError('Unable to obtain a suitable tranquil landscape photo')
def crop(image,w,h):
 return ImageOps.fit(image,(w,h),method=Image.Resampling.LANCZOS,centering=(.52,.49))
def font(size,bold=False):
 paths=[
  '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
  '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
 ]
 for p in paths:
  if Path(p).exists():return ImageFont.truetype(p,size)
 raise RuntimeError('Korean font unavailable')
photo=download()
image=ImageEnhance.Color(crop(photo,1920,1080)).enhance(.95)
image.save(ROOT/'bg.jpg','JPEG',quality=91,optimize=True,progressive=True)
for f in ('background.jpg','background-v1.jpg'):shutil.copyfile(ROOT/'bg.jpg',ASSETS/f)
LINES=[
 ("TODAY'S WORD  ·  2026.10.22",105,101,23,False,False),
 ("내 마음은 고요하고",105,182,61,True,False),
 ("평온합니다",105,268,72,True,True),
 ("어머니 품에 안긴 아이처럼",105,381,30,False,False),
 ("오직 주님만을 의지하여라",105,427,30,False,False),
 ("시편 131:1–3",105,526,28,False,False)
]
def render(v):
 im=crop(image,1200,630).convert('RGBA')
 veil=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(veil)
 for x in range(1200):
  a=round(42+70*(1-x/1199))
  d.line((x,0,x,629),fill=(7,17,32,a))
 im=Image.alpha_composite(im,veil)
 pane=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(pane)
 d.rectangle((60,53,1140,578),fill=(8,22,39,186),outline=(202,217,224,220),width=2)
 d.rectangle((60,53,79,578),fill=(92,159,181,244))
 im=Image.alpha_composite(im,pane)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));sd=ImageDraw.Draw(shadow)
 prepared=[]
 for text,x,y,size,bold,accent in LINES:
  ff=font(size,bold)
  while sd.textbbox((0,0),text,font=ff)[2]>940 and size>18:
   size-=1;ff=font(size,bold)
  prepared.append((text,x,y,ff,accent))
  sd.text((x+3,y+4),text,font=ff,fill=(0,0,0,222),stroke_width=1,stroke_fill=(0,0,0,150))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(im)
 for text,x,y,ff,accent in prepared:
  d.text((x,y),text,font=ff,fill=(255,232,163,255) if accent and v==2 else (255,255,255,255))
 d.line((105,492,557,492),fill=(239,198,166,255),width=3)
 result=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg'
 png=ASSETS/f'thumbnail-v{v}.png'
 result.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 result.save(png,'PNG',optimize=True)
 with Image.open(jpg) as test:assert test.size==(1200,630)
 print('DONE:',jpg.name,jpg.stat().st_size)
for version in (1,2):render(version)
for p in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v2.jpg',ASSETS/'thumbnail-v2.png']:
 assert p.is_file() and p.stat().st_size>5000,p
print('PASS: all Psalm 131 image assets generated')
