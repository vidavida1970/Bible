#!/usr/bin/env python3
"""Create Matthew 5:14-16 village light background and Kakao 1200x630 thumbnails."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import urllib.request, shutil
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
ASSETS.mkdir(exist_ok=True,parents=True)
# Stock image from Unsplash search: warmly illuminated hillside stone village.
SOURCES=[
    'https://images.unsplash.com/photo-1499174549139-68d3f37243b4?auto=format&fit=crop&w=2400&q=88',
    'https://images.unsplash.com/photo-1548115184-bc6544d06a58?auto=format&fit=crop&w=2400&q=88',
    'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=88',
]
def get_photo():
    for i,url in enumerate(SOURCES):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=32) as r: data=r.read()
            im=Image.open(BytesIO(data)).convert('RGB')
            if min(im.size)<600:raise ValueError('low resolution background')
            print('Background photo index',i,'pixels',im.size)
            return im
        except Exception as e:print('Photo source failed',i,str(e)[:175])
    raise RuntimeError('Could not download freely licensed Unsplash photo')
def cover(im,w,h):
    return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.49))
def font(sz,bold=False):
    candidates=[
      '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
      '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    ]
    for name in candidates:
        if Path(name).is_file():return ImageFont.truetype(name,sz)
    raise RuntimeError('Korean font missing: install fonts-noto-cjk')
photo=get_photo()
background=ImageEnhance.Color(cover(photo,1920,1080)).enhance(1.08)
background.save(ROOT/'bg.jpg','JPEG',quality=89,optimize=True,progressive=True)
for name in ('background.jpg','background-v1.jpg'):
    shutil.copyfile(ROOT/'bg.jpg',ASSETS/name)
LINES=[
    ("TODAY'S BIBLE VERSE  ·  2026.10.29",106,106,21,False,False),
    ("너희는 세상의 빛이다",106,182,63,True,False),
    ("너희 빛을 사람에게 비추어라",106,273,52,True,True),
    ("산 위에 세운 마을은 숨길 수 없다",106,389,29,False,False),
    ("착한 행실로 아버지께 영광을 돌리게 하여라",106,434,27,False,False),
    ("마태복음서 5:14–16",106,527,28,False,False),
]
def render(n):
    im=cover(background,1200,630).convert('RGBA')
    dim=Image.new('RGBA',im.size,(0,0,0,0))
    d=ImageDraw.Draw(dim)
    for x in range(1200):
        alpha=round(51+61*(1-x/1199))
        d.line((x,0,x,629),fill=(4,11,27,alpha))
    im=Image.alpha_composite(im,dim)
    panel=Image.new('RGBA',im.size,(0,0,0,0))
    d=ImageDraw.Draw(panel)
    d.rectangle((60,53,1140,578),fill=(5,15,33,188),outline=(231,204,146,229),width=2)
    d.rectangle((60,53,78,578),fill=(218,177,99,240))
    im=Image.alpha_composite(im,panel)
    shadow=Image.new('RGBA',im.size,(0,0,0,0))
    sd=ImageDraw.Draw(shadow)
    prepared=[]
    for s,x,y,sz,bold,accent in LINES:
        f=font(sz,bold)
        while sd.textbbox((0,0),s,font=f)[2]>948 and sz>17:
            sz-=1;f=font(sz,bold)
        width=sd.textbbox((0,0),s,font=f)[2]
        assert x+width<1140,('Text overflow',s,x+width)
        prepared.append((s,x,y,f,accent))
        sd.text((x+3,y+3),s,font=f,fill=(0,0,0,220),stroke_width=1,stroke_fill=(0,0,0,154))
    im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.6)))
    d=ImageDraw.Draw(im)
    for s,x,y,f,accent in prepared:
        d.text((x,y),s,font=f,fill=(255,232,163,255) if accent and n==2 else (255,255,255,255))
    d.line((106,495,568,495),fill=(251,215,162,255),width=3)
    out=im.convert('RGB')
    jpg=ASSETS/f'thumbnail-v{n}.jpg'
    png=ASSETS/f'thumbnail-v{n}.png'
    out.save(jpg,'JPEG',quality=94,optimize=True,subsampling=0)
    out.save(png,'PNG',optimize=True)
    with Image.open(jpg) as check:
        assert check.size==(1200,630)
    print('Saved',jpg.name,jpg.stat().st_size)
for n in (1,2):render(n)
for f in [ROOT/'bg.jpg',ASSETS/'background.jpg',ASSETS/'background-v1.jpg',ASSETS/'thumbnail-v1.png',ASSETS/'thumbnail-v1.jpg',ASSETS/'thumbnail-v2.png',ASSETS/'thumbnail-v2.jpg']:
    assert f.is_file() and f.stat().st_size>5000,f
print('All Matthew 5:14–16 visual assets generated')
