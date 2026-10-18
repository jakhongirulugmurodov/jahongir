# "AI sotuvchi" loyihasi karusellari (10 slayd, 1080x1350). Uslub: nuqtali fon, qo'pol ramkali oq kadr,
# oq boshli odamchalar, robot-agent, teal raqam doirasi, Caveat izohlar (loyiha storyboardlari bilan bir xil).
# Foydalanish: python3 ai_karusel.py <post: guruh|instagram|oqitish> <chiqish.svg>
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storyboard"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sblib import person, bubble, INK, T as TL, SOFT, DEEP, P
from uztypo import typo_markup
SW, SH = 1080, 1350; FX, FY, FW, FH = 70, 560, 940, 640
LIGHT = "#E9F7F7"; GREYT = "#9AA8A6"
def tx(x, y, s, size=40, color=INK, font="Caveat", anchor="start", weight=700):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{s}</text>'
def robot(x, y, s=1, face="ok"):
    m = '<path d="M34 64 q16 10 32 0" stroke="#17211F" stroke-width="4" fill="none" stroke-linecap="round"/>' if face == "ok" else '<path d="M34 66 h32" stroke="#17211F" stroke-width="4" stroke-linecap="round"/>'
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M50 0 v-18" stroke="{INK}" stroke-width="4"/><circle cx="50" cy="-22" r="7" fill="{TL}" stroke="{INK}" stroke-width="3"/>'
            f'<rect width="100" height="86" rx="20" fill="{SOFT}" stroke="{INK}" stroke-width="4"/><circle cx="34" cy="40" r="9" fill="{INK}"/><circle cx="66" cy="40" r="9" fill="{INK}"/>{m}'
            f'<rect x="20" y="90" width="60" height="70" rx="12" fill="{SOFT}" stroke="{INK}" stroke-width="4"/></g>')
def chat(x, y, w, n, hi=None, title="Telegram guruh", hit="SMM kerak! narxi qancha?"):
    h = 70 + n * 38
    o = f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/><rect width="{w}" height="54" rx="16" fill="{DEEP}"/><rect y="30" width="{w}" height="24" fill="{DEEP}"/>{tx(w/2, 36, title, 24, "#fff", "Space Grotesk", "middle")}'
    for i in range(n):
        ww = (w - 60) - (i * 53 % 120); yy = 72 + i * 38
        if i == hi: o += f'<rect x="20" y="{yy-4}" width="{w-40}" height="34" rx="17" fill="#fff" stroke="{TL}" stroke-width="4"/>' + tx(40, yy + 21, hit, 27, DEEP)
        else: o += f'<rect x="{20 + (i % 2) * 40}" y="{yy}" width="{ww}" height="24" rx="12" fill="{"#fff" if i % 3 else SOFT}" stroke="{INK}" stroke-width="2.5"/>'
    return o + "</g>"
def clock(cx, cy, r, hh=0, mm=0, label=None):
    import math
    ha = math.radians((hh % 12 + mm / 60) * 30 - 90); ma = math.radians(mm * 6 - 90)
    o = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M{cx} {cy} L{cx + math.cos(ha) * r * .5:.1f} {cy + math.sin(ha) * r * .5:.1f} M{cx} {cy} L{cx + math.cos(ma) * r * .75:.1f} {cy + math.sin(ma) * r * .75:.1f}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="8" fill="{TL}"/>')
    if label: o += tx(cx, cy + r + 50, label, 40, P, anchor="middle")
    return o
def stack(x, y, n, w=150):
    return "".join(f'<rect x="{x + (k % 2) * 5}" y="{y - k * 15}" width="{w}" height="19" rx="3" fill="{"#fff" if k % 3 else SOFT}" stroke="{INK}" stroke-width="3"/>' for k in range(n))
def card(x, y, w, h, l1, l2=None, fill="#fff"):
    o = f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{INK}" stroke-width="4"/>{tx(24, 46, l1, 28, INK, "Space Grotesk")}'
    if l2: o += tx(24, 86, l2, 30, P)
    return o + "</g>"
def funnel(x, y):
    return (f'<g transform="translate({x},{y})"><rect x="30" y="0" width="190" height="24" rx="12" fill="#fff" stroke="{INK}" stroke-width="2.5"/><rect x="50" y="34" width="150" height="24" rx="12" fill="{SOFT}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M0 80 h250 l-90 110 v110 l-70 34 v-144z" fill="{LIGHT}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>')
def ig_icon(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><rect width="110" height="110" rx="30" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="55" cy="55" r="24" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="84" cy="26" r="6" fill="{TL}"/></g>'
def tg_icon(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><circle cx="55" cy="55" r="55" fill="{SOFT}" stroke="{INK}" stroke-width="5"/><path d="M26 58 L84 34 L74 84 L52 66 Z M52 66 L58 82" fill="#fff" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/></g>'
def igpost(x, y, comment="narxi qancha?", s=1):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect width="300" height="380" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/><rect x="18" y="18" width="264" height="200" rx="10" fill="{SOFT}"/>'
            f'<circle cx="40" cy="250" r="14" fill="{LIGHT}" stroke="{INK}" stroke-width="3"/><path d="M64 250 h120" stroke="{SOFT}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="18" y="286" width="264" height="44" rx="22" fill="#fff" stroke="{TL}" stroke-width="4"/>{tx(38, 316, comment, 28, DEEP)}<path d="M30 356 h150" stroke="{SOFT}" stroke-width="6" stroke-linecap="round"/></g>')
def timer(cx, cy, label, hot=False):
    c = "#C4553E" if hot else TL
    return (f'<g><circle cx="{cx}" cy="{cy}" r="62" fill="#fff" stroke="{INK}" stroke-width="5"/><rect x="{cx-14}" y="{cy-86}" width="28" height="16" rx="4" fill="{INK}"/>'
            f'<path d="M{cx} {cy-62} A62 62 0 0 1 {cx+54} {cy+30}" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round"/>{tx(cx, cy+12, label, 34, INK, "Space Grotesk", "middle")}</g>')
def mark(x, y, ok=True, s=1):
    if ok: return f'<path d="M{x} {y} l{16*s} {16*s} l{34*s} {-38*s}" fill="none" stroke="{TL}" stroke-width="{9*s}" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<path d="M{x} {y-20*s} l{36*s} {36*s} M{x+36*s} {y-20*s} l{-36*s} {36*s}" stroke="#C4553E" stroke-width="{9*s}" stroke-linecap="round"/>'
def offer(lines, sub):
    o = f'<rect x="12" y="12" width="{FW-24}" height="{FH-24}" rx="6" fill="{DEEP}"/><circle cx="{FW-70}" cy="74" r="20" fill="{TL}"/>'
    for i, l in enumerate(lines): o += tx(FW / 2, 200 + i * 66, l, 54, "#fff", "Space Grotesk", "middle")
    o += f'<rect x="{FW/2-230}" y="{230 + len(lines) * 66}" width="140" height="84" rx="42" fill="#fff"/>{tx(FW/2-160, 288 + len(lines) * 66, "AI", 52, DEEP, "Space Grotesk", "middle")}'
    o += tx(FW / 2 - 70, 286 + len(lines) * 66, "deb izoh yozing", 48, SOFT)
    o += tx(FW / 2, 400 + len(lines) * 66, sub, 38, SOFT, anchor="middle")
    return o

def build(slides, motif=None):
    N = len(slides); W = SW * N
    dots = f'<pattern id="dots" width="27" height="27" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#C9DCDC"/></pattern>'
    rough = '<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>'
    body = ""
    for i, s in enumerate(slides):
        o = i * SW
        g = f'<g transform="translate({o},0)">'
        g += tx(70, 118, s.get("kick", ""), 32, P, "Hanken Grotesk", weight=600) + tx(SW - 70, 118, "AI sotuvchi", 40, P, anchor="end")
        for k, l in enumerate(s["h"]):
            g += tx(70, 235 + k * 84, l, 76, TL if (k == len(s["h"]) - 1 and s.get("teal", True)) else INK, "Space Grotesk")
        g += (f'<g transform="translate({FX},{FY})"><g filter="url(#rough)"><rect width="{FW}" height="{FH}" rx="8" fill="#fff" stroke="{INK}" stroke-width="6"/>{s["art"]}</g>'
              f'<circle cx="52" cy="52" r="30" fill="{TL}"/>{tx(52, 64, str(i + 1), 32, "#fff", "Space Grotesk", "middle")}</g>')
        if s.get("cap"): g += tx(SW / 2, 1268, s["cap"], 46, INK, anchor="middle")
        g += tx(SW - 70, 1318, f"{i + 1}/{N}", 28, GREYT, "Hanken Grotesk", "end", 600)
        if i == 0: g += tx(70, 1318, "surib ko'ring →", 40, TL)
        body += g + "</g>"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{SH}" viewBox="0 0 {W} {SH}"><defs>{rough}{dots}</defs>'
           f'<rect width="{W}" height="{SH}" fill="#F5F5F3"/><rect width="{W}" height="{SH}" fill="url(#dots)"/>{body}</svg>')
    return typo_markup(svg)

def guruh():
    S = []
    S.append(dict(kick="#1 · AI sotuvchi", h=["Guruhda mijoz", "yozadi. Siz esa", "ko'rmaysiz."], art=chat(170, 60, 600, 12, hi=7) , cap="xabar ko'milib ketdi"))
    S.append(dict(kick="Bizning guruh: 2000 kishi", h=["Kuniga", "1000–2000 ta", "xabar."], art=chat(60, 70, 380, 12) + chat(330, 120, 380, 11, title="...") + chat(560, 170, 330, 10, title="..."), cap="hammasini o'qib bo'lmaydi"))
    S.append(dict(kick="Ichida bittasi", h=["Shulardan bittasi", "pulli mijoz:"], art=f'<g transform="translate(80,90)"><rect width="780" height="120" rx="60" fill="#fff" stroke="{TL}" stroke-width="6"/>{tx(60, 78, "SMM kerak! narxi qancha?", 56, DEEP)}</g>'
              + f'<circle cx="600" cy="420" r="120" fill="{LIGHT}" fill-opacity=".6" stroke="{INK}" stroke-width="10"/><path d="M690 510 l120 110" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>' + person(250, 340, 1.5, "down", "wow"), cap="u hozir yozdi"))
    S.append(dict(kick="15:00 → 18:00", h=["Siz ko'rguningizcha", "3 soat o'tdi."], art=person(260, 230, 1.6, "phone", "worry") + clock(640, 280, 160, 6, 10) + bubble(480, 480, 340, 100, "3 soat o'tdi...", (-90, 0), 40, fill=LIGHT), cap="kech ko'rdingiz"))
    S.append(dict(kick="Bu orada", h=["U allaqachon", "boshqasi bilan", "kelishdi."], art=person(300, 250, 1.6, "point") + person(640, 250, 1.6, "point", flip=True) + f'<circle cx="470" cy="330" r="22" fill="{SOFT}" stroke="{INK}" stroke-width="4"/>' + bubble(560, 50, 320, 100, "kelishdik!", (-60, 30), 46) + tx(110, 92, "raqobatchingiz →", 40, GREYT), cap="mijoz ketdi"))
    S.append(dict(kick="Odatdagi yechim", h=["Kuzatish uchun", "odam yollash?", "Qimmat."], art=person(240, 220, 1.6, "down", "ok") + card(470, 120, 380, 110, "Sotuvchi", "har oy oylik") + card(470, 260, 380, 110, "Ish vaqti", "9:00 – 18:00") + card(470, 400, 380, 110, "Kechasi", "hech kim yo'q"), cap="biz boshqacha qildik"))
    S.append(dict(kick="27-sentabr, 15:34", h=["Guruhni biz o'rnimizga", "o'qiydigan agent", "qurdik."], art=robot(180, 230, 2.2) + chat(470, 90, 400, 11, hi=5), cap="agent ishga tushdi"))
    S.append(dict(kick="Agent nima qiladi", h=["Har xabarni o'qiydi.", "Faqat mijozni", "ajratadi."], art=funnel(80, 120) + f'<rect x="150" y="490" width="170" height="48" rx="24" fill="{TL}" stroke="{INK}" stroke-width="3"/>{tx(235, 524, "mijoz ✓", 36, "#fff", anchor="middle")}'
              + tx(470, 200, "spam", 46, GREYT) + mark(640, 190, False) + tx(470, 320, "o'z xizmatini sotuvchi", 40, GREYT) + mark(810, 310, False, .8) + tx(470, 440, "ish so'rayotgan", 46, INK) + mark(780, 430, True), cap="keraksizi o'tib ketadi"))
    S.append(dict(kick="17:05", h=["1,5 soatda birinchi", "mijoz. 3 haftada", "300 ga yaqin."], art=card(70, 80, 420, 120, "🔥 Issiq mijoz", "1,5 soatda topildi") + clock(270, 400, 120, 5, 5) + stack(640, 540, 26, 200) + tx(740, 110, "~300", 60, DEEP, "Space Grotesk", "middle"), cap="sotuvchi yollamasdan"))
    S.append(dict(kick="Bitta qoida", h=["Mijoz yozadi.", "Kim birinchi ko'rsa,", "o'sha oladi."], art=offer(["Sizning guruhlaringizda", "ham ishlaydi"], "to'liq maqolani Direct'ga yuboraman"), cap="Bepul 15 daqiqalik tahlil: @sp_business_agency"))
    return S

def instagram():
    S = []
    S.append(dict(kick="#2 · AI sotuvchi", h=["Instagram'da", "“narxi qancha?”", "deb so'rashdi."], art=igpost(120, 120, s=1.25) + timer(720, 300, "0:00"), cap="soat yura boshladi"))
    S.append(dict(kick="0:30", h=["U javob", "kutyapti."], art=person(260, 230, 1.6, "phone", "ok") + timer(700, 260, "0:30") + bubble(480, 430, 360, 100, "javob bormi?", (-80, 0), 42), cap="hali qiziqyapti"))
    S.append(dict(kick="2:00", h=["2 daqiqa. Boshqa", "sahifalarni", "ko'ryapti."], art=person(220, 230, 1.6, "phone", "flat") + igpost(400, 90, "arzonroq?", .8) + igpost(560, 130, "bor", .8) + timer(820, 140, "2:00"), cap="raqobatchilar yonida"))
    S.append(dict(kick="5:00", h=["5 daqiqa.", "Ketdi."], art=timer(470, 250, "5:00", True) + f'<path d="M150 470 h640" stroke="{SOFT}" stroke-width="6" stroke-dasharray="14 14" stroke-linecap="round"/>' + tx(470, 560, "endi u boshqa sahifada", 44, GREYT, anchor="middle"), cap="javob kech keldi"))
    S.append(dict(kick="Ikkinchi muammo", h=["Doimiy mijoz ham", "norozi: muddat", "esdan chiqdi."], art=person(250, 230, 1.6, "down", "worry") + card(470, 110, 400, 110, "Kelishuv: 3 ta video", "juma kuni") + card(470, 260, 400, 110, "Juma", "esdan chiqdi") + mark(780, 330, False, .9) + bubble(470, 420, 400, 100, "qachon bo'ladi?", (-90, 0), 42), cap="ishonch ketadi"))
    S.append(dict(kick="15-oktabr", h=["Agentga Instagram'ni", "ham uladik."], art=robot(190, 230, 2.2) + f'<path d="M430 330 h120" stroke="{INK}" stroke-width="6" stroke-dasharray="4 14" stroke-linecap="round"/>' + ig_icon(600, 230, 1.6), cap="bitta agent, ikki tarmoq"))
    S.append(dict(kick="0:03", h=["Izohga darhol javob,", "keyin Direct."], art=igpost(80, 120, s=1.05) + timer(800, 160, "0:03") + bubble(440, 330, 420, 130, "Assalomu alaykum!\nDirect'ga yozdim", (-120, 0), 40, fill=LIGHT), cap="mijoz kutmaydi"))
    S.append(dict(kick="Doimiy mijozlar uchun", h=["Har mijozga", "karta va eslatma."], art=card(80, 90, 460, 260, "Mijoz kartasi") + f'<path d="M110 200 h300 M110 250 h240 M110 300 h280" stroke="{SOFT}" stroke-width="10" stroke-linecap="round"/>'
              + f'<g transform="translate(640,150)"><path d="M60 0 c-40 0 -60 30 -60 70 v60 l-20 30 h160 l-20 -30 v-60 c0 -40 -20 -70 -60 -70z" fill="{LIGHT}" stroke="{INK}" stroke-width="5"/><circle cx="60" cy="176" r="16" fill="{TL}" stroke="{INK}" stroke-width="4"/></g>' + tx(700, 430, "muddat yaqin!", 44, P, anchor="middle"), cap="hech narsa esdan chiqmaydi"))
    S.append(dict(kick="Natija", h=["Telegram va Instagram", "bitta agentda.", "Qo'shimcha xarajatsiz."], art=tg_icon(200, 180, 1.5) + robot(410, 210, 1.7) + ig_icon(620, 180, 1.5) + tx(470, 560, "bepul modellarda ishlaydi", 44, P, anchor="middle"), cap="ikkala tarmoq nazoratda"))
    S.append(dict(kick="Bitta qoida", h=["Tez javob ham", "sotuvning bir", "qismi."], art=offer(["Instagram'ingizni", "ham ulaymiz"], "to'liq maqolani Direct'ga yuboraman"), cap="Bepul 15 daqiqalik tahlil: @sp_business_agency"))
    return S

def oqitish():
    S = []
    S.append(dict(kick="#3 · AI sotuvchi", h=["AI noto'g'ri odamga", "yozsa, obro'yingiz", "ketadi."], art=robot(180, 230, 2) + person(700, 240, 1.6, "down", "flat", flip=True) + bubble(360, 60, 360, 100, "xizmat kerakmi?", (40, 30), 42), cap="agentning eng katta xavfi"))
    S.append(dict(kick="1-xavf", h=["Raqobatchingizga", "“xizmatimiz", "kerakmi?”"], art=robot(160, 230, 1.8) + person(680, 240, 1.6, "point", "smile", flip=True) + tx(560, 110, "raqobatchingiz", 40, GREYT) + bubble(250, 400, 320, 100, "o'zim ham shu!", (60, 0), 40), cap="kulgili, lekin zararli"))
    S.append(dict(kick="2-xavf", h=["O'zi xizmat", "sotayotgan odamga", "taklif."], art=robot(160, 230, 1.8) + chat(440, 80, 420, 9, hi=3, title="Guruh", hit="SMM xizmati: 50% chegirma!") , cap="u mijoz emas, sotuvchi"))
    S.append(dict(kick="Natija", h=["Sizni spamchi", "deb o'ylashadi."], art=person(200, 240, 1.4, "down", "worry") + person(470, 240, 1.4, "down", "flat") + person(740, 240, 1.4, "down", "flat") + tx(470, 560, "“yana reklama...”", 50, GREYT, anchor="middle"), cap="obro‘ bir marta ketadi"))
    S.append(dict(kick="15–17-oktabr", h=["121 ta suhbatni", "birma-bir", "tekshirdik."], art=stack(110, 560, 30, 260) + f'<g transform="translate(460,120)"><rect width="380" height="170" rx="20" fill="{LIGHT}" stroke="{INK}" stroke-width="5"/>{tx(190, 120, "121", 110, DEEP, "Space Grotesk", "middle")}</g>' + tx(650, 400, "haqiqiy suhbat", 46, P, anchor="middle"), cap="hech biri tashlab ketilmadi"))
    S.append(dict(kick="Har biriga baho", h=["Kimga yozish to'g'ri", "edi, kimga", "noto'g'ri."], art="".join(f'<g transform="translate(110,{70 + k * 105})"><rect width="560" height="80" rx="14" fill="#fff" stroke="{INK}" stroke-width="3.5"/><path d="M28 32 h{300 - k * 30} M28 54 h{200 + k * 20}" stroke="{SOFT}" stroke-width="8" stroke-linecap="round"/></g>' + mark(740, 115 + k * 105, k not in (1, 3)) for k in range(5)), cap="imtihon varaqasi"))
    S.append(dict(kick="Qayta o'qitish", h=["Agentni shu", "suhbatlar asosida", "qayta o'qitdik."], art=robot(200, 230, 2.2) + f'<path d="M210 210 l110 -40 l110 40 l-110 40z" fill="{DEEP}" stroke="{INK}" stroke-width="4"/><path d="M410 218 v60" stroke="{INK}" stroke-width="4"/>' + f'<g transform="translate(560,160)"><path d="M0 20 q90 -30 160 0 v280 q-70 -30 -160 0z M160 20 q70 -30 160 0 v280 q-90 -30 -160 0z" fill="#fff" stroke="{INK}" stroke-width="5"/><path d="M30 80 h100 M30 120 h90 M190 80 h100 M190 120 h80" stroke="{SOFT}" stroke-width="7" stroke-linecap="round"/></g>', cap="haqiqiy misollardan"))
    S.append(dict(kick="Yana qo'shildi", h=["Endi agent", "qo'shimcha ham", "ishlaydi:"], art="".join(card(90, 50 + k * 112, 760, 92, t) + mark(770, 105 + k * 112, True, .8) for k, t in enumerate(["Har kech shom vaqtida hisobot", "Yangi guruhlarni o'zi qidiradi", "Ish e'lonlari kanallarini kuzatadi", "Ovozli xabar → matn", "Mijozlarga eslatma"])), cap="bitta agent, besh vazifa"))
    S.append(dict(kick="Natija", h=["Keraksiz odamni", "o'zi o'tkazib", "yuboradi."], art=robot(130, 230, 1.8) + person(470, 240, 1.3, "down", "flat") + mark(430, 470, False, .9) + person(740, 240, 1.3, "point", "smile", flip=True) + mark(700, 480, True) + tx(470, 600, "siz esa har kech hisobotni ko'rasiz", 40, P, anchor="middle"), cap="faqat kerakli odamga yozadi"))
    S.append(dict(kick="Bitta qoida", h=["AI'ni o'qitmasangiz,", "u sizning nomingizdan", "xato qiladi."], art=offer(["Sizning xizmatingizga", "moslab o'qitamiz"], "to'liq maqolani Direct'ga yuboraman"), cap="Bepul 15 daqiqalik tahlil: @sp_business_agency"))
    return S

if __name__ == "__main__":
    S = {"guruh": guruh, "instagram": instagram, "oqitish": oqitish}[sys.argv[1]]()
    open(sys.argv[2], "w").write(build(S)); print("ok")
