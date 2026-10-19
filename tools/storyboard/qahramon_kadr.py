# Jahongir qahramoni rasmlaridan (content/media/qahramon/*.jpg, Gemini'da generatsiya qilingan) storyboard kadri:
# rasm + doodle uslubidagi lenta sarlavha + raqam. Faqat "Shaxsiy blog tizimi" loyihasi uchun.
# Foydalanish: python3 tools/storyboard/qahramon_kadr.py <rasm> <sarlavha> <raqam> <chiqish.jpg>
import asyncio, base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from doodle import Frame, W, H
import fontroute
from playwright.async_api import async_playwright
from PIL import Image
src, cap, num, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
iw, ih = Image.open(src).size
s = min(W / iw, (H - 120) / ih) if iw / ih > 1.6 else max(W / iw, H / ih)
w, h = iw * s, ih * s; x, y = (W - w) / 2, (H - h) / 2 + (40 if iw / ih > 1.6 else 0)
f = Frame(cap, num)
f.parts.append(f'<image href="data:image/jpeg;base64,{base64.b64encode(open(src, "rb").read()).decode()}" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" preserveAspectRatio="xMidYMid slice"/>')
svg = f.svg().replace('class="dood"', 'class="dood still"')
# lenta va raqamni rasm ustiga chiqarish: ular svg() da rasmdan oldin chiziladi, shuning uchun qayta qo'shamiz
i = svg.find('<g class="f" style="--d:0s">'); j = svg.find('</g>', svg.find('</g>', i) + 4) + 4
ribbon = svg[i:j]; svg = svg.replace('</svg>', ribbon + '</svg>')
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); c = await b.new_context(viewport={"width": W, "height": H}); await c.route("https://**/*", fontroute.route)
        pg = await c.new_page(); await pg.set_content('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{margin:0}svg{display:block;width:1200px;height:900px}</style>' + svg)
        await pg.wait_for_timeout(600); await pg.screenshot(path=out, type="jpeg", quality=86); await b.close()
asyncio.run(m()); print("ok", out)
