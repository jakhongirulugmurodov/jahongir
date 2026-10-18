# Post uchun tik story (1080x1920) HTML'ini tayyorlaydi: og'riq savoli + ikki kadr + taklif.
# Foydalanish: python3 tools/story/make.py spec.json chiqish_papka
# spec: {"nom","sana","kicker","sarlavha","lead","kadrlar":[[rasm, izoh],[rasm, izoh]]}
# Natija: <nom>-tg.html (Telegram: "To'liq o'qish →" tugmasi) va <nom>-ig.html (Instagram: "AI deb yozing").
import json, os, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from uztypo import typo_markup
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
E = html.escape
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Hanken+Grotesk:wght@400;500;600;700&family=Caveat:wght@500;700&display=swap">'
CSS = """*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0A4E50;font-family:'Hanken Grotesk',sans-serif;color:#fff;position:relative}
.g{position:absolute;inset:0;background:radial-gradient(1200px 900px at 85% 10%,rgba(22,166,169,.35),transparent 60%),radial-gradient(900px 700px at 0% 100%,rgba(6,40,41,.7),transparent 60%)}
.top{position:absolute;top:250px;left:90px;right:90px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;font-family:'Space Grotesk';font-weight:700;font-size:44px}
.sep{width:3px;height:44px;background:rgba(255,255,255,.4);margin:0 24px}
.logo{display:inline-flex;align-items:flex-start;font-size:58px;letter-spacing:-.01em;line-height:.9}.logo .lo{position:relative;display:inline-block}.logo .lo::after{content:'';position:absolute;top:.05em;right:.06em;width:.15em;height:.15em;border-radius:50%;background:#16A6A9}.logo .ln{margin-left:.07em}
.date{font-size:30px;font-weight:600;color:#9AD2D2;letter-spacing:.08em;text-transform:uppercase}
.kick{position:absolute;top:400px;left:90px;font-size:30px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#9AD2D2;display:flex;align-items:center;gap:18px}
.kick b{width:16px;height:16px;border-radius:50%;background:#16A6A9}
.col{position:absolute;top:455px;left:0;right:0;display:flex;flex-direction:column}
h1{margin:0 80px 0 86px;font-family:'Space Grotesk';font-weight:700;font-size:80px;line-height:1.03;letter-spacing:-.025em}
.lead{margin:28px 110px 0 90px;font-size:40px;line-height:1.3;color:rgba(255,255,255,.9)}
.area{position:relative;flex:1;margin-top:44px}
.card{position:absolute;width:600px;background:#F5F5F3;padding:16px 16px 0;box-shadow:0 30px 50px -20px rgba(0,0,0,.55)}
.card img{display:block;width:100%}
.card p{font-family:'Caveat';font-weight:700;font-size:40px;color:#17211F;text-align:center;padding:8px 0 12px}
.c1{left:56px;top:0;transform:rotate(-3deg)}.c2{right:56px;bottom:0;transform:rotate(2.5deg)}
.btn{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap}
.pill{background:#fff;color:#0A4E50;font-family:'Space Grotesk';font-weight:700;font-size:50px;padding:34px 70px;border-radius:999px;box-shadow:0 20px 40px -14px rgba(0,0,0,.6)}
.url{position:absolute;top:1765px;left:0;right:0;text-align:center;font-size:30px;color:#9AD2D2;letter-spacing:.04em}"""
def page(mode):
    (a1, t1), (a2, t2) = spec["kadrlar"]
    bottom = 1920 - (1550 if mode == "tg" else 1460)
    if mode == "tg":
        cta = '<a class="btn pill" id="btn" style="top:1580px">To\'liq o\'qish →</a>'
    else:
        cta = ('<div class="btn" id="btn" style="top:1490px;text-align:center"><span style="display:inline-block;background:#fff;color:#0A4E50;font-family:\'Space Grotesk\';'
               'font-weight:700;font-size:64px;padding:14px 40px;border-radius:22px;transform:rotate(-3deg)">AI</span>'
               '<span style="display:block;font-family:\'Caveat\';font-size:56px;margin-top:22px">deb yozing, to\'liq maqolani yuboraman</span></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div class="g"></div>
<div class="top"><div class="brand">Jahongir<span class="sep"></span><span class="logo"><span class="lo">O</span><span class="ln">N</span></span></div><div class="date">{E(spec['sana'])}</div></div>
<p class="kick"><b></b>{E(spec['kicker'])}</p>
<div class="col" style="bottom:{bottom}px"><h1>{E(spec['sarlavha'])}</h1><p class="lead">{E(spec['lead'])}</p>
<div class="area"><div class="card c1"><img src="{os.path.abspath(a1)}"><p>{E(t1)}</p></div>
<div class="card c2"><img src="{os.path.abspath(a2)}"><p>{E(t2)}</p></div></div></div>
<script>(function(){{var A=document.querySelector('.area'),h=A.clientHeight,ch=Math.min(h/1.68,520),w=Math.min(560,(ch-86)/0.726+32);
document.querySelectorAll('.card').forEach(function(c){{c.style.width=w+'px'}});}})()</script>
{cta}<p class="url">jahongir.onagy.app</p></body></html>"""
for m in ("tg", "ig"):
    open(os.path.join(out, f"{spec['nom']}-{m}.html"), "w").write(typo_markup(page(m)))
print("ok", spec["nom"])
