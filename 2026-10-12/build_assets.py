#!/usr/bin/env python3
"""Generate photography and Kakao preview thumbnails for 2026-10-12 daily verse."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import io,urllib.request,shutil
P=Path(__file__).resolve().parent;A=P/'assets';A.mkdir(parents=True,exist_ok=True)
URLS=[
'https://images.unsplash.com/photo-1663604586581-cb2ae59b6db2?auto=format&fit=crop&w=2300&q=87',
'https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?auto=format&fit=crop&w=2300&q=87',
]
def photo():
    for url in URLS:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=50) as resp: return Image.open(io.BytesIO(resp.read())).convert('RGB')
        except Exception as e: print('Photo fallback due to',str(e)[:150])
    raise RuntimeError('Unable to download licensed photo')
def crop(im,w,h):
    W,H=im.size;r=max(w/W,h/H)
    im=im.resize((round(W*r),round(H*r)),Image.Resampling.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width+w)//2,(im.height+h)//2))
def font(n):
    paths=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    for name in paths:
        if Path(name).exists():return ImageFont.truetype(name,n)
    raise FileNotFoundError('No Korean font installed')
original=photo()
bg=ImageEnhance.Color(crop(original,1920,1080)).enhance(.95)
bg.save(P/'bg.jpg','JPEG',quality=90,optimize=True,progressive=True)
for p in ('background.jpg','background-v1.jpg'):shutil.copyfile(P/'bg.jpg',A/p)
def render(v):
    W,H=1200,630
    im=crop(original,W,H).convert('RGBA')
    im=Image.alpha_composite(im,Image.new('RGBA',(W,H),(3,10,24,112)))
    overlay=Image.new('RGBA',(W,H),(0,0,0,0))
    overlay_draw=ImageDraw.Draw(overlay)
    for y in range(H):
        alpha=round(85+55*abs(y-H/2)/(H/2))
        overlay_draw.line((0,y,W,y),fill=(3,8,20,alpha))
    im=Image.alpha_composite(im,overlay)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((58,79,1142,571),radius=40,fill=(3,13,31,172))
    gold=(232,194,112,238)
    for start,end in ((180,263),(277,360),(0,75),(105,180)):
        d.arc((49,70,1151,579),start,end,fill=gold,width=3)
    for start,end,y in ((95,394,70),(806,1105,70),(95,446,579),(754,1105,579)):
        d.line((start,y,end,y),fill=gold,width=3)
    label='TODAY’S BIBLE VERSE  ·  2026.10.12';f=font(20);bbox=d.textbbox((0,0),label,font=f);tw=bbox[2]-bbox[0]
    d.rounded_rectangle((600-tw/2-24,50,600+tw/2+24,91),radius=20,fill=(225,190,116,244))
    d.text((600,71),label,font=f,anchor='mm',fill=(35,31,25,255))
    lines=[('내 안에 머물러 있어라.',44,False),('그리하면 나도 너희 안에 머물러 있겠다.',40,False),('나는 포도나무요, 너희는 가지이다.',48,True),('너희는 나를 떠나서는 아무것도 할 수 없다.',37,False)]
    ys=(191,266,342,418) if v==1 else (191,264,342,424)
    for (s,size,accent),y in zip(lines,ys):
        f=font(size)
        while d.textbbox((0,0),s,font=f)[2]>1000:size-=1;f=font(size)
        for off,opacity in ((5,90),(3,180),(2,225)):
            d.text((600+off,y+off),s,font=f,anchor='mm',fill=(0,0,0,opacity))
        d.text((600,y),s,font=f,anchor='mm',fill=(255,232,163,255) if accent else (255,255,255,255),stroke_width=1,stroke_fill=(12,14,20,245))
    d.text((600,541),'— 요한복음서 15:4–5 —',font=font(25),fill=(255,232,163,255),anchor='mm')
    rgb=im.convert('RGB')
    rgb.save(A/('thumbnail-v%d.jpg'%v),'JPEG',quality=94,optimize=True,subsampling=0)
    rgb.save(A/('thumbnail-v%d.png'%v),'PNG',optimize=True)
for v in (1,2):render(v)
for file in (P/'bg.jpg',A/'background.jpg',A/'background-v1.jpg',A/'thumbnail-v1.png',A/'thumbnail-v1.jpg',A/'thumbnail-v2.png',A/'thumbnail-v2.jpg'):
    with Image.open(file) as test: print(file.name,test.size,file.stat().st_size)
