#!/usr/bin/env python3
"""2026-10-25 Colossians 2:6-7: rooted in Christ, grateful faith / 1200x630 Kakao images."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
# Web-selected open-license Unsplash images; streamside roots, sunlit forest and green hills.
SOURCES=[
 'https://images.unsplash.com/photo-1695098449022-cdf33144a727?auto=format&fit=crop&w=2400&q=90',
 'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=2400&q=90',
 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=90'
]
def download():
 for i,url in enumerate(SOURCES):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as f:
    data=f.read()
   im=Image.open(BytesIO(data)).convert('RGB')
   if min(im.size)<640:raise RuntimeError('Image resolution too low')
   print('Photo source index:',i,'photo size:',im.size)
   return im
  except Exception as e:print('Photo fallback:',i,str(e)[:140])
 raise RuntimeError('None of the background photos could be downloaded')
def crop(im,w,h):
 return ImageOps.fit(im,(w,h),Image.Resampling.LANCZOS,centering=(.52,.49))
def font(sz,bold=False):
 paths=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
 ]
 for f in paths:
  if Path(f).is_file():return ImageFont.truetype(f,sz)
 raise FileNotFoundError('Korean fonts required: fonts-noto-cjk')
photo=download()
bg=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.07)
bg.save(ROOT/'bg.jpg','JPEG',quality=92,optimize=True,progressive=True)
for f in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/f)
TEXT=[
 ("TODAY'S WORD  ·  2026.10.25",106,103,22,False,False),
 ("그분 안에 뿌리를 박고",106,181,58,True,False),
 ("믿음을 굳게 하십시오",106,267,57,True,True),
 ("그분 안에서 살아가십시오",106,382,31,False,False),
 ("감사의 마음이 넘치게 하십시오",106,427,29,False,False),
 ("골로새서 2:6–7",106,526,28,False,False)
]
def render(v):
 im=crop(bg,1200,630).convert('RGBA')
 dark=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(dark)
 for x in range(1200):
  alpha=round(36+80*(1-x/1199))
  d.line((x,0,x,629),fill=(3,13,29,alpha))
 im=Image.alpha_composite(im,dark)
 panel=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(4,19,37,187),outline=(200,216,224,231),width=2)
 d.rectangle((60,53,79,578),fill=(90,170,164,244))
 im=Image.alpha_composite(im,panel)
 shadows=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(shadows)
 labels=[]
 for text,x,y,size,bold,highlight in TEXT:
  face=font(size,bold)
  while d.textbbox((0,0),text,font=face)[2]>925 and size>18:
   size-=1;face=font(size,bold)
  labels.append((text,x,y,face,highlight))
  d.text((x+3,y+4),text,font=face,fill=(0,0,0,225),stroke_width=1,stroke_fill=(0,0,0,160))
 im=Image.alpha_composite(im,shadows.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(im)
 for text,x,y,face,highlight in labels:
  color=(255,232,163,255) if highlight and v==2 else (255,255,255,255)
  d.text((x,y),text,font=face,fill=color)
 d.line((106,490,577,490),fill=(244,203,161,255),width=3)
 result=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg'
 png=ASSETS/f'thumbnail-v{v}.png'
 result.save(jpg,'JPEG',quality=93,optimize=True,subsampling=0)
 result.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:
  assert check.size==(1200,630)
 print('Saved',jpg.name,jpg.stat().st_size)
for i in (1,2):render(i)
for f in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v2.jpg',ASSETS/'thumbnail-v2.png']:
 assert f.is_file() and f.stat().st_size>5000,f
print('Completed Colossians 2:6–7 Bible background and thumbnails')
