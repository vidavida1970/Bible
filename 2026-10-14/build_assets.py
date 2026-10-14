#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import urllib.request,shutil
P=Path(__file__).resolve().parent; A=P/'assets'; A.mkdir(exist_ok=True,parents=True)
URLS=['https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=2400&q=90','https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=90','https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2400&q=90']
def source():
    for url in URLS:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=38) as r:
                im=Image.open(BytesIO(r.read())).convert('RGB')
                if min(im.size)>500:return im
        except Exception as e:print('Photo URL failed:',str(e)[:140])
    im=Image.new('RGB',(1920,1080));d=ImageDraw.Draw(im)
    for y in range(1080):
        t=y/1080
        d.line((0,y,1920,y),fill=(int(32+113*t),int(57+91*t),int(113-31*t)))
    return im
def crop(im,w,h):
    iw,ih=im.size;scale=max(w/iw,h/ih)
    im=im.resize((round(iw*scale),round(ih*scale)),Image.Resampling.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width+w)//2,(im.height+h)//2))
def font(size,bold=False):
    paths=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    for path in paths:
        if Path(path).exists():return ImageFont.truetype(path,size)
    raise FileNotFoundError('Install fonts-noto-cjk')
img=source()
bg=ImageEnhance.Color(crop(img,1920,1080)).enhance(1.08)
bg.save(P/'bg.jpg','JPEG',quality=89,optimize=True)
shutil.copyfile(P/'bg.jpg',A/'background.jpg')
shutil.copyfile(P/'bg.jpg',A/'background-v1.jpg')
lines=[("TODAY'S WORD  ·  2026.10.14",104,96,22,False,False),('주님을 아는 지혜',104,174,57,True,False),('긍휼과 공평과 공의',104,260,59,True,True),('이것을 자랑하여라',104,361,30,False,False),('주께서 기뻐하시는 것',104,408,30,False,False),('예레미야 9:24',104,520,26,False,False)]
def render(variant):
    im=crop(img,1200,630).convert('RGBA')
    dark=Image.new('RGBA',im.size);dd=ImageDraw.Draw(dark)
    for x in range(1200):dd.line((x,0,x,630),fill=(4,10,27,int(68+60*(1-x/1200))))
    im=Image.alpha_composite(im,dark)
    panel=Image.new('RGBA',im.size);d=ImageDraw.Draw(panel)
    d.rectangle((60,52,1140,578),fill=(10,21,43,160),outline=(200,208,221,204),width=2)
    d.rectangle((60,52,78,578),fill=(92,157,188,238))
    for x in range(79,800):d.line((x,54,x,577),fill=(9,18,40,round(60*(1-(x-79)/721))))
    im=Image.alpha_composite(im,panel)
    layer=Image.new('RGBA',im.size);ld=ImageDraw.Draw(layer)
    cached=[]
    for txt,x,y,size,bold,gold in lines:
        f=font(size,bold)
        while ld.textbbox((0,0),txt,font=f)[2]>755:size-=1;f=font(size,bold)
        cached.append((txt,x,y,f,bold,gold))
        ld.text((x+3,y+3),txt,font=f,fill=(0,0,0,235),stroke_width=1,stroke_fill=(0,0,0,160))
    im=Image.alpha_composite(im,layer.filter(ImageFilter.GaussianBlur(2.4)))
    d=ImageDraw.Draw(im)
    for txt,x,y,f,bold,gold in cached:
        d.text((x,y),txt,font=f,fill=(255,232,163,255) if gold and variant==2 else (255,255,255,255))
    d.line(((104,485),(530,485)),fill=(253,201,164,240),width=3)
    result=im.convert('RGB')
    result.save(A/('thumbnail-v%d.jpg'%variant),'JPEG',quality=93,optimize=True,subsampling=0)
    result.save(A/('thumbnail-v%d.png'%variant),'PNG',optimize=True)
    with Image.open(A/('thumbnail-v%d.jpg'%variant)) as c:
        assert c.size==(1200,630)
    print('thumbnail-v%d.jpg'%variant,(A/('thumbnail-v%d.jpg'%variant)).stat().st_size)
for variant in (1,2):render(variant)
print('All Bible image assets created')
