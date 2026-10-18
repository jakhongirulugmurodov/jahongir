# "Konveyer" karuseli (10 slayd, 1080x1350): bitta uzun panorama, slaydlar orasida lenta uzilmay davom etadi.
# Foydalanish: python3 tools/carousel/konveyer.py <chiqish_papka>  → konveyer.svg (10800x1350)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storyboard"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from doodle import Frame, INK, TEAL, SOFT, DEEP, GREY, PAPER, GRID
from uztypo import typo_markup
SW, SH, N = 1080, 1350, 10
W = SW * N
BELT = 1110
class Pano(Frame):
    def svg(self):
        grid = "".join(f'<path d="M{i} 0V{SH}"/>' for i in range(0, W + 1, 45)) + "".join(f'<path d="M0 {j}H{W}"/>' for j in range(0, SH + 1, 45))
        return typo_markup(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {SH}" width="{W}" height="{SH}" class="dood still">'
            '<style>.l{fill:none;stroke-linecap:round;stroke-linejoin:round}</style>'
            f'<rect width="{W}" height="{SH}" fill="{PAPER}"/><g stroke="{GRID}" stroke-width="2">{grid}</g>{"".join(self.parts)}</svg>')
f = Pano("", 0)
def head(i, lines, y0=250, size=92, gap=1.08, last_teal=True, x=80):
    for k, t in enumerate(lines):
        f.text(i * SW + x, y0 + k * size * gap, t, size, TEAL if (last_teal and k == len(lines) - 1) else INK, anchor="start", font="Space Grotesk")
def kick(i, t): f.text(i * SW + 80, 130, t, 34, TEAL, anchor="start", font="Hanken Grotesk", weight=600)
def note(i, x, y, t, size=52, rot=-3, color=INK): f.text(i * SW + x, y, t, size, color, rot=rot)
# lenta: 1-slayd o'rtasidan 10-slaydgacha
x0, x1 = 560, W - 260
f.line(f"M{x0} {BELT} H{x1}", w=6); f.line(f"M{x0} {BELT + 56} H{x1}", w=6)
f.line(f"M{x0} {BELT} a28 28 0 0 0 0 56 M{x1} {BELT} a28 28 0 0 1 0 56", w=6)
for x in range(x0 + 60, x1, 120):
    f.line(f"M{x - 14} {BELT + 28} a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0", w=4, color=GREY)
for i in range(N):
    f.text(i * SW + SW - 70, SH - 60, f"{i + 1}/10", 30, GREY, anchor="end", font="Hanken Grotesk", weight=600)

# 1 — muqova
kick(0, "#5 · Shaxsiy blog tizimi")
head(0, ["Post yozish", "oson.", "Uni tarqatish", "qiyin."], y0=290, size=112)
f.person(330, BELT - 4, "slump", 2.1, face="sad")
note(0, 820, 1260, "surib ko'ring →", 56, -2, TEAL)
# 2 — har kuni
kick(1, "Tanish holatmi?")
head(1, ["Har kuni bitta", "post. Va har kuni", "shu takrorlanadi:"], size=84)
f.person(SW + 300, BELT - 4, "worry", 2.0, face="sad")
for k, (lbl, dx) in enumerate([("sayt", 560), ("kanal", 760), ("Instagram", 560), ("story", 760)]):
    f.box(SW + dx, 600 + (k // 2) * 200, 180, 150); f.text(SW + dx + 90, 690 + (k // 2) * 200, lbl, 32 if len(lbl) < 8 else 26, font="Space Grotesk")
note(1, 820, 1020, "har kuni...", 50, -4, TEAL)
# 3-6 — to'rt bekat
st = [("1-qadam:", "saytga joylash", "boshladik..."), ("2-qadam:", "kanalga moslash", "matnni qayta yozish"),
      ("3-qadam:", "Instagram o'lchami", "rasmni qayta kesish"), ("4-qadam:", "ikki xil story", "yana ikki o'lcham")]
for k, (a, b, n) in enumerate(st):
    i = 2 + k; o = i * SW
    kick(i, f"Bekat {k + 1}/4")
    head(i, [a, b], size=96)
    if k == 0: f.browser(o + 520, BELT - 300, 360, 290, "sayt"); f.lines(o + 550, BELT - 210, 300, 3, 28)
    if k == 1: f.box(o + 540, BELT - 280, 330, 270); f.tg(o + 705, BELT - 160, 1.5)
    if k == 2: f.box(o + 560, BELT - 330, 300, 320); f.ig(o + 710, BELT - 170, 1.6)
    if k == 3:
        f.box(o + 520, BELT - 380, 170, 370); f.text(o + 605, BELT - 190, "story", 34, font="Space Grotesk")
        f.box(o + 720, BELT - 380, 170, 370); f.text(o + 805, BELT - 190, "story", 34, font="Space Grotesk")
    f.person(o + 260, BELT - 4, ["press", "press", "worry", "slump"][k], 1.9, face=["smile", "flat", "sad", "sad"][k])
    f.clock(o + 880, 560, 60 + k * 6)
    note(i, 560, 1270, n, 50, -2)
# 7 — burilish
kick(6, "Bir tarixiy misol")
head(6, ["Genri Ford", "ishchini tezlatmadi.", "Ishni ishchiga", "olib keldi."], size=86)
o = 6 * SW
f.line(f"M{o + 560} {BELT - 20} h360 v-90 l-60 -70 h-170 l-60 70 h-70 z", w=6)
f.line(f"M{o + 640} {BELT - 20} a32 32 0 1 0 64 0 a32 32 0 1 0 -64 0 M{o + 820} {BELT - 20} a32 32 0 1 0 64 0 a32 32 0 1 0 -64 0", w=6)
f.person(o + 260, BELT - 4, "point", 1.9)
note(6, 560, 1270, "1913-yil, birinchi konveyer", 46, -2, TEAL)
# 8 — bizning konveyer
kick(7, "Biz ham konveyer qurdik")
head(7, ["Siz bir marta", "aytasiz. Qolgani", "o'zi tayyorlanadi."], size=84)
o = 7 * SW
f.person(o + 200, BELT - 4, "point", 1.8)
f.box(o + 420, BELT - 300, 260, 290, "#E9F3F3"); f.text(o + 550, BELT - 140, "tizim", 48, DEEP, font="Space Grotesk")
f.line(f"M{o + 520} {BELT - 330} a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0", w=5)
for k, lbl in enumerate(["sayt", "kanal", "IG", "story"]):
    f.box(o + 720 + (k % 2) * 150, BELT - 300 + (k // 2) * 150, 130, 130); f.text(o + 785 + (k % 2) * 150, BELT - 225 + (k // 2) * 150, lbl, 30, font="Space Grotesk")
f.bubble(o + 80, 640, 300, 120, "bugun shuni\nhal qildik", tail=(40, 30), size=40)
# 9 — natija
kick(8, "Natija")
head(8, ["18-oktabr:", "3 ta story chiqdi.", "Qo'lda joylandi:", "0 marta."], size=88)
f.person(9 * SW - 300, BELT - 4, "cheer", 2.0)
f.story_ring(8 * SW + 200, 900, 40); f.story_ring(8 * SW + 310, 900, 40); f.story_ring(8 * SW + 420, 900, 40)
# 10 — xulosa va taklif
kick(9, "Bitta qoida")
head(9, ["Yozish sizning", "ishingiz.", "Tarqatish", "tizimning ishi."], size=100)
o = 9 * SW
f.pill(o + 80, 760, 150, 96, "AI", fill="#fff", color=DEEP, size=58)
f.text(o + 260, 822, "deb izoh yozing:", 56, anchor="start")
f.text(o + 80, 900, "to'liq maqolani Direct'ga yuboraman", 52, TEAL, anchor="start")
f.text(o + 80, 1290, "Bepul 15 daqiqalik tahlil: @sp_business_agency", 34, INK, anchor="start", font="Hanken Grotesk", weight=600)
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
open(os.path.join(out, "konveyer.svg"), "w").write(f.svg())
print("ok")
