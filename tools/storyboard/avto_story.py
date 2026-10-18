# "Avto-story" loyihasi postlari uchun doodle storyboard'lar (3 post × 3 kadr).
# Ishga tushirish: python3 tools/storyboard/avto_story.py <chiqish_papka>  → <post>-<n>.svg
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodle import *
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
F = {}

# ---- 1-post: har postni 3 joyga qo'lda joylash
f = Frame("Bitta post, uch joyga qo'lda", 1)
f.person(300, 790, "worry", 1.7, face="sad")
f.browser(560, 180, 330, 200, "sayt"); f.lines(590, 260, 250, 3)
f.tg(650, 520); f.ig(830, 520); f.story_ring(1010, 520, 34)
f.text(650, 600, "Telegram", 30); f.text(830, 600, "Instagram", 30); f.text(1010, 600, "story", 30)
f.arrow("M420 560 Q480 380 548 300", head=(548, 300, -55)); f.arrow("M430 620 Q520 560 606 530", head=(606, 530, -10))
f.clock(1030, 260, 62); f.text(1030, 370, "har kuni...", 38, TEAL, rot=-4)
f.text(820, 760, "yana va yana qo'lda", 46, rot=-3)
F["avto-1"] = [f]
f = Frame("Saytga bir marta yozasiz", 2)
f.browser(430, 170, 660, 440); f.text(560, 280, "Yangi post", 40, INK, anchor="start", font="Space Grotesk")
f.lines(470, 320, 520, 4, 32)
f.pill(470, 500, 230, 64, "Joylash", size=32)
f.person(330, 770, "press", 1.75)
f.text(860, 700, "1 marta!", 64, TEAL, rot=-6)
F["avto-1"].append(f)
f = Frame("Story'lar o'zi chiqadi", 3)
def scr(x, y, w, h):
    for i in range(3): f.story_ring(x + 30 + i * 32 + 3, y + 48, 13)
    f.fill(f"M{x + 14} {y + 80} h{w - 28} v{h - 110} h{-(w - 28)} z", SOFT, 0.55); f.lines(x + 26, y + 100, w - 52, 3, 24, TEAL)
f.phone(510, 190, 1.35, scr)
f.tg(270, 300); f.ig(270, 520)
f.arrow("M320 300 Q420 300 500 340", head=(500, 340, 20)); f.arrow("M320 520 Q420 520 500 470", head=(500, 470, -25))
f.person(950, 830, "cheer", 1.5)
f.text(270, 700, "har 3 soatda", 44, TEAL, rot=-4); f.text(270, 750, "o'zi chiqadi", 44, TEAL, rot=-4)
F["avto-1"].append(f)

# ---- 2-post: Instagram story'da havola bosilmaydi
f = Frame("Havola bosilmaydi", 1)
def scr2(x, y, w, h):
    f.fill(f"M{x + 14} {y + 30} h{w - 28} v{h - 60} h{-(w - 28)} z", SOFT, 0.5)
    f.pill(x + 22, y + h / 2 - 20, w - 44, 44, "havola", size=22)
    f.line(f"M{x + 30} {y + h / 2 - 34} l{w - 60} 70 M{x + w - 30} {y + h / 2 - 34} l{-(w - 60)} 70", w=6, color="#C0392B")
f.phone(330, 220, 1.6, scr2)
f.person(820, 800, "think", 1.7, face="flat")
f.text(820, 330, "qanday o'qiyman?", 44, rot=-4)
F["avto-2"] = [f]
f = Frame("«AI» deb yozadi", 2)
def scr3(x, y, w, h):
    f.fill(f"M{x + 14} {y + 30} h{w - 28} v{h - 60} h{-(w - 28)} z", SOFT, 0.5)
    f.box(x + 16, y + h - 74, w - 32, 46); f.text(x + w / 2, y + h - 40, "AI", 34, INK, font="Space Grotesk")
f.phone(640, 200, 1.6, scr3)
f.person(400, 800, "phone", 1.75)
f.bubble(150, 210, 260, 120, "«AI»", tail=(40, 30), size=56)
f.arrow("M420 360 Q560 480 650 520", head=(650, 520, 30))
F["avto-2"].append(f)
f = Frame("Havola Direct'ga keladi", 3)
def scr4(x, y, w, h):
    f.box(x + 16, y + 40, w - 60, 56, "#E9F3F3"); f.text(x + 34, y + 76, "Mana maqola:", 22, INK, anchor="start")
    f.pill(x + 16, y + 110, w - 50, 40, "jahongir.onagy.app", fill="#fff", color=TEAL, size=15)
f.phone(250, 210, 1.6, scr4)
f.person(560, 800, "phone", 1.6)
f.box(780, 230, 330, 150, "#fff", rot=3); f.text(945, 290, "Yangi mijoz!", 40, TEAL, rot=3); f.text(945, 340, "Direct'da gaplashyapti", 30, INK, rot=3)
f.person(960, 820, "cheer", 1.3)
F["avto-2"].append(f)

# ---- 3-post: nega sayt kerak
f = Frame("Postlar lentada ko'milib ketadi", 1)
for i in range(6):
    f.box(640 + (i % 2) * 40, 150 + i * 120, 330, 96, "#fff" if i % 2 else "#EEF5F5", rot=(-4 if i % 2 else 3))
    f.lines(670 + (i % 2) * 40, 180 + i * 120, 230, 2, 26)
f.arrow("M1080 200 V780", w=6, head=(1080, 780, 90))
f.person(360, 800, "run", 1.7, face="open")
f.text(360, 380, "qayerda edi?", 48, rot=-5)
F["avto-3"] = [f]
f = Frame("Sayt: ishlaringiz uyi", 2)
f.browser(470, 170, 640, 470)
for i in range(4): f.story_ring(540 + i * 80, 260, 26)
f.folder(520, 350, 150, 110, "Loyihalar"); f.folder(720, 350, 150, 110, "Kundalik"); f.folder(920, 350, 150, 110, "Taqvim")
f.person(260, 800, "point", 1.75)
f.text(790, 720, "hammasi bitta havolada", 46, TEAL, rot=-3)
F["avto-3"].append(f)
f = Frame("Telegram va Instagram: saytga eshik", 3)
f.browser(640, 190, 480, 380); f.lines(680, 280, 380, 4, 32); f.folder(690, 430, 120, 90, ""); f.folder(860, 430, 120, 90, "")
f.tg(150, 300); f.ig(150, 520)
f.arrow("M200 300 Q420 260 628 330", head=(628, 330, 15)); f.arrow("M200 520 Q420 560 628 470", head=(628, 470, -20))
f.person(440, 820, "walk", 1.6)
f.text(560, 560, "mijoz", 44, TEAL, rot=-4)
F["avto-3"].append(f)

for k, frames in F.items():
    for i, fr in enumerate(frames, 1):
        open(os.path.join(out, f"{k}-{i}.svg"), "w").write(fr.svg())
print("ok", sum(len(v) for v in F.values()), "kadr")
