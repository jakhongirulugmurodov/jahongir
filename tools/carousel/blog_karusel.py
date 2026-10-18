# "Shaxsiy blog tizimi" karusellari (10 slayd, 1080x1350): katak qog'oz, teal tanali odamchalar,
# slaydlar orasida uzilmaydigan bitta motiv (konveyer.py bilan bir uslub).
# Foydalanish: python3 blog_karusel.py <zanjir|iz> <chiqish.svg>
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storyboard"))
from doodle import Frame, INK, TEAL, SOFT, DEEP, GREY, PAPER, GRID
from uztypo import typo_markup
SW, SH, N = 1080, 1350, 10; W = SW * N; G = 1110
class Pano(Frame):
    def svg(self):
        grid = "".join(f'<path d="M{i} 0V{SH}"/>' for i in range(0, W + 1, 45)) + "".join(f'<path d="M0 {j}H{W}"/>' for j in range(0, SH + 1, 45))
        return typo_markup(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {SH}" width="{W}" height="{SH}" class="dood still">'
            '<style>.l{fill:none;stroke-linecap:round;stroke-linejoin:round}</style>'
            f'<rect width="{W}" height="{SH}" fill="{PAPER}"/><g stroke="{GRID}" stroke-width="2">{grid}</g>{"".join(self.parts)}</svg>')
f = Pano("", 0)
def head(i, lines, y0=250, size=92, gap=1.08):
    for k, t in enumerate(lines): f.text(i * SW + 80, y0 + k * size * gap, t, size, TEAL if k == len(lines) - 1 else INK, anchor="start", font="Space Grotesk")
def kick(i, t): f.text(i * SW + 80, 130, t, 34, TEAL, anchor="start", font="Hanken Grotesk", weight=600)
def note(i, x, y, t, size=50, rot=-3, color=INK): f.text(i * SW + x, y, t, size, color, rot=rot)
def nums():
    for i in range(N): f.text(i * SW + SW - 70, SH - 60, f"{i + 1}/10", 30, GREY, anchor="end", font="Hanken Grotesk", weight=600)
def final(i, lines, offer):
    head(i, lines, size=100); o = i * SW
    f.pill(o + 80, 760, 150, 96, "AI", fill="#fff", color=DEEP, size=58)
    f.text(o + 260, 822, "deb izoh yozing:", 56, anchor="start")
    f.text(o + 80, 900, "to'liq maqolani Direct'ga yuboraman", 52, TEAL, anchor="start")
    f.text(o + 80, 1290, offer, 34, INK, anchor="start", font="Hanken Grotesk", weight=600)

def zanjir():
    # Motiv: bitta sharcha slaydlar bo'ylab yumalab, domino zanjirini yurgizadi (bir marta yozasiz → hammasi o'zi).
    kick(0, "#4 · Shaxsiy blog tizimi"); head(0, ["Har postni", "alohida joylashdan", "charchadingizmi?"], size=90)
    f.person(330, G, "slump", 2.0, face="sad")
    for k in range(4): f.phone(560 + k * 105, 640 + (k % 2) * 40, 0.75, rot=-8 + k * 6)
    note(0, 230, 1270, "surib ko‘ring →", 50, -2, TEAL)
    kick(1, "Har safar"); head(1, ["Rasmni moslash,", "havola qo'shish,", "vaqt kutish."], size=86)
    o = SW
    for k, t in enumerate(["rasm o'lchami", "havola", "qulay vaqt", "yana takror"]):
        f.box(o + 470, 640 + k * 110, 70, 70); f.line(f"M{o + 485} {675 + k * 110} l15 15 l30 -34", w=6, color=TEAL); f.text(o + 570, 690 + k * 110, t, 48, anchor="start")
    f.person(o + 260, G, "worry", 1.9, face="sad")
    kick(2, "Oxiri"); head(2, ["Sahifa haftalab", "jim turadi."], size=96)
    o = 2 * SW; f.calendar(o + 470, 560, 470, 430, marks=(), title="Oktabr")
    f.person(o + 240, G, "think", 1.9, face="flat"); note(2, 600, 1060, "jim sahifaga mijoz ishonmaydi", 44, -2, TEAL)
    kick(3, "Biz boshqacha qildik"); head(3, ["Bir marta", "yozasiz."], size=110)
    o = 3 * SW; f.person(o + 260, G, "press", 1.9); f.box(o + 400, 820, 230, 150); f.lines(o + 425, 860, 170, 3, 30)
    # yo'lak: 4-slayddan 9-slaydgacha qiya rampa + sharcha
    track = []
    x0 = 3 * SW + 640
    f.line(f"M{x0} 990 L{9 * SW - 120} 1090", w=6); f.line(f"M{x0} 1010 L{9 * SW - 120} 1110", w=4, color=GREY)
    ball = lambda x, y: (f.fill(f"M{x - 22} {y} a22 22 0 1 0 44 0 a22 22 0 1 0 -44 0", TEAL), f.line(f"M{x - 22} {y} a22 22 0 1 0 44 0 a22 22 0 1 0 -44 0", w=4))
    yat = lambda x: 990 + (x - x0) * 100 / (9 * SW - 120 - x0)
    ball(x0 + 60, yat(x0 + 60) - 24); note(3, 720, 940, "tushdi!", 44, -6, TEAL)
    # 5-8: har slaydda domino qulab, natija chiqadi
    st = [("1 → sayt", "post saytda turadi"), ("2 → story rasmlari", "o'zi tayyorlanadi"), ("3 → Telegram", "story chiqdi"), ("4 → Instagram", "story chiqdi")]
    for k, (a, b) in enumerate(st):
        i = 4 + k; o = i * SW; kick(i, f"Zanjir {k + 1}/4"); head(i, [a, b], size=90)
        bx = o + 300; by = yat(bx)
        for d in range(3):
            xx = bx + d * 60; yy = yat(xx); ang = -55 + d * 18
            f.raw(f'<rect x="{xx - 12}" y="{yy - 120}" width="24" height="120" rx="4" fill="#fff" stroke="{INK}" stroke-width="4.5" transform="rotate({ang if d < 2 else 0} {xx} {yy})"/>')
        ball(o + 120, yat(o + 120) - 24)
        f.line(f"M{o + 140} {yat(o + 140) - 70} l40 0 M{o + 130} {yat(o + 130) - 50} l50 0", w=4, color=GREY)
        if k == 0: f.browser(o + 560, 560, 380, 300, "sayt"); f.lines(o + 590, 660, 300, 4, 34)
        if k == 1:
            f.box(o + 560, 520, 160, 330); f.text(o + 640, 700, "TG", 44, font="Space Grotesk"); f.box(o + 760, 520, 160, 330); f.text(o + 840, 700, "IG", 44, font="Space Grotesk")
        if k == 2: f.phone(o + 640, 520, 1.5); f.tg(o + 730, 680, 1.4)
        if k == 3: f.phone(o + 640, 520, 1.5); f.ig(o + 730, 680, 1.4)
    kick(8, "17-oktabr → 18-oktabr"); head(8, ["Ertasi kuni ertalab", "story'lar o'zi chiqdi.", "Qo'lda: 0 marta."], size=80)
    o = 8 * SW; f.person(o + 620, G - 40, "cheer", 2.0)
    for k in range(3): f.story_ring(o + 160 + k * 120, 800, 44)
    final(9, ["Jim sahifaga", "mijoz", "ishonmaydi."], "Bepul 15 daqiqalik tahlil: @sp_business_agency")
    nums()

def iz():
    # Motiv: oyoq izlari 1-slayddan 10-slaydgacha uzilmay boradi va kundan-kunga ko'payadi (har kungi yozuv = iz).
    def foot(x, y, left, sc=1.0, col=TEAL):
        dy = -14 if left else 14
        f.fill(f"M{x - 16 * sc} {y + dy} a{16 * sc} {24 * sc} 0 1 0 {32 * sc} 0 a{16 * sc} {24 * sc} 0 1 0 {-32 * sc} 0", col, 0.85)
        for t in range(3): f.fill(f"M{x - 16 * sc + t * 13 * sc} {y + dy - 34 * sc} a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0", col, 0.85)
    # iz yo'li
    xs = list(range(4 * SW + 120, W - 200, 95))
    for n, x in enumerate(xs): foot(x, G + 20 + math.sin(n * 0.5) * 18, n % 2 == 0, 0.9 + n * 0.006)
    kick(0, "#6 · Shaxsiy blog tizimi"); head(0, ["Ishingiz yaxshi.", "Lekin buni hech kim", "ko'rmasa-chi?"], size=86)
    o = 0
    f.raw(f'<g opacity=".35">' + "".join(f'<circle cx="{330 + a}" cy="{790 + b}" r="4" fill="{INK}"/>' for a, b in [(0, 0)]) + '</g>')
    f.person(330, G, "stand", 2.0, face="flat"); f.raw(f'<rect x="200" y="640" width="260" height="480" fill="{PAPER}" fill-opacity=".6"/>')
    f.line("M200 640 h260 v480 h-260 z", w=4, color=GREY, extra='stroke-dasharray="12 14"'); note(0, 600, 900, "ko'rinmas usta", 52, -3, GREY)
    note(0, 230, 1270, "surib ko‘ring →", 50, -2, TEAL)
    kick(1, "Mijoz nima qiladi"); head(1, ["Ishonishdan oldin", "isbot qidiradi."], size=92)
    o = SW; f.person(o + 280, G, "think", 1.9)
    f.line(f"M{o + 600} 760 a110 110 0 1 0 220 0 a110 110 0 1 0 -220 0", w=10); f.line(f"M{o + 790} 840 l110 110", w=24)
    note(1, 720, 600, "nima qilgansiz?", 44, -4, TEAL)
    kick(2, "Ijtimoiy tarmoqda"); head(2, ["Post 1–2 kunda", "lentaning pastiga", "tushib ketadi."], size=86)
    o = 2 * SW; f.phone(o + 560, 600, 1.9)
    for k in range(5): f.box(o + 590, 650 + k * 70, 170, 52, SOFT if k == 4 else "#fff")
    f.arrow(f"M{o + 860} 650 V1000", w=6, head=(o + 860, 1000, 90)); f.person(o + 250, G, "worry", 1.9, face="sad")
    kick(3, "Natija"); head(3, ["Ishlaringiz yana", "ko'rinmay qoladi."], size=92)
    o = 3 * SW; f.person(o + 300, G, "slump", 2.0, face="sad")
    for k in range(3): f.box(o + 560 + k * 60, 700 + k * 40, 260, 160, "#fff", rot=-6 + k * 6)
    note(3, 620, 1060, "eski ishlar...", 48, -3, GREY)
    kick(4, "Yechim"); head(4, ["Har kuni bitta hal", "qilingan muammo."], size=90)
    o = 4 * SW; f.person(o + 760, G - 10, "walk", 1.9); note(4, 120, 1270, "1-kun: birinchi iz", 46, -2, TEAL)
    kick(5, "Formula"); head(5, ["Nima bo'ldi →", "qanday hal qildik →", "natija."], size=84)
    o = 5 * SW
    for k, t in enumerate(["muammo", "yechim", "natija"]): f.box(o + 90 + k * 310, 720, 270, 170, "#E9F3F3" if k == 2 else "#fff"); f.text(o + 225 + k * 310, 820, t, 46, DEEP if k == 2 else INK, font="Space Grotesk")
    kick(6, "Saytda doim turadi"); head(6, ["Loyihalar papkada,", "kunlar taqvimda."], size=90)
    o = 6 * SW; f.folder(o + 110, 640, 300, 220, "loyihalar"); f.calendar(o + 500, 560, 440, 400, marks=(0, 2, 3, 6, 8, 11, 12, 15, 16, 17))
    kick(7, "Tarmoqlar nima qiladi"); head(7, ["Telegram va Instagram", "odamlarni saytga", "olib keladi."], size=80)
    o = 7 * SW; f.tg(o + 170, 700, 1.6); f.ig(o + 170, 900, 1.6)
    f.arrow(f"M{o + 250} 700 Q{o + 420} 700 {o + 520} 790", w=5, head=(o + 520, 790, 40)); f.arrow(f"M{o + 250} 900 Q{o + 420} 900 {o + 520} 830", w=5, head=(o + 520, 830, -30))
    f.browser(o + 540, 660, 400, 300, "sayt"); f.lines(o + 570, 760, 320, 4, 34)
    kick(8, "Endi"); head(8, ["Mijozga bitta", "havola yuboraman.", "Hammasini ko'radi."], size=86)
    o = 8 * SW; f.person(o + 260, G, "phone", 1.9); f.person(o + 760, G, "cheer", 1.9)
    f.pill(o + 380, 690, 300, 80, "1 ta havola", fill="#fff", color=DEEP, size=34)
    final(9, ["Ishonch", "har kungi", "izdan tug'iladi."], "Bepul 15 daqiqalik tahlil: @sp_business_agency")
    nums()

{"zanjir": zanjir, "iz": iz}[sys.argv[1]]()
open(sys.argv[2], "w").write(f.svg()); print("ok")
