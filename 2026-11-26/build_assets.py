#!/usr/bin/env python3
"""Build Bible background and Kakao preview for Psalm 16:8–11."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; ASSETS.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT.parent/'2026-11-25'/'bg.jpg'
if not SOURCE.exists(): raise FileNotFoundError("Previous day's established background missing")
photo=Image.open(SOURCE).convert('RGB')
def cover(im,w,h):
  s=max(w/im.width,h/im.height)
  nw,nh=round(im.width*s),round(im.height*s)
  im=im.resize((nw,nh),Image.Resampling.LANCZOS)
  return im.crop(((nw-w)//2,(nh-h)//2,(nw+w)//2,(nh+h)//2))
base=cover(photo,1920,1080)
base=ImageEnhance.Color(base).enhance(0.93)
base=ImageEnhance.Contrast(base).enhance(1.03)
for target,q in [(ROOT/'bg.jpg',90),(ASSETS/'background.jpg',87),(ASSETS/'background-v1.jpg',84)]:
  base.save(target,'JPEG',quality=q,subsampling=0,optimize=True)
SERIF='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SANS='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(size,serif=True):
  choices=([SERIF,'/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'] if serif else [SANS,'/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'])
  for p in choices:
    if Path(p).exists(): return ImageFont.truetype(p,size)
  raise FileNotFoundError(choices)
def fit(draw,txt,max_size,max_width,serif=True):
  size=max_size
  while size>25 and draw.textbbox((0,0),txt,font=font(size,serif))[2]>max_width: size-=1
  return font(size,serif)
verse_lines=[
  ('주님은 언제나 나와 함께 계시는 분,',False),
  ('그가 나의 오른쪽에 계시니,',False),
  ('나는 흔들리지 않는다.',True),
  ('주님을 모시고 사는 삶에 기쁨이 넘칩니다.',True),
]
for variant in (1,2):
  im=cover(base,1200,630).filter(ImageFilter.GaussianBlur(3.2 if variant==1 else 5.2))
  im=ImageEnhance.Brightness(im).enhance(0.78 if variant==1 else 0.72).convert('RGBA')
  veil=Image.new('RGBA',im.size,(4,12,27,157 if variant==1 else 178))
  im=Image.alpha_composite(im,veil)
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((41,49,1159,581),radius=26,outline=(255,222,157,224),width=3)
  d.rounded_rectangle((330,22,870,81),radius=28,fill=(245,207,137,255),outline=(255,239,199,255),width=2)
  d.text((600,52),"TODAY'S BIBLE VERSE  ·  2026.11.26",font=font(22,False),fill=(21,31,50),anchor='mm')
  ys=[176,265,365,465]
  for i,(line,em) in enumerate(verse_lines):
    f=fit(d,line,55 if em else 48,1020)
    d.text((604,ys[i]+5),line,font=f,anchor='mm',fill=(0,0,0,237),stroke_width=5,stroke_fill=(0,0,0,220))
    d.text((600,ys[i]),line,font=f,anchor='mm',fill=(255,232,163) if em else (255,255,255))
  d.rounded_rectangle((434,561,766,601),radius=18,fill=(6,17,37,255))
  d.text((600,578),'— 시편 16:8–11 —',font=font(27,False),fill=(255,232,163),anchor='mm')
  out=im.convert('RGB')
  out.save(ASSETS/f'thumbnail-v{variant}.jpg','JPEG',quality=93,optimize=True,subsampling=0)
  out.save(ASSETS/f'thumbnail-v{variant}.png','PNG',optimize=True)
for p in (ROOT/'bg.jpg', *ASSETS.iterdir()):
  assert p.exists() and p.stat().st_size>10000,p
  print('OK',p.name,p.stat().st_size)
