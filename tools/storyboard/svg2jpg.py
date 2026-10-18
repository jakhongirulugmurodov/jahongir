# Doodle SVG kadrlarini tayyor (to'liq chizilgan) JPG'ga aylantiradi: kartochka, story va muqova uchun.
# Foydalanish: python3 tools/storyboard/svg2jpg.py <svg...>  → yonida .jpg (1200x900)
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); import fontroute
from playwright.async_api import async_playwright
HEAD = '<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{margin:0}svg{width:1200px;height:900px;display:block}</style></head><body>'
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); c = await b.new_context(viewport={"width": 1200, "height": 900}); await c.route("https://**/*", fontroute.route)
        pg = await c.new_page()
        for f in sys.argv[1:]:
            await pg.set_content(HEAD + open(f).read().replace('class="dood"', 'class="dood still"') + "</body></html>")
            await pg.wait_for_timeout(500); await pg.screenshot(path=f[:-4] + ".jpg", type="jpeg", quality=84)
        await b.close()
asyncio.run(m())
