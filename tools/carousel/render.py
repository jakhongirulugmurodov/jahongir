# Panorama SVG (N*1080 x 1350) → N ta 1080x1350 JPG. Foydalanish: python3 render.py <svg> <chiqish_papka>
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import fontroute
from playwright.async_api import async_playwright
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
svg = open(src).read()
import re
W = int(re.search(r'width="(\d+)"', svg).group(1)); N = W // 1080
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); c = await b.new_context(viewport={"width": W, "height": 1350}); await c.route("https://**/*", fontroute.route)
        pg = await c.new_page()
        await pg.set_content('<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{margin:0}</style></head><body>' + svg + "</body></html>")
        await pg.wait_for_timeout(1200); await pg.screenshot(path=os.path.join(out, "pano.png")); await b.close()
asyncio.run(m())
im = Image.open(os.path.join(out, "pano.png")).convert("RGB")
for i in range(N): im.crop((i * 1080, 0, (i + 1) * 1080, 1350)).save(os.path.join(out, f"{i + 1:02d}.jpg"), quality=88)
g = Image.new("RGB", (5 * 432, ((N + 4) // 5) * 540), "white")
for i in range(N): g.paste(im.crop((i * 1080, 0, (i + 1) * 1080, 1350)).resize((432, 540)), ((i % 5) * 432, (i // 5) * 540))
g.save(os.path.join(out, "grid.jpg"), quality=80); os.remove(os.path.join(out, "pano.png"))
print("ok", N)
