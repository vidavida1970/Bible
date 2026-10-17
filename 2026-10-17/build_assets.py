#!/usr/bin/env python3
"""2026-10-17 Jeremiah 17:7-8: create bright green riverside tree background and Kakao thumbnails."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter,ImageOps
from io import BytesIO
import urllib.request,shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';ASSETS.mkdir(parents=True,exist_ok=True)
PHOTOS=[
 ('https://images.unsplash.com/photo-1695098449022-cdf33144a727?auto=format&fit=crop&w=2560&q=90',True),
 ('https://images.unsplash.com/photo-1702314586007-3d499115e855?auto=format&fit=crop&w=2560&q=90',False),
 ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2560&q=90',False),
]
def load():
 for i,(url,mirror) in enumerate(PHOTOS):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as response:
    data=response.read()
   im=Image.open(BytesIO(data)).convert('RGB')
   if min(im.size)<600:raise RuntimeError('Source smaller than 600 pixels')
   print('Source photo:',i,'size:',im.size)
   return ImageOps.mirror(im) if mirror else im
  except Exception as exc:
   print('Unavailable image source',i,':',str(exc)[:160])
 raise RuntimeError('No background image source was reachable')
def crop(im,w,h):
 iw,ih=im.size;ratio=max(w/iw,h/ih)
 im=im.resize((round(iw*ratio),round(ih*ratio)),Image.Resampling.LANCZOS)
 return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width+w)//2,(im.height+h)//2))
def font(sz,bold=False):
 paths=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf']
 for path in paths:
  if Path(path).exists():return ImageFont.truetype(path,sz)
 raise RuntimeError('fonts-noto-cjk is required to render Hangul')
photo=load()
background=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.05)
background.save(ROOT/'bg.jpg','JPEG',quality=91,optimize=True,progressive=True)
for dest in ['background.jpg','background-v1.jpg']:
 shutil.copyfile(ROOT/'bg.jpg',ASSETS/dest)
LINES=[
 ("TODAY'S WORD  ·  2026.10.17",105,99,23,False,False),
 ("주님을 의지하는 사람",105,170,56,True,False),
 ("물가에 심은 나무",105,256,60,True,True),
 ("무더위와 가뭄에도",105,368,30,False,False),
 ("언제나 푸르고 열매를 맺는다",105,411,29,False,False),
 ("예레미야서 17:7–8",105,517,27,False,False)]
def render(v):
 im=crop(photo,1200,630).convert('RGBA')
 scrim=Image.new('RGBA',im.size,(0,0,0,0));s=ImageDraw.Draw(scrim)
 for x in range(1200):
  alpha=round(32+76*(1-x/1199))
  s.line((x,0,x,629),fill=(3,17,24,alpha))
 im=Image.alpha_composite(im,scrim)
 panel=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(panel)
 d.rectangle((60,53,1140,578),fill=(4,22,30,178),outline=(192,214,221,216),width=2)
 d.rectangle((60,53,79,578),fill=(92,176,179,240))
 im=Image.alpha_composite(im,panel)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));sd=ImageDraw.Draw(shadow)
 measured=[]
 for text,x,y,size,bold,accent in LINES:
  f=font(size,bold)
  while sd.textbbox((0,0),text,font=f)[2]>860 and size>18:
   size-=1;f=font(size,bold)
  measured.append((text,x,y,f,accent))
  sd.text((x+3,y+4),text,font=f,fill=(0,0,0,210),stroke_width=1,stroke_fill=(0,0,0,160))
 im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.5)))
 d=ImageDraw.Draw(im)
 for text,x,y,f,accent in measured:
  d.text((x,y),text,font=f,fill=(255,232,163,255) if accent and v==2 else (255,255,255,255))
 d.line((105,487,558,487),fill=(238,205,158,245),width=3)
 out=im.convert('RGB')
 jpg=ASSETS/f'thumbnail-v{v}.jpg';png=ASSETS/f'thumbnail-v{v}.png'
 out.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
 out.save(png,'PNG',optimize=True)
 with Image.open(jpg) as ver:assert ver.size==(1200,630)
 print('Written',jpg.name,jpg.stat().st_size,'bytes')
for v in (1,2):render(v)
for path in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v2.png',ASSETS/'thumbnail-v2.jpg']:
 assert path.exists() and path.stat().st_size>4000,path
print('Jeremiah 17:7-8 backgrounds and Kakao cards generated successfully')
