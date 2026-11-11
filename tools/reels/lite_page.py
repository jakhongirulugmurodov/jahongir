# "90 Reels" panelining yengil (JS'siz) varianti — eski iPhone Safari ham ochadi.
# Foydalanish (repo ildizidan): python3 tools/reels/panel_data.py /tmp/panel && python3 tools/reels/lite_page.py /tmp/panel /tmp/panel/lite.html
# Natija: bitta statik HTML (ma'lumot ichida). Artifact tool bilan https://claude.ai/artifact/<lite> ga qayta publish qilinadi.
import json, os, sys, html
from datetime import datetime, timedelta, timezone
TZ = timezone(timedelta(hours=5))
d, out = sys.argv[1], sys.argv[2]
R = lambda n: json.load(open(os.path.join(d, n + ".json")))["rows"]
nav, st, tr = R("navbat"), R("statistika"), R("tarix")
s = json.load(open("content/reels-stats.json")) if os.path.exists("content/reels-stats.json") else {}
kor = {x["media_id"]: x for x in st}
chiq = [x for x in nav if x["holat"] == "chiqdi"]
kut = [x for x in nav if x["holat"] == "kutmoqda"]
jami = sum(int(x.get("korish") or 0) for x in st)
obun = s.get("obunachi") or ""
e = lambda t: html.escape(str(t))
def f(n):
    n = int(n or 0)
    return "{:,}".format(n).replace(",", " ")
def vaqt(v):
    try: return datetime.fromisoformat(v).astimezone(TZ).strftime("%d.%m %H:%M")
    except Exception: return v or ""
def nom(fl): return fl.replace(".mp4", "").replace("-video", "")
def badge(x): return ' <span class="tr">trial</span>' if x.get("trial") else ""
# kunlik ko'rish (tarixdagi jami ko'rish farqi), oxirgi 14 kun
kun = [(tr[i]["kun"], max(0, int(tr[i]["korish"] or 0) - int(tr[i - 1]["korish"] or 0))) for i in range(1, len(tr))][-14:]
mx = max([v for _, v in kun] + [1])
bars = "".join('<div class="b"><div class="bv" style="height:%d%%"></div><div class="bl">%s</div></div>' % (max(2, v * 100 // mx), k[8:10]) for k, v in kun)
top = sorted(chiq, key=lambda x: -int(kor.get(x["media_id"], {}).get("korish") or 0))[:5]
def row(x, i=None):
    k = kor.get(x["media_id"], {})
    return "<tr><td>%s%s<div class='sp'>%s</div></td><td class='r'>%s</td><td class='r'>%s</td></tr>" % (
        e(nom(x["fayl"])), badge(x), e(x.get("spiker", "")), f(k.get("korish")), f(k.get("layk")))
oxirgi = list(reversed(chiq))[:8]
keyin = "".join("<tr><td>%s%s<div class='sp'>%s</div></td><td class='r'>%s</td></tr>" % (e(nom(x["fayl"])), badge(x), e(x.get("spiker", "")), vaqt(x["vaqt"])) for x in kut[:6])
xato = [x for x in nav if x["holat"] == "xato"]
LOGO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "on_logo.svg")).read().strip()
now = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
H = """<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>90 Reels Lite</title><style>
:root{--bg:#061312;--p:#0B1E1D;--t:#16A6A9;--l:#9AD2D2;--w:#F2FAFA;--m:#7FA3A3}
*{box-sizing:border-box}body{margin:0;background:#061312;background:var(--bg);color:#F2FAFA;font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%%}
.w{max-width:640px;margin:0 auto;padding:16px}
.hd{display:-webkit-box;display:flex;-webkit-box-align:center;align-items:center;margin:4px 0 18px}.hd svg{width:52px;height:39px;margin-right:12px;flex:none}
.k{font-size:12px;letter-spacing:.14em;color:#9AD2D2;font-weight:700}.h1{font-size:26px;font-weight:800;margin:2px 0 0}
.up{font-size:13px;color:#7FA3A3;margin-top:4px}
.g{overflow:hidden;margin:0 -5px}.c{float:left;width:50%%;padding:5px}.ci{background:#0B1E1D;border:1px solid #123534;border-radius:14px;padding:14px;height:110px}
.n{font-size:30px;font-weight:800;line-height:1.1}.n small{font-size:16px;color:#7FA3A3;font-weight:600}.lb{font-size:14px;color:#9AD2D2;margin-top:4px}
.bar{height:8px;background:#123534;border-radius:4px;margin-top:10px;overflow:hidden}.bar i{display:block;height:8px;background:#16A6A9}
h2{font-size:15px;letter-spacing:.12em;color:#9AD2D2;margin:24px 0 10px;font-weight:700}
.box{background:#0B1E1D;border:1px solid #123534;border-radius:14px;padding:12px}
.bs{height:120px;display:-webkit-box;display:flex;-webkit-box-align:end;align-items:flex-end}.b{-webkit-box-flex:1;flex:1;height:100%%;position:relative;margin:0 2px}
.bv{position:absolute;bottom:18px;left:0;right:0;background:#16A6A9;border-radius:3px 3px 0 0}.b:last-child .bv{background:#9AD2D2}
.bl{position:absolute;bottom:0;left:0;right:0;text-align:center;font-size:11px;color:#7FA3A3}
.bx{position:relative;height:120px}
table{width:100%%;border-collapse:collapse;font-size:16px}td,th{padding:9px 6px;border-bottom:1px solid #123534;vertical-align:top}
th{font-size:12px;color:#7FA3A3;text-align:left;font-weight:600;letter-spacing:.06em}tr:last-child td{border-bottom:0}
.r{text-align:right;white-space:nowrap}.sp{font-size:12px;color:#7FA3A3;margin-top:2px}
.tr{display:inline-block;font-size:11px;font-weight:700;color:#061312;background:#9AD2D2;border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:2px}
.er{color:#FF9A8A;font-size:14px;margin-top:8px}.ft{display:-webkit-box;display:flex;-webkit-box-align:center;align-items:center;margin:28px 0 8px;color:#7FA3A3;font-size:13px}.ft svg{width:30px;height:23px;margin-right:8px}
</style></head><body><div class="w">
<div class="hd">%(logo)s<div><div class="k">O‘SISH NUQTASI · 90 REELS</div><div class="h1">Bir oyda 90 ta reels</div><div class="up">Yangilandi: %(now)s</div></div></div>
<div class="g">
<div class="c"><div class="ci"><div class="n">%(chiq)d<small> / 90</small></div><div class="lb">Chiqdi</div><div class="bar"><i style="width:%(pct)d%%"></i></div></div></div>
<div class="c"><div class="ci"><div class="n">%(obun)s</div><div class="lb">Obunachilar</div></div></div>
<div class="c"><div class="ci"><div class="n">%(jami)s</div><div class="lb">Jami ko‘rish</div></div></div>
<div class="c"><div class="ci"><div class="n">%(kut)d</div><div class="lb">Navbatda (%(trial)d trial)</div></div></div>
</div>%(xato)s
<h2>KUNLIK KO‘RISH · 14 KUN</h2><div class="box"><div class="bs">%(bars)s</div></div>
<h2>ENG KO‘P KO‘RILGAN</h2><div class="box"><table><tr><th>VIDEO</th><th class="r">KO‘RISH</th><th class="r">LAYK</th></tr>%(top)s</table></div>
<h2>OXIRGI CHIQQANLAR</h2><div class="box"><table><tr><th>VIDEO</th><th class="r">KO‘RISH</th><th class="r">LAYK</th></tr>%(oxirgi)s</table></div>
<h2>KEYINGI NAVBAT</h2><div class="box"><table><tr><th>VIDEO</th><th class="r">TAXMINIY VAQT</th></tr>%(keyin)s</table></div>
<div class="ft">%(logo)s<span>O‘N Agency · yengil versiya</span></div>
</div></body></html>""" % dict(logo=LOGO, now=now, chiq=len(chiq), pct=min(100, len(chiq) * 100 // 90), obun=f(obun) if obun != "" else "—", jami=f(jami),
    kut=len(kut), trial=sum(1 for x in kut if x.get("trial")), bars=bars, top="".join(row(x) for x in top), oxirgi="".join(row(x) for x in oxirgi), keyin=keyin,
    xato=('<div class="er">Xato bilan qolgan: ' + ", ".join(e(nom(x["fayl"])) for x in xato) + "</div>") if xato else "")
open(out, "w").write(H)
print("lite:", out, len(H), "bayt")
