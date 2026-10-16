#!/usr/bin/env python3
"""Build John 6:33–35 16:9 background & pixel-perfect 1200x630 Kakao thumbnails."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from io import BytesIO
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(exist_ok=True,parents=True)
# Stock photography: bread with a warm golden-hour rural landscape.
BREAD=[
 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=1800&q=86',
 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=1800&q=86',
 'https://images.unsplash.com/photo-1608198093002-ad4e005484df?auto=format&fit=crop&w=1800&q=86',
]
FIELDS=[
 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2400&q=88',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=88',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=88',
]
def download(urls):
 for i,url in enumerate(urls):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=38) as r:
    data=r.read()
   im=Image.open(BytesIO(data)).convert('RGB')
   if min(im.size)<600:raise ValueError('Insufficient photo resolution')
   print('photo',i,im.size,url)
   return im
  except Exception as e:print('Image source',i,'failed:',str(e)[:150])
 return None
def crop(im,w,h):
 iw,ih=im.size;fac=max(w/iw,h/ih)
 im=im.resize((round(iw*fac),round(ih*fac)),Image.Resampling.LANCZOS)
 return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width+w)//2,(im.height+h)//2))
def base_photo():
 field=download(FIELDS)
 bread=download(BREAD)
 if field is None and bread is None:raise RuntimeError('No available image sources')
 if field is None:return crop(bread,1920,1080)
 field=crop(field,1920,1080).convert('RGBA')
 field=ImageEnhance.Color(field).enhance(1.14)
 if bread:
  bread=crop(bread,980,1080).convert('RGBA')
  bread=ImageEnhance.Color(bread).enhance(1.12)
  mask=Image.new('L',(980,1080));md=ImageDraw.Draw(mask)
  for x in range(980):
   # Gently blend imagery across the right of the landscape.
   a=min(1,max(0,(x/980-.03)/.46))
   md.line((x,0,x,1080),fill=round(a*232))
  mask=mask.filter(ImageFilter.GaussianBlur(26))
  field.paste(bread,(940,0),mask)
 return field.convert('RGB')
def font(size,bold=False):
 variants=[
  '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
  '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
 ]
 for path in variants:
  if Path(path).is_file():return ImageFont.truetype(path,size)
 raise FileNotFoundError('Korean font missing; install fonts-noto-cjk')
back=base_photo()
back.save(ROOT/'bg.jpg','JPEG',quality=91,optimize=True,progressive=True)
for f in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/f)
def thumbnail(v):
 im=crop(back,1200,630).convert('RGBA')
 glaze=Image.new('RGBA',im.size,(0,0,0,0));draw=ImageDraw.Draw(glaze)
 for x in range(1200):
  shade=round(44+63*(1-x/1199))
  draw.line((x,0,x,629),fill=(4,10,28,shade))
 im=Image.alpha_composite(im,glaze)
 panel=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(7,17,37,182),outline=(190,206,223,220),width=2)
 d.rectangle((60,53,79,578),fill=(74,151,174,240))
 im=Image.alpha_composite(im,panel)
 labels=[
 ("TODAY'S WORD  ·  2026.10.16",105,99,23,False,False),
 ('생명의 빵',105,171,64,True,False),
 ('세상에 생명을 주다',105,249,55,True,True),
 ('결코 주리지 않고',105,369,29,False,False),
 ('다시는 목마르지 않을 것이다',105,412,29,False,False),
 ('요한복음서 6:33–35',105,518,27,False,False),
 ]
 shadows=Image.new('RGBA',im.size,(0,0,0,0));ds=ImageDraw.Draw(shadows)
 txt=[]
 for s,x,y,size,bold,gold in labels:
  ff=font(size,bold)
  while ds.textbbox((0,0),s,font=ff)[2]>875 and size>18:
   size-=1;ff=font(size,bold)
  txt.append((s,x,y,ff,gold))
  ds.text((x+3,y+4),s,font=ff,fill=(0,0,0,220),stroke_width=1,stroke_fill=(0,0,0,170))
 im=Image.alpha_composite(im,shadows.filter(ImageFilter.GaussianBlur(2.3)))
 d=ImageDraw.Draw(im)
 for s,x,y,ff,gold in txt:
  d.text((x,y),s,font=ff,fill=(255,231,160,255) if gold and v==2 else (255,255,255,255))
 d.line([(105,488),(556,488)],fill=(244,199,155,255),width=3)
 rgb=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg'
 png=ASSETS/f'thumbnail-v{v}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:assert check.size==(1200,630)
 print(jpg.name,jpg.stat().st_size)
for v in (1,2):thumbnail(v)
assert all((ASSETS/p).is_file() for p in ['thumbnail-v1.jpg','thumbnail-v1.png','thumbnail-v2.jpg','thumbnail-v2.png','background.jpg','background-v1.jpg'])
print('2026-10-16 images complete')
