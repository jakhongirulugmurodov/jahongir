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

# ---- 2-post: qancha vaqt tejaydi
f = Frame("Har kuni: 4 joy, 4 xil o'lcham", 1)
f.person(250, 800, "slump", 1.7, face="sad")
f.box(470, 190, 250, 160); f.text(595, 290, "sayt", 40, font="Space Grotesk")
f.box(760, 190, 300, 120); f.text(910, 262, "kanal", 40, font="Space Grotesk")
f.box(470, 400, 210, 210); f.text(575, 515, "Instagram", 34, font="Space Grotesk")
f.box(730, 360, 140, 250); f.text(800, 495, "story", 32, font="Space Grotesk")
f.box(900, 360, 140, 250); f.text(970, 495, "story", 32, font="Space Grotesk")
f.clock(1000, 720, 56); f.text(780, 740, "yana qo'lda...", 46, rot=-4)
F["avto-2"] = [f]
f = Frame("Siz faqat aytib berasiz", 2)
f.person(260, 800, "point", 1.7)
f.bubble(110, 230, 330, 130, "bugun shuni\nhal qildik", tail=(40, 30), size=40)
f.arrow("M470 520 Q560 520 620 470", head=(620, 470, -30))
f.browser(640, 190, 240, 170, "sayt"); f.lines(665, 260, 190, 3, 24)
f.box(910, 190, 180, 120); f.text(1000, 262, "kanal", 34, font="Space Grotesk")
f.box(650, 420, 170, 250); f.text(735, 555, "story", 32, font="Space Grotesk")
f.box(850, 420, 240, 240); f.text(970, 550, "post", 36, font="Space Grotesk")
f.text(870, 760, "hammasi o'zi tayyor", 48, TEAL, rot=-3)
F["avto-2"].append(f)
f = Frame("Bo'shagan vaqt mijozlarga", 3)
f.person(380, 800, "point", 1.7)
f.person(760, 800, "stand", 1.7, flip=True)
f.bubble(620, 240, 300, 120, "kelishdik!", tail=(-30, 30), size=48)
f.clock(170, 300, 64); f.text(170, 420, "vaqt bor", 42, TEAL, rot=-4)
f.text(1000, 700, "+1 mijoz", 54, TEAL, rot=-6)
F["avto-2"].append(f)

# ---- 3-post: nega har kuni yozish va sayt kerak
f = Frame("Ish bor, lekin ko'rgan yo'q", 1)
f.person(260, 800, "press", 1.7)
f.browser(380, 300, 300, 220, "ish"); f.text(530, 420, "✓ ✓ ✓", 50, TEAL, font="Space Grotesk")
f.line("M760 180 V860", w=6, color=GREY)
f.person(960, 800, "think", 1.7, flip=True, face="flat")
f.text(960, 330, "kim bu?", 48, rot=4)
F["avto-3"] = [f]
f = Frame("Har kuni bitta yozuv", 2)
f.calendar(520, 180, 520, 430, marks=(4, 5, 7, 13, 14, 16, 17, 18))
f.person(300, 800, "phone", 1.7)
f.text(780, 700, "+1 har kuni", 56, TEAL, rot=-4)
F["avto-3"].append(f)
f = Frame("Bitta havola: hamma ish", 3)
f.person(240, 800, "phone", 1.6)
f.arrow("M330 560 Q480 420 600 430", head=(600, 430, 5))
f.browser(610, 150, 470, 340); f.folder(650, 250, 120, 90, "Loyihalar"); f.folder(800, 250, 120, 90, "Kundalik"); f.folder(950, 250, 110, 90, "Taqvim")
f.person(860, 870, "cheer", 1.2)
f.text(430, 360, "havola", 40, TEAL, rot=-8)
F["avto-3"].append(f)

for k, frames in F.items():
    for i, fr in enumerate(frames, 1):
        open(os.path.join(out, f"{k}-{i}.svg"), "w").write(fr.svg())
print("ok", sum(len(v) for v in F.values()), "kadr")
