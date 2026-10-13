#!/usr/bin/env python3
"""Generate photography and Kakao preview thumbnails for 2026-10-13 daily verse."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import io,urllib.request,shutil
P=Path(__file__).resolve().parent;A=P/'assets';A.mkdir(parents=True,exist_ok=True)
URLS=[
'https://images.unsplash.com/reserve/qw4JvEnzT3iyU1HR9Ed5_DSC02436.jpg?auto=format&fit=crop&w=2300&q=87',
'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2300&q=87',
'https://images.unsplash.com/photo-1663604586581-cb2ae59b6db2?auto=format&fit=crop&w=2300&q=87',
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
    d.rounded_rectangle((58,79,1142,571),radius=40,fill=(3,13,31,220))
    gold=(232,194,112,238)
    d.arc((64,92,136,164),180,270,fill=gold,width=3)
    d.arc((1064,92,1136,164),270,360,fill=gold,width=3)
    d.arc((64,488,136,560),90,180,fill=gold,width=3)
    d.arc((1064,488,1136,560),0,90,fill=gold,width=3)
    for a,b in ((136,373),(827,1064)):d.line((a,92,b,92),fill=gold,width=3)
    for a,b in ((136,407),(793,1064)):d.line((a,560,b,560),fill=gold,width=3)
    d.line((64,164,64,488),fill=gold,width=3)
    d.line((1136,164,1136,488),fill=gold,width=3)
    label='TODAY’S BIBLE VERSE  ·  2026.10.13';f=font(20);bbox=d.textbbox((0,0),label,font=f);tw=bbox[2]-bbox[0]
    d.rounded_rectangle((600-tw/2-24,50,600+tw/2+24,91),radius=20,fill=(225,190,116,244))
    d.text((600,71),label,font=f,anchor='mm',fill=(35,31,25,255))
    lines=([('아버지께서 다른 보혜사를',43,False),('너희에게 보내셔서,',45,False),('영원히 너희와 함께',53,True),('계시게 하실 것이다.',49,True)] if v==1 else [('내가 아버지께 구하겠다.',43,False),('아버지께서 다른 보혜사를 보내셔서,',42,False),('영원히 너희와 함께',55,True),('계시게 하실 것이다.',50,True)])
    ys=(198,279,358,435)
    for (s,size,accent),y in zip(lines,ys):
        f=font(size)
        while d.textbbox((0,0),s,font=f)[2]>1000:size-=1;f=font(size)
        for off,opacity in ((5,90),(3,180),(2,225)):
            d.text((600+off,y+off),s,font=f,anchor='mm',fill=(0,0,0,opacity))
        d.text((600,y),s,font=f,anchor='mm',fill=(255,232,163,255) if accent else (255,255,255,255),stroke_width=1,stroke_fill=(12,14,20,245))
    d.text((600,541),'— 요한복음서 14:16–17 —',font=font(25),fill=(255,232,163,255),anchor='mm')
    rgb=im.convert('RGB')
    rgb.save(A/('thumbnail-v%d.jpg'%v),'JPEG',quality=94,optimize=True,subsampling=0)
    rgb.save(A/('thumbnail-v%d.png'%v),'PNG',optimize=True)
for v in (1,2):render(v)
for file in (P/'bg.jpg',A/'background.jpg',A/'background-v1.jpg',A/'thumbnail-v1.png',A/'thumbnail-v1.jpg',A/'thumbnail-v2.png',A/'thumbnail-v2.jpg'):
    with Image.open(file) as test: print(file.name,test.size,file.stat().st_size)
