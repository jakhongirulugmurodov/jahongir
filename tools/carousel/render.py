import asyncio,sys
sys.path.insert(0,'/home/claude/jahongir/tools'); import fontroute
from playwright.async_api import async_playwright
from PIL import Image
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={"width":10800,"height":1350}); await c.route('https://**/*',fontroute.route)
        pg=await c.new_page(); svg=open('/tmp/car/konveyer.svg').read()
        await pg.set_content('<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{margin:0}</style></head><body>'+svg+'</body></html>')
        await pg.wait_for_timeout(1200); await pg.screenshot(path='/tmp/car/pano.png'); await b.close()
asyncio.run(m())
im=Image.open('/tmp/car/pano.png').convert('RGB')
for i in range(10): im.crop((i*1080,0,(i+1)*1080,1350)).save(f'/tmp/car/s{i+1:02d}.jpg',quality=88)
c=Image.new('RGB',(5*432,2*540),'white')
for i in range(10): c.paste(im.crop((i*1080,0,(i+1)*1080,1350)).resize((432,540)),((i%5)*432,(i//5)*540))
c.save('/tmp/car/grid.jpg',quality=80)
