import asyncio,sys,json
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..')); import fontroute
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={"width":1080,"height":1920}); await c.route('https://**/*',fontroute.route)
        pg=await c.new_page(); await pg.goto("file://"+__import__('os').path.abspath(sys.argv[1])); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=sys.argv[2],type="jpeg",quality=90)
        r=await pg.eval_on_selector("#btn","e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]}")
        print(json.dumps(r)); await b.close()
asyncio.run(m())
