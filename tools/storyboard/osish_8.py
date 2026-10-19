# #8 "3 ta jamoa. 6 oy." — O'sish Nuqtasi: 10 sahna (karusel) + 3 tasi storyboard kadri.
# python3 osish_8.py <papka>  → kadr-1..3.svg (1200x900) va karusel.svg (10800x1350)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marker import *
def s1(m):
    m.shop(140, 200, 400, 400)
    for i, t in enumerate(["1-jamoa", "2-jamoa", "3-jamoa"]):
        y = 210 + i * 150; m.card(640, y, 300, 110, t, "#fff", 40, rot=-3 + i * 3)
        m.line(f"M650 {y + 10} L930 {y + 100} M930 {y + 10} L650 {y + 100}", w=6, color=CORAL, dur=0.25)
    m.note(600, 760, "6 oy o‘tdi", 50, CORAL, rot=-2)
def s2(m):
    m.phone(170, 150, 300, 560); m.big(320, 400, "4–5", 96, CORAL); m.note(320, 470, "ko‘rish", 40)
    m.hero(780, 790, "worry", 1.3, face="sad")
def s3(m):
    for i, (t, c) in enumerate([("kunlik\nsavdo", "leaf"), ("taniqlilik", "sky"), ("B2B\nsavdo", "must")]):
        m.card(110 + i * 345, 270 + (i % 2) * 40, 300, 240, t, H_(c), 46, rot=-4 + i * 4)
    m.note(600, 700, "do‘kon nima xohlaydi", 50, CORAL)
def s4(m):
    m.hero(380, 780, "think", 1.3, face="flat"); m.bubble(540, 200, 460, 170, "uchalasi\nto‘g‘ri istak", (-120, 40), 50)
def s5(m):
    for i, (t, c) in enumerate([("savdo", "leaf"), ("taniqlilik", "sky"), ("B2B", "must")]):
        m.card(150 + i * 320, 220, 270, 130, t, H_(c), 42)
        m.arrow(285 + i * 320, 360, 285 + i * 320, 470, INK)
    m.card(150, 490, 910, 150, "auditoriya", H_("coral"), 64)
    m.note(600, 740, "poydevor bitta", 50, INK)
def s6(m):
    m.hero(600, 790, "shrug", 1.4, face="flat"); m.bubble(660, 150, 440, 160, "muammo jamoada\nemas...", (-120, 40), 46)
def s7(m):
    m.dots(170, 200, 10, 10, 50, 16, filled=42, color="coral")
    m.big(820, 380, "42%", 120, CORAL); m.note(820, 460, "“bozorda ehtiyoj yo‘q”", 40, INK)
    m.note(600, 760, "CB Insights · 101 ta yopilgan startap", 36, INK)
def s8(m):
    for i, (t, c) in enumerate([("1 oylik\nkontent reja", "sky"), ("xarajat", "must"), ("qanday\nqiymat", "leaf")]):
        m.card(110 + i * 345, 260, 300, 240, t, H_(c), 42, rot=-3 + i * 3)
    m.note(600, 680, "hozir shu do‘kon uchun tayyorlayapmiz", 44, CORAL)
def s9(m):
    m.phone(160, 160, 300, 560); m.fill("M250 290 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0", H_("leaf")); m.line("M250 290 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0", w=5)
    m.note(310, 410, "@osish.nuqtasi", 34); m.note(310, 460, "1-video chiqdi", 30, CORAL)
    m.hero(760, 790, "point", 1.3, flip=True); m.note(820, 300, "o‘zimizdan\nboshladik", 46, CORAL)
def s10(m):
    m.hero(300, 790, "happy", 1.3)
    for i in range(14): m.hero(560 + (i % 7) * 85, 520 + (i // 7) * 150, "stand", 0.45, shirt=["sky", "must", "leaf"][i % 3])
    m.card(600, 160, 480, 130, "avval auditoriya", H_("must"), 50, rot=-3)
SC = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
HEAD = [(["3 ta jamoa.", "6 oy."], "#8 · O‘sish Nuqtasi"),
        (["Natija: sahifani", "4–5 kishi ko‘radi."], "Bugungi suhbat"),
        (["Ular uch narsa", "xohlaydi."], "Do‘kon egasi aytdi"),
        (["Uchalasi ham", "to‘g‘ri istak."], "Lekin"),
        (["Uchalasining poydevori", "bitta: auditoriya."], "Asosiy gap"),
        (["Muammo jamoada emas.", "Tartibda."], "Nega ishlamadi"),
        (["Ehtiyoj bormi?", "Keyin so‘raladi."], "Raqamlar"),
        (["Endi reja:", "avval auditoriya."], "Biz nima qilyapmiz"),
        (["Biz ham shunday", "boshladik."], "O‘sish Nuqtasi"),
        (["Auditoriyasiz", "marketing ishlamaydi."], "Bitta qoida")]
CAPS = ["3 ta jamoa, 6 oy", "Poydevor bitta", "Avval auditoriya"]
def carousel():
    N = 10; SW, SH = 1080, 1350; body = ""
    for i, f in enumerate(SC):
        m = Marker("", 0); m.ns = 1.15; f(m)
        lines, kick = HEAD[i]; o = i * SW
        g = f'<g transform="translate({o},0)"><text x="130" y="128" font-family="Patrick Hand" font-size="38" fill="{CORAL}">{kick}</text>'
        for k, l in enumerate(lines): g += f'<text x="130" y="{238 + k * 96}" font-family="Fraunces" font-weight="900" font-size="{84 if len(l) < 20 else 74}" fill="{CORAL if k == len(lines) - 1 else INK}">{l}</text>'
        g += (f'<g transform="translate(110,480)"><rect x="-6" y="-6" width="872" height="682" fill="{INK}" fill-opacity=".08" transform="rotate(1.2 430 340)"/><rect width="860" height="670" fill="#fff" stroke="{INK}" stroke-width="5"/>'
              f'<g transform="translate(-20,-5) scale(0.75)"><g filter="url(#pen)">{"".join(m.parts)}</g></g></g>'
              f'<path d="M{SW/2 - 120} 448 l240 -6 l4 50 l-240 6z" fill="{MUST}" fill-opacity=".8"/>')
        if i == 9:
            g += (f'<rect x="130" y="1190" width="120" height="76" rx="38" fill="{CORAL}"/><text x="190" y="1243" font-family="Fraunces" font-weight="900" font-size="44" fill="#fff" text-anchor="middle">AI</text>'
                  f'<text x="270" y="1240" font-family="Patrick Hand" font-size="46" fill="{INK}">deb izoh yozing — maqolani yuboraman</text>'
                  f'<text x="130" y="1305" font-family="Hanken Grotesk" font-weight="600" font-size="32" fill="{INK}">Bepul 15 daqiqalik suhbat: @sp_business_agency</text>')
        elif i == 0: g += f'<text x="130" y="1250" font-family="Patrick Hand" font-size="46" fill="{CORAL}">surib ko‘ring →</text>'
        g += f'<text x="{SW - 70}" y="{SH - 50}" font-family="Patrick Hand" font-size="34" fill="{INK}" fill-opacity=".5" text-anchor="end">{i + 1}/10</text></g>'
        body += g
    W_ = SW * N
    return typo_markup(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{SH}" viewBox="0 0 {W_} {SH}" class="dood still">{CSS}{defs()}'
                       f'<rect width="{W_}" height="{SH}" fill="{CREAM}"/><g stroke="{LINE}" stroke-width="2.2">' + "".join(f'<path d="M0 {y}H{W_}"/>' for y in range(60, SH, 46)) + "</g>"
                       + "".join(f'<path d="M{i * SW + 92} 0V{SH}" stroke="{MARGIN}" stroke-width="3"/>' for i in range(N)) + f"{body}</svg>")
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for n, (f, cap) in enumerate(zip([s1, s5, s10], CAPS), 1):
    m = Marker(cap, n); f(m); open(f"{out}/osish-8-{n}.svg", "w").write(m.svg())
    open(f"{out}/osish-8-{n}-still.svg", "w").write(m.svg(still=True))
open(f"{out}/karusel.svg", "w").write(carousel()); print("ok")
