#!/usr/bin/env python3
"""2026-10-18 Colossians 1:20-22: serene cross background and Kakao 1200x630 previews."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from io import BytesIO
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
# Michaja Sudar's free Unsplash photo "a cross on top of a hill with a sky background"
PHOTOS=[
 'https://images.unsplash.com/photo-1689169624103-157e54a4aa75?auto=format&fit=crop&w=2300&q=90',
 'https://images.unsplash.com/photo-1491396023581-4344e51fec5c?auto=format&fit=crop&w=2300&q=90',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2300&q=90',
]
def download():
 for ix,url in enumerate(PHOTOS):
  try:
   request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(request,timeout=43) as response:
    raw=response.read()
   image=Image.open(BytesIO(raw)).convert('RGB')
   if min(image.size)<600:raise ValueError('Image source too small')
   print('Downloaded image source:',ix,'size:',image.size)
   return image,ix
  except Exception as err:
   print('Image source',ix,'failed:',str(err)[:180])
 raise RuntimeError('No background image source available')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),Image.Resampling.LANCZOS,centering=(0.5,0.51))
def font(size,bold=False):
 choices=[
  '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
  '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
 ]
 for p in choices:
  if Path(p).is_file():return ImageFont.truetype(p,size)
 raise FileNotFoundError('Install fonts-noto-cjk for Korean text rendering')
photo,source_index=download()
if source_index==0: photo=ImageOps.mirror(photo)
bg=crop(photo,1920,1080)
bg=ImageEnhance.Color(bg).enhance(1.10)
bg.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for filename in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/filename)
lines=[
 ("TODAY'S WORD  ·  2026.10.18",105,101,23,False,False),
 ("십자가로 이루신",105,178,59,True,False),
 ("화해와 평화",105,265,66,True,True),
 ("그리스도로 말미암아",105,377,30,False,False),
 ("하나님과 화해하게 하셨습니다",105,420,29,False,False),
 ("골로새서 1:20–22",105,525,27,False,False)
]
def render(v):
 image=crop(bg,1200,630).convert('RGBA')
 gradient=Image.new('RGBA',image.size,(0,0,0,0))
 gd=ImageDraw.Draw(gradient)
 for x in range(1200):
  a=round(35+86*(1-x/1199))
  gd.line((x,0,x,629),fill=(5,14,29,a))
 image=Image.alpha_composite(image,gradient)
 glass=Image.new('RGBA',image.size,(0,0,0,0))
 d=ImageDraw.Draw(glass)
 d.rectangle((60,53,1140,578),fill=(6,17,34,175),outline=(196,207,220,220),width=2)
 d.rectangle((60,53,79,578),fill=(91,161,184,240))
 image=Image.alpha_composite(image,glass)
 shadow=Image.new('RGBA',image.size,(0,0,0,0))
 sd=ImageDraw.Draw(shadow)
 cached=[]
 for text,x,y,size,bold,accent in lines:
  face=font(size,bold)
  while sd.textbbox((0,0),text,font=face)[2]>860 and size>18:
   size-=1;face=font(size,bold)
  cached.append((text,x,y,face,accent))
  sd.text((x+3,y+4),text,font=face,fill=(0,0,0,220),stroke_width=1,stroke_fill=(0,0,0,150))
 image=Image.alpha_composite(image,shadow.filter(ImageFilter.GaussianBlur(2.7)))
 d=ImageDraw.Draw(image)
 for text,x,y,face,accent in cached:
  color=(255,232,163,255) if accent and v==2 else (255,255,255,255)
  d.text((x,y),text,font=face,fill=color)
 d.line((105,497,555,497),fill=(234,193,151,255),width=3)
 rgb=image.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg'
 png=ASSETS/f'thumbnail-v{v}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:
  assert check.size==(1200,630)
 print('Generated',jpg.name,jpg.stat().st_size)
for variant in (1,2): render(variant)
for f in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v2.png',ASSETS/'thumbnail-v2.jpg']:
 assert f.is_file() and f.stat().st_size>4000,f
print('Colossians 1:20-22 image assets are ready')
