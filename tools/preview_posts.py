# Faqat tanlangan postlarni (saytsiz) ko'rsatadigan bitta HTML: storyboard chizilib chiqadi, matn va taklif.
# Foydalanish: python3 tools/preview_posts.py <chiqish.html> <post_id> [post_id ...]
import json, os, sys, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uztypo import typo, typo_markup
from urllib.parse import quote
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
E = lambda s: html.escape(typo(s))
site = json.load(open(os.path.join(R, "content/site.json")))
projs = {p["slug"]: p for p in json.load(open(os.path.join(R, "content/projects/projects.json")))}
OY = ["yanvar","fevral","mart","aprel","may","iyun","iyul","avgust","sentabr","oktabr","noyabr","dekabr"]
def svg(k):
    p = os.path.join(R, "content", k["svg"]); s = open(p).read()
    return re.sub(r"<svg ", '<svg role="img" aria-label="%s" ' % E(k.get("izoh", "")), s, count=1)
cards = []
for pid in sys.argv[2:]:
    p = json.load(open(os.path.join(R, "content/posts", pid + ".json"))); K = p["storyboard"]["kadrlar"]
    y, m, d = p["sana"].split("-"); pr = projs[p["loyiha"]]
    cta = f'https://t.me/{site["telegram"]}?text={quote(typo(p["taklif"]["xabar"]))}'
    frames = "".join(f'<div class="pl-f{" on" if i == 0 else ""}" data-cap="{E(k.get("izoh",""))}">{svg(k)}</div>' for i, k in enumerate(K))
    dots = "".join(f'<button type="button" aria-label="{i+1}-kadr"{" class=on" if i == 0 else ""}></button>' for i in range(len(K)))
    cards.append(f'''<article class="post">
  <p class="meta">{int(d)}-{OY[int(m)-1]}, {y} · {E(pr["nom"])} · {E(p.get("tur",""))}</p>
  <h2>{E(p["sarlavha"])}</h2>
  <div class="player"><div class="stage">{frames}</div>
    <div class="bar"><span class="dots">{dots}</span><span class="cap">{E(K[0].get("izoh",""))}</span><button type="button" class="re" aria-label="Qayta ko‘rish">↻</button></div></div>
  <div class="blocks"><section><h3>Muammo</h3><p>{E(p["muammo"])}</p></section><section><h3>Yechim</h3><p>{E(p["yechim"])}</p></section><section><h3>Natija</h3><p>{E(p["natija"])}</p></section></div>
  <a class="cta" href="{html.escape(cta)}" target="_blank" rel="noopener">{E(p["taklif"]["tugma"])} →</a>
</article>''')
page = f'''<title>Shaxsiy blog postlari</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Hanken+Grotesk:wght@400;500;600&family=Caveat:wght@700&display=swap">
<style>
/* Layout: bitta ustun, har post qog'oz varag'i; storyboard katak qog'oz bo'lib qoladi (ikkala mavzuda ham) */
:root{{--bg:#E9EFEE;--sheet:#FFFFFF;--ink:#17211F;--soft:#55605E;--deep:#0A4E50;--primary:#0E7E80;--line:#C9DCDC;--dot:#16A6A9;
--display:"Space Grotesk",system-ui,sans-serif;--body:"Hanken Grotesk",system-ui,sans-serif;--hand:"Caveat","Comic Sans MS",cursive}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0B1F20;--sheet:#13292A;--ink:#E7F1F0;--soft:#A9BDBB;--deep:#9AD2D2;--primary:#5FC2C3;--line:#2A4647;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0B1F20;--sheet:#13292A;--ink:#E7F1F0;--soft:#A9BDBB;--deep:#9AD2D2;--primary:#5FC2C3;--line:#2A4647;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font:16px/1.6 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 56px}}
.wrap{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:36px}}
.head h1{{font:700 clamp(26px,5vw,36px)/1.1 var(--display);margin:0 0 6px;color:var(--deep);text-wrap:balance}}
.head p{{margin:0;color:var(--soft);max-width:62ch}}
.post{{background:var(--sheet);border-radius:8px;padding:clamp(18px,4vw,34px);box-shadow:0 1px 2px rgba(10,59,60,.08),0 24px 50px -30px rgba(8,69,70,.45);display:flex;flex-direction:column;gap:16px;min-width:0}}
.meta{{margin:0;font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--primary)}}
.post h2{{margin:0;font:700 clamp(21px,3.6vw,28px)/1.18 var(--display);text-wrap:balance}}
.stage{{position:relative;aspect-ratio:4/3;max-width:100%;border:1.6px solid #1E3A39;border-radius:8px;overflow:hidden;background:#FBFBF8}}
.pl-f{{position:absolute;inset:0;opacity:0;transition:opacity .45s ease}}.pl-f.on{{opacity:1}}
.pl-f svg{{display:block;width:100%;height:100%}}
.bar{{display:flex;align-items:center;gap:12px;margin-top:10px}}
.dots{{display:flex;gap:6px}}.dots button{{width:9px;height:9px;padding:0;border:0;border-radius:5px;background:var(--line);cursor:pointer;transition:width .3s,background .3s}}
.dots button.on{{width:24px;background:var(--primary)}}
.cap{{flex:1;min-width:0;font:700 22px/1.1 var(--hand);color:var(--deep)}}
.re{{width:34px;height:34px;border-radius:50%;border:1.6px solid var(--line);background:transparent;color:var(--ink);font-size:17px;cursor:pointer}}
button:focus-visible,.cta:focus-visible{{outline:2px solid var(--dot);outline-offset:2px}}
.blocks{{display:grid;gap:14px}}
.blocks h3{{margin:0 0 2px;font:700 12px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--primary)}}
.blocks p{{margin:0;max-width:65ch}}
.cta{{align-self:flex-start;display:inline-flex;padding:13px 22px;border-radius:999px;background:var(--deep);color:var(--sheet);font:700 16px var(--display);text-decoration:none}}
@media (prefers-reduced-motion: reduce){{.pl-f{{transition:none}}}}
</style>
<div class="wrap">
  <header class="head"><h1>{E(projs[json.load(open(os.path.join(R,"content/posts",sys.argv[2]+".json")))["loyiha"]]["nom"])}: 3 ta post</h1>
  <p>{E("Saytdagi ko'rinishi: storyboard ko'z oldida chiziladi, keyin keyingi kadrga o'tadi. Kadr nuqtalarini bosib almashtirish yoki ↻ bilan qayta ko'rish mumkin.")}</p></header>
  {"".join(cards)}
</div>
<script>
(function(){{var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll(".player").forEach(function(el){{var F=[].slice.call(el.querySelectorAll(".pl-f")),D=el.querySelectorAll(".dots button"),cap=el.querySelector(".cap"),i=0,t=0,vis=true;
function len(f){{var s=f.querySelector("svg");return s?(parseFloat(s.getAttribute("data-len"))||3)*1000+1400:3000}}
function show(n){{clearTimeout(t);F[i].classList.remove("on");D[i].classList.remove("on");i=n;var f=F[i];f.classList.add("on");D[i].classList.add("on");cap.textContent=f.getAttribute("data-cap");
var s=f.querySelector("svg");if(s&&!reduce){{var c=s.cloneNode(true);s.parentNode.replaceChild(c,s)}}if(reduce)return;t=setTimeout(function next(){{if(vis)show((i+1)%F.length);else t=setTimeout(next,800)}},len(f))}}
D.forEach(function(b,n){{b.addEventListener("click",function(){{show(n)}})}});el.querySelector(".re").addEventListener("click",function(){{show(i)}});
if(window.IntersectionObserver)new IntersectionObserver(function(es){{vis=es[0].isIntersecting}},{{threshold:.3}}).observe(el);show(0)}})}})();
</script>'''
open(sys.argv[1], "w").write(typo_markup(page))
print("ok", len(page) // 1024, "KB")
