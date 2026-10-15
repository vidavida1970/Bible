#!/usr/bin/env python3
"""2026-10-15 Isaiah 46:3-4 page: create photo background & two Kakao previews."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter
from io import BytesIO
import urllib.request, shutil
P=Path(__file__).resolve().parent; A=P/'assets'; A.mkdir(exist_ok=True,parents=True)
# Photo by Ingmar, free to use under Unsplash License
SOURCES=[
'https://images.unsplash.com/photo-1760479099643-b37a52e7c094?auto=format&fit=crop&w=2300&q=88',
'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2300&q=88',
'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2300&q=88',
]
def fetch():
    for i,url in enumerate(SOURCES):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; BibleCardBot/1.0)'})
            with urllib.request.urlopen(request,timeout=35) as f:
                b=f.read()
            image=Image.open(BytesIO(b)).convert('RGB')
            if min(image.size) < 600: raise RuntimeError('Image resolution too small')
            print('Background photo source index:',i,'source dimensions:',image.size)
            return image
        except Exception as exc:
            print('Photo source failed:',i,str(exc)[:200])
    raise RuntimeError('No royalty-free background photo could be downloaded')
def crop(image,w,h):
    iw,ih=image.size
    factor=max(w/iw,h/ih)
    image=image.resize((round(iw*factor),round(ih*factor)),Image.Resampling.LANCZOS)
    return image.crop(((image.width-w)//2,(image.height-h)//2,(image.width+w)//2,(image.height+h)//2))
def font(size,bold=False):
    files=[
      '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
      '/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    ]
    for f in files:
        if Path(f).exists(): return ImageFont.truetype(f,size)
    raise RuntimeError('Required Korean fonts missing')
photo=fetch()
bg=ImageEnhance.Color(crop(photo,1920,1080)).enhance(1.05)
bg.save(P/'bg.jpg','JPEG',quality=90,optimize=True)
shutil.copyfile(P/'bg.jpg',A/'background.jpg')
shutil.copyfile(P/'bg.jpg',A/'background-v1.jpg')
def make_thumbnail(v):
    im=crop(photo,1200,630).convert('RGBA')
    overlay=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(overlay)
    for x in range(1200):
        shade=round(34+64*(1-x/1199))
        d.line([(x,0),(x,629)],fill=(5,12,31,shade))
    im=Image.alpha_composite(im,overlay)
    panel=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(panel)
    d.rectangle((60,53,1140,578),fill=(6,16,36,181),outline=(189,203,219,222),width=2)
    d.rectangle((60,53,78,578),fill=(93,160,189,248))
    im=Image.alpha_composite(im,panel)
    words=[
      ("TODAY'S WORD  ·  2026.10.15",105,100,23,False,False),
      ("태어날 때부터",105,174,60,True,False),
      ("백발이 될 때까지",105,252,62,True,True),
      ("내가 너희를 안고 다니고",105,362,30,False,False),
      ("또 구원하여 주겠다",105,410,30,False,False),
      ("이사야 46:3–4",105,515,28,False,False),
    ]
    cache=[]
    shadow=Image.new('RGBA',im.size,(0,0,0,0));ds=ImageDraw.Draw(shadow)
    for s,x,y,size,bold,gold in words:
        f=font(size,bold)
        while ds.textbbox((0,0),s,font=f)[2]>810 and size>17:
            size-=1;f=font(size,bold)
        cache.append((s,x,y,f,bold,gold))
        ds.text((x+3,y+4),s,font=f,fill=(0,0,0,215),stroke_width=1,stroke_fill=(0,0,0,170))
    im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(2.5)))
    d=ImageDraw.Draw(im)
    for s,x,y,f,bold,gold in cache:
        color=(255,232,163,255) if (gold and v==2) else (255,255,255,255)
        d.text((x,y),s,font=f,fill=color)
    d.line((105,480,537,480),fill=(238,194,159,255),width=3)
    out=im.convert('RGB')
    out.save(A/f'thumbnail-v{v}.jpg','JPEG',quality=93,optimize=True,subsampling=0)
    out.save(A/f'thumbnail-v{v}.png','PNG',optimize=True)
    with Image.open(A/f'thumbnail-v{v}.jpg') as check:
        assert check.size==(1200,630)
    print(f'Thumbnail {v}: {(A/f"thumbnail-v{v}.jpg").stat().st_size} bytes')
for version in (1,2):make_thumbnail(version)
for file in [P/'bg.jpg',A/'background.jpg',A/'background-v1.jpg',A/'thumbnail-v1.png',A/'thumbnail-v1.jpg',A/'thumbnail-v2.png',A/'thumbnail-v2.jpg']:
    assert file.exists() and file.stat().st_size>2000,file
print('Completed all 2026-10-15 Bible image assets')
