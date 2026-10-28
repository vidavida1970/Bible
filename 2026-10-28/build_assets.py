#!/usr/bin/env python3
"""Build 2026-10-28 Ephesians 6:14-17 background and accessible Kakao 1200x630 thumbnails."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
A=ROOT/'assets'; A.mkdir(parents=True,exist_ok=True)
# First image confirmed in Unsplash 'path forward' visual search; free-to-use under Unsplash License.
SOURCES=[
 'https://images.unsplash.com/photo-1584428177364-f5a2a0a3a9c6?auto=format&fit=crop&w=2500&q=88',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2500&q=88',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2500&q=88',
]
def download():
 for index,url in enumerate(SOURCES):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as response: blob=response.read()
   im=Image.open(BytesIO(blob)).convert('RGB')
   if min(im.size)<650: raise ValueError('image is too small')
   print('Image source index',index,'size',im.size)
   return im
  except Exception as ex:
   print('Image source unavailable',index,str(ex)[:165])
 raise RuntimeError('Could not obtain photographic background')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.51))
def font(size,bold=False):
 paths=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf']
 for path in paths:
  if Path(path).is_file(): return ImageFont.truetype(path,size)
 raise RuntimeError('Install fonts-noto-cjk for reliable Hangul rendering')
photo=download()
bg=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.07)
bg.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for name in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',A/name)
LINES=[
 ("TODAY'S WORD  ·  2026.10.28",106,103,23,False,False),
 ("진리의 허리띠로 허리를 동이고",106,187,54,True,False),
 ("믿음의 방패를 손에 드십시오",106,277,53,True,True),
 ("발에는 평화의 복음을 전할 차비를 하십시오",106,387,29,False,False),
 ("성령의 검 곧 하나님의 말씀을 받으십시오",106,432,29,False,False),
 ("에베소서 6:14–17",106,527,28,False,False),
]
def render(v):
 im=crop(bg,1200,630).convert('RGBA')
 shade=Image.new('RGBA',im.size,(0,0,0,0))
 sd=ImageDraw.Draw(shade)
 for x in range(1200):
  a=round(36+81*(1-x/1199))
  sd.line((x,0,x,629),fill=(5,12,28,a))
 im=Image.alpha_composite(im,shade)
 panel=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(6,18,36,190),outline=(207,217,228,222),width=2)
 d.rectangle((60,53,79,578),fill=(95,160,186,245))
 im=Image.alpha_composite(im,panel)
 sh=Image.new('RGBA',im.size,(0,0,0,0)); s=ImageDraw.Draw(sh)
 items=[]
 for txt,x,y,size,bold,accent in LINES:
  face=font(size,bold)
  while s.textbbox((0,0),txt,font=face)[2]>920 and size>18:
   size-=1;face=font(size,bold)
  w=s.textbbox((0,0),txt,font=face)[2]
  assert x+w < 1135,(txt,x+w)
  items.append((txt,x,y,face,accent))
  s.text((x+3,y+4),txt,font=face,fill=(0,0,0,220),stroke_width=1,stroke_fill=(0,0,0,150))
 im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(im)
 for txt,x,y,face,accent in items:
  d.text((x,y),txt,font=face,fill=(255,232,163,255) if accent and v==2 else (255,255,255,255))
 d.line((106,495,575,495),fill=(243,202,166,255),width=3)
 result=im.convert('RGB')
 jpg=A/f'thumbnail-v{v}.jpg'
 png=A/f'thumbnail-v{v}.png'
 result.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 result.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check: assert check.size==(1200,630)
 print('Kakao',jpg.name,'size',jpg.stat().st_size)
for n in (1,2): render(n)
for path in [ROOT/'bg.jpg',A/'background.jpg',A/'background-v1.jpg',A/'thumbnail-v1.jpg',A/'thumbnail-v1.png',A/'thumbnail-v2.jpg',A/'thumbnail-v2.png']:
 assert path.is_file() and path.stat().st_size>4000,path
print('2026-10-28 Bible verse background and Kakao thumbnails complete')
