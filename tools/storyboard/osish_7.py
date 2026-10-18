# #7 "Do'kon ochdingiz. Mijoz qayerda?" — O'sish Nuqtasi: 10 sahna (karusel) + 3 tasi storyboard kadri.
# python3 osish_7.py <papka>  → kadr-1..3.svg (1200x900) va karusel.svg (10800x1350)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marker import *
def s1(m):
    m.shop(560, 170, 460, 470); m.hero(330, 760, "stand", 1.25, face="flat")
    m.line("M1000 260 l50 -40 M1000 260 l60 10 M1000 260 l40 40 M1020 230 q20 30 40 40", w=2.5, color=INK, dur=0.2)
    m.note(790, 720, "hech kim yo'q...", 46, CORAL, rot=-3)
def s2(m):
    m.hero(260, 780, "worry", 1.25, face="sad")
    m.bill(470, 190, "ijara", -8); m.bill(720, 250, "oylik", 6, fill=H_("must")); m.bill(560, 420, "kommunal", -3, w=240); m.bill(840, 470, "soliq", 9)
    m.note(740, 720, "oy oxiri keldi", 48, CORAL, rot=-2)
def s3(m):
    m.hero(380, 780, "think", 1.3, face="flat"); m.bubble(540, 200, 460, 170, "kimga sotsam\nekan?", (-120, 40), 52)
def s4(m):
    for i, (t, c) in enumerate([("Auditoriyang\nbormi?", "sky"), ("Kimga\nsotmoqchisan?", "must"), ("Ehtiyoj\nbormi?", "leaf")]):
        m.card(110 + i * 345, 260 + (i % 2) * 40, 300, 260, t, H_(c), 42, rot=-4 + i * 4)
    m.note(600, 700, "do'kon ochishdan OLDIN", 52, CORAL)
def s5(m):
    m.hero(600, 790, "shrug", 1.4, face="flat"); m.bubble(660, 150, 420, 140, "bilmayman...", (-120, 40), 50)
def s6(m):
    for i, (t, c) in enumerate([("auditoriya", "sky"), ("ehtiyoj", "must"), ("do'kon", "coral")]):
        m.card(80 + i * 380, 330, 300, 170, t, H_(c), 50)
        if i < 2: m.arrow(390 + i * 380, 380, 450 + i * 380, 380, CORAL)
    m.note(230, 600, "1", 70, INK); m.note(610, 600, "2", 70, INK); m.note(990, 600, "3", 70, INK)
def s7(m):
    m.phone(160, 160, 300, 560); m.fill("M250 290 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0", H_("must")); m.line("M250 290 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0", w=5)
    m.note(310, 410, "@osish.nuqtasi", 34); m.note(310, 460, "0 obunachi", 30, CORAL)
    for i in range(3):
        for j in range(2): m.rect(190 + i * 82, 500 + j * 90, 72, 80, H_("sky") if (i + j) % 2 else "#fff", 6, 3)
    m.hero(760, 790, "point", 1.3, flip=True); m.note(820, 300, "biz ham shunday\nboshladik", 46, CORAL)
def s8(m):
    m.mic(220, 470, 1.3); m.arrow(330, 420, 460, 420, CORAL)
    m.card(470, 330, 220, 170, "eng foydali\nqismi", "#fff", 36); m.arrow(700, 420, 820, 420, CORAL)
    m.hero(960, 760, "happy", 1.1); m.note(560, 640, "ruxsat bilan · o‘z animatsiyamiz", 40, INK)
def s9(m):
    m.dots(170, 220, 15, 6, 58, 18, filled=90, color="coral")
    m.big(600, 680, "90 ta reels / oy", 76, INK); m.note(600, 760, "AI montaj: 9–10 kunda tayyor", 46, CORAL)
def s10(m):
    m.hero(300, 790, "happy", 1.3)
    for i in range(14): m.hero(560 + (i % 7) * 85, 520 + (i // 7) * 150, "stand", 0.45, shirt=["sky", "must", "leaf"][i % 3])
    m.card(640, 160, 420, 130, "keyin — do'kon", H_("must"), 50, rot=-3)
SC = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
HEAD = [(["Do'kon ochdingiz.", "Mijoz qayerda?"], "#7 · O'sish Nuqtasi"),
        (["Oy oxiri: ijara,", "oylik, kommunal."], "Keyin nima bo'ladi"),
        (["Endi savol tug'iladi:", "kimga sotaman?"], "Kech qolgan savol"),
        (["Men har doim", "uch savol beraman."], "Biznes boshlamoqchi bo'lganlarga"),
        (["Ko'pchilikning javobi:", "“bilmayman”."], "Eng xavfli javob"),
        (["Biznes do'kondan emas,", "mijozdan boshlanadi."], "To'g'ri tartib"),
        (["Biz ham shunday", "qilyapmiz."], "18-oktabr"),
        (["Podkastlardan eng", "foydali qism."], "O'sish Nuqtasi qanday ishlaydi"),
        (["Oyiga 90 ta", "reels."], "Reja"),
        (["Avval auditoriya.", "Keyin do'kon."], "Bitta qoida")]
CAPS = ["Do'kon ochildi, mijoz yo'q", "Uch savol", "Avval auditoriya"]
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
for n, (f, cap) in enumerate(zip([s1, s4, s10], CAPS), 1):
    m = Marker(cap, n); f(m); open(f"{out}/osish-7-{n}.svg", "w").write(m.svg())
    open(f"{out}/osish-7-{n}-still.svg", "w").write(m.svg(still=True))
open(f"{out}/karusel.svg", "w").write(carousel()); print("ok")
