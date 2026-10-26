#!/usr/bin/env python3
"""2026-10-26 Colossians 3:15–17: Unsplash calm lake background & 1200x630 Kakao thumbnails."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from io import BytesIO
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';ASSETS.mkdir(parents=True,exist_ok=True)
# Peace and gratitude: tranquil lake with golden morning reflections. Unsplash License.
SOURCES=[
 'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=2400&q=88',
 'https://images.unsplash.com/photo-1505887837284-44dc0a2c058b?auto=format&fit=crop&w=2400&q=88',
 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=88',
]
def download():
 for i,url in enumerate(SOURCES):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as f: data=f.read()
   img=Image.open(BytesIO(data)).convert('RGB')
   if min(img.size)<600:raise ValueError('resolution too low')
   print('Unsplash source',i,'size',img.size)
   return img
  except Exception as e:print('image source error',i,str(e)[:160])
 raise RuntimeError('Could not download any usable background photograph')
def crop(img,w,h):
 return ImageOps.fit(img,(w,h),method=Image.Resampling.LANCZOS,centering=(.50,.50))
def font(sz,bold=False):
 names=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
 ]
 for f in names:
  if Path(f).is_file():return ImageFont.truetype(f,sz)
 raise RuntimeError('Korean font unavailable: install fonts-noto-cjk')
source=download()
bg=ImageEnhance.Color(crop(source,1920,1080)).enhance(1.05)
bg.save(ROOT/'bg.jpg','JPEG',quality=90,optimize=True,progressive=True)
for name in ('background.jpg','background-v1.jpg'):
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/name)
LINES=[
 ("TODAY'S WORD  ·  2026.10.26",105,101,23,False,False),
 ("그리스도의 평화가",105,181,60,True,False),
 ("여러분의 마음을 지배하게 하십시오",105,271,48,True,True),
 ("또 여러분은 감사하는 사람이 되십시오",105,387,29,False,False),
 ("그리스도의 말씀이 풍성히 살아 있게 하십시오",105,432,27,False,False),
 ("골로새서 3:15–17",105,523,28,False,False),
]
def make(version):
 im=crop(bg,1200,630).convert('RGBA')
 dim=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(dim)
 for x in range(1200):
  alpha=round(37+75*(1-x/1199))
  dd.line((x,0,x,629),fill=(5,13,29,alpha))
 im=Image.alpha_composite(im,dim)
 glass=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(glass)
 d.rectangle((60,53,1140,578),fill=(5,19,38,192),outline=(205,213,225,225),width=2)
 d.rectangle((60,53,79,578),fill=(92,164,182,245))
 im=Image.alpha_composite(im,glass)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));s=ImageDraw.Draw(shadow)
 prepared=[]
 for words,x,y,size,bold,accent in LINES:
  face=font(size,bold)
  while s.textbbox((0,0),words,font=face)[2]>941 and size>18:
   size-=1;face=font(size,bold)
  width=s.textbbox((0,0),words,font=face)[2]
  assert x+width<=1138,words
  prepared.append((words,x,y,face,accent))
  s.text((x+3,y+3),words,font=face,fill=(0,0,0,215),stroke_width=1,stroke_fill=(0,0,0,158))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.2)))
 d=ImageDraw.Draw(im)
 for words,x,y,face,accent in prepared:
  d.text((x,y),words,font=face,fill=(255,232,163,255) if accent and version==2 else (255,255,255,255))
 d.line((105,487,572,487),fill=(244,200,159,255),width=3)
 rgb=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{version}.jpg'
 png=ASSETS/f'thumbnail-v{version}.png'
 rgb.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 rgb.save(png,'PNG',optimize=True)
 with Image.open(jpg) as check:assert check.size==(1200,630)
 print(jpg.name,jpg.stat().st_size,'bytes')
for version in (1,2):make(version)
for path in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v2.png',ASSETS/'thumbnail-v2.jpg']:
 assert path.is_file() and path.stat().st_size>5000,path
print('All Colossians 3:15–17 image assets completed')
