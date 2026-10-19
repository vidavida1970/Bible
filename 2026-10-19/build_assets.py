#!/usr/bin/env python3
"""Build 2026-10-19 Hebrews 10:21-23 sunrise background and 1200x630 Kakao thumbnails."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(exist_ok=True,parents=True)
# Unsplash warm sunrise, clouds and scenic mountains, with resilient alternatives.
PHOTOS=[
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=89',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=89',
 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2400&q=89',
]
def download_photo():
 for idx,url in enumerate(PHOTOS):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=40) as r:
    image=Image.open(BytesIO(r.read())).convert('RGB')
   if min(image.size)<600:raise ValueError('Photo source too small')
   print('Used Unsplash source',idx,'source photo dimensions',image.size)
   return image
  except Exception as e:
   print('Image source',idx,'not available:',str(e)[:160])
 raise RuntimeError('Failed to download a suitable Unsplash background')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(0.5,0.5))
def font(size,bold=False):
 options=[
  '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
  '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
 ]
 for path in options:
  if Path(path).exists():return ImageFont.truetype(path,size)
 raise RuntimeError('Install fonts-noto-cjk for accurate Hangul rendering')
photo=download_photo()
background=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.12)
background.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for f in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/f)
LINES=[
 ("TODAY'S WORD  ·  2026.10.19",105,104,22,False,False),
 ("흔들리지 말고",105,184,59,True,False),
 ("소망을 굳게 지킵시다",105,267,55,True,True),
 ("약속하신 분은 신실하시니",105,380,29,False,False),
 ("참된 마음으로 하나님께 나아갑시다",105,425,28,False,False),
 ("히브리서 10:21–23",105,524,27,False,False),
]
def render(variant):
 img=crop(background,1200,630).convert('RGBA')
 fade=Image.new('RGBA',img.size,(0,0,0,0))
 d=ImageDraw.Draw(fade)
 for x in range(1200):
  shade=round(28+69*(1-x/1199))
  d.line((x,0,x,629),fill=(4,10,27,shade))
 img=Image.alpha_composite(img,fade)
 glass=Image.new('RGBA',img.size,(0,0,0,0))
 gd=ImageDraw.Draw(glass)
 gd.rectangle((60,53,1140,578),fill=(7,17,37,184),outline=(204,215,228,218),width=2)
 gd.rectangle((60,53,79,578),fill=(91,165,188,241))
 img=Image.alpha_composite(img,glass)
 shade=Image.new('RGBA',img.size,(0,0,0,0))
 sd=ImageDraw.Draw(shade)
 measured=[]
 for text,x,y,size,bold,emphasis in LINES:
  face=font(size,bold)
  while sd.textbbox((0,0),text,font=face)[2]>950 and size>18:
   size-=1;face=font(size,bold)
  measured.append((text,x,y,face,emphasis))
  sd.text((x+3,y+4),text,font=face,fill=(0,0,0,230),stroke_width=1,stroke_fill=(0,0,0,160))
 img=Image.alpha_composite(img,shade.filter(ImageFilter.GaussianBlur(2.4)))
 d=ImageDraw.Draw(img)
 for text,x,y,face,emphasis in measured:
  color=(255,232,163,255) if emphasis and variant==2 else (255,255,255,255)
  d.text((x,y),text,font=face,fill=color)
 d.line((105,492,569,492),fill=(239,197,154,255),width=3)
 rgb=img.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{variant}.jpg'
 png=ASSETS/f'thumbnail-v{variant}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:
  assert check.size==(1200,630)
 print(jpg.name,jpg.stat().st_size,'bytes')
for i in (1,2):render(i)
for file in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',
             ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v1.jpg',
             ASSETS/'thumbnail-v2.png',ASSETS/'thumbnail-v2.jpg']:
 assert file.is_file() and file.stat().st_size>5000,file
print('2026-10-19 Bible assets ready')
