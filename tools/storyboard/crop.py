import asyncio,sys
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..')); import fontroute
from playwright.async_api import async_playwright
from PIL import Image
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={"width":1800,"height":int(sys.argv[3]) if len(sys.argv)>3 else 1160},device_scale_factor=2); await c.route('https://**/*',fontroute.route)
        pg=await c.new_page(); await pg.goto("file://"+__import__('os').path.abspath(sys.argv[1])); await pg.wait_for_timeout(1200)
        await pg.screenshot(path="/tmp/sb-big.png"); await b.close()
asyncio.run(m())
im=Image.open("/tmp/sb-big.png").convert("RGB")
im.resize((1600,round(im.height*1600/im.width)),Image.LANCZOS).save(sys.argv[2]+".jpg",quality=84,optimize=True,progressive=True)
PW,PH,GX,TOP=560,470,30,110
for i in range(int(sys.argv[4]) if len(sys.argv)>4 else 6):
    cx,r=i%3,i//3; x=GX+cx*(PW+30); y=TOP+r*(PH+40)
    im.crop(((x-12)*2,(y-12)*2,(x+PW+12)*2,(y+PH-70+12)*2)).save(sys.argv[2]+f"-{i+1}.jpg",quality=84,optimize=True,progressive=True)
print("ok")
