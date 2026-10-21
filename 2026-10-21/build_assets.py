#!/usr/bin/env python3
"""2026-10-21 Psalm 130:5-7: sunrise watchtower background and 1200x630 Kakao thumbnails."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';ASSETS.mkdir(parents=True,exist_ok=True)
PHOTOS=[
 # Silhouette of lighthouse tower near calm sea during golden hour, Elmer Canas / Unsplash
 'https://images.unsplash.com/photo-1558524934-7a5f9b67d53e?auto=format&fit=crop&w=2400&q=90',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=90',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=90',
]
def download_image():
 for n,url in enumerate(PHOTOS):
  try:
   request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(request,timeout=40) as response:
    data=response.read()
   im=Image.open(BytesIO(data)).convert('RGB')
   if min(im.size)<650:raise ValueError('Image too small')
   print('Selected sunrise photo source',n,'dimensions',im.size)
   return im,n
  except Exception as e: print('Photo source',n,'unavailable',str(e)[:190])
 raise RuntimeError('No photographic background source was reachable')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.50))
def font(size,bold=False):
 options=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf']
 for f in options:
  if Path(f).exists():return ImageFont.truetype(f,size)
 raise RuntimeError('Korean font not installed')
photo,source_index=download_image()
img=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.10)
img.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for file in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/file)
WORDS=[
 ("TODAY'S WORD  ·  2026.10.21",105,100,23,False,False),
 ("파수꾼이 아침을 기다리듯",105,185,54,True,False),
 ("주님을 기다립니다",105,265,66,True,True),
 ("내 영혼이 주님의 말씀을 바란다",105,377,29,False,False),
 ("주님께만 인자하심과 속량의 능력이 있다",105,422,27,False,False),
 ("시편 130:5–7",105,523,28,False,False),
]
def render(variant):
 im=crop(img,1200,630).convert('RGBA')
 overlay=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(overlay)
 for x in range(1200):
  a=round(41+71*(1-x/1199))
  d.line((x,0,x,629),fill=(5,13,31,a))
 im=Image.alpha_composite(im,overlay)
 glass=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(glass)
 d.rectangle((60,53,1140,578),fill=(6,17,37,182),outline=(196,206,220,222),width=2)
 d.rectangle((60,53,79,578),fill=(88,163,190,245))
 im=Image.alpha_composite(im,glass)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));s=ImageDraw.Draw(shadow)
 prepared=[]
 for word,x,y,size,bold,accent in WORDS:
  f=font(size,bold)
  while s.textbbox((0,0),word,font=f)[2]>930 and size>18:
   size-=1;f=font(size,bold)
  prepared.append((word,x,y,f,accent))
  s.text((x+3,y+3),word,font=f,fill=(0,0,0,220),stroke_width=1,stroke_fill=(0,0,0,140))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.4)))
 d=ImageDraw.Draw(im)
 for word,x,y,f,accent in prepared:
  d.text((x,y),word,font=f,fill=(255,232,163,255) if accent and variant==2 else (255,255,255,255))
 d.line((105,492,568,492),fill=(244,198,158,248),width=3)
 out=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{variant}.jpg'
 png=ASSETS/f'thumbnail-v{variant}.png'
 out.save(jpg,'JPEG',quality=93,optimize=True,subsampling=0)
 out.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:assert check.size==(1200,630)
 print('Generated',jpg.name,jpg.stat().st_size,'bytes')
for n in (1,2):render(n)
for f in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v2.jpg',ASSETS/'thumbnail-v2.png']:
 assert f.is_file() and f.stat().st_size>5000,f
print('Psalms 130:5-7 assets complete')
