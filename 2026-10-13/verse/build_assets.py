#!/usr/bin/env python3
"""10/13 share thumbnail: replicate 2026-10-10 left-aligned word/title/subtitle/source hierarchy.
Existing sunrise/dove bg.jpg remains untouched; only Kakao image files are refreshed.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(exist_ok=True,parents=True)
BACKGROUND=ROOT/'bg.jpg'
if not BACKGROUND.exists():
    raise FileNotFoundError('Original background bg.jpg must be preserved')

REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
if not Path(REG).exists():REG='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
if not Path(BOLD).exists():BOLD='/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'
def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else REG,size)

def fit(im,w=1200,h=630):
    iw,ih=im.size
    rate=max(w/iw,h/ih)
    im=im.resize((int(iw*rate+.5),int(ih*rate+.5)),Image.Resampling.LANCZOS)
    left=(im.width-w)//2
    top=int((im.height-h)*.35)
    return im.crop((left,top,left+w,top+h))

def make(variant):
    img=fit(Image.open(BACKGROUND).convert('RGB')).convert('RGBA')
    W,H=img.size
    img=Image.alpha_composite(img,Image.new('RGBA',(W,H),(5,13,28,48)))
    panel=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(panel)
    d.rectangle((60,53,1140,578),fill=(12,19,39,178),outline=(162,173,192,225),width=2)
    d.rectangle((60,53,76,578),fill=(100,161,191,242))
    grad=Image.new('RGBA',(1080,524))
    gd=ImageDraw.Draw(grad)
    for xx in range(1080):
        alpha=round(55*(1-xx/1080)**1.4)
        gd.line((xx,0,xx,523),fill=(4,11,32,alpha),width=1)
    panel.alpha_composite(grad,(60,53))
    img=Image.alpha_composite(img,panel)
    shadow=Image.new('RGBA',img.size)
    sd=ImageDraw.Draw(shadow)
    texts=[
        ("TODAY'S WORD · 2026.10.13",(105,90),24,False,(255,255,255,245)),
        ('영원히 함께하시는',(105,157),55,True,(255,255,255,255)),
        ('진리의 영',(105,228),60,True,(255,255,255,255) if variant==1 else (255,233,185,255)),
        ('너희와 함께 계시고',(105,327),30,False,(255,255,255,250)),
        ('너희 안에 계실 것이다',(105,373),30,False,(255,255,255,250)),
        ('요한복음서 14:16–17',(105,481),27,False,(255,255,255,250)),
    ]
    for content,xy,size,bold,color in texts:
        f=font(size,bold)
        while sd.textbbox((0,0),content,font=f)[2]>690:
            size-=1
            f=font(size,bold)
        sd.text((xy[0]+2,xy[1]+3),content,font=f,fill=(0,0,0,190),stroke_width=1,stroke_fill=(0,0,0,155))
    img=Image.alpha_composite(img,shadow.filter(ImageFilter.GaussianBlur(3)))
    d=ImageDraw.Draw(img)
    for content,xy,size,bold,color in texts:
        f=font(size,bold)
        while d.textbbox((0,0),content,font=f)[2]>690:
            size-=1
            f=font(size,bold)
        d.text(xy,content,font=f,fill=color)
    d.line([(105,453),(431,453)],fill=(230,178,152,248),width=3)
    rgb=img.convert('RGB')
    jpg=ASSETS/f'thumbnail-v{variant}.jpg'
    png=ASSETS/f'thumbnail-v{variant}.png'
    rgb.save(jpg,'JPEG',quality=92,optimize=True,progressive=True,subsampling=0)
    rgb.save(png,'PNG',optimize=True)
    with Image.open(jpg) as check:
        assert check.size==(1200,630)
    print(str(jpg),jpg.stat().st_size)

for variant in (1,2):make(variant)
