# "Rangli qalam" uslubi — O‘sish Nuqtasi loyihasi (boshqa loyihalarda ishlatilmaydi).
# Daftar varag'i (krem qog'oz, och ko'k chiziqlar, qizil hoshiya), rangli qalam shtrixli bo'yoq,
# yumaloq qahramon (marjon rang kofta), kadr yuqorisida "skotch" lenta. Shriftlar: Fraunces + Patrick Hand.
# Chizish animatsiyasi doodle.Frame mexanizmidan (pathLength + CSS) foydalanadi.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodle import Frame
from uztypo import typo_markup
INK = "#22304A"; CORAL = "#EE6A4C"; MUST = "#F4B740"; LEAF = "#5BAE7E"; SKY = "#8CC3E8"; CREAM = "#FFF6E6"; LINE = "#DCE6F2"; MARGIN = "#F2A3A3"; SKIN = "#FBE3CC"
W, H = 1200, 900
H_ = lambda c: f"url(#h-{c})"   # shtrixli bo'yoq
def defs():
    pats = "".join(f'<pattern id="h-{n}" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate({a})"><rect width="9" height="9" fill="{c}" fill-opacity=".55"/><path d="M0 0V9" stroke="{c}" stroke-width="4.2" stroke-opacity=".95"/></pattern>'
                   for n, c, a in [("coral", CORAL, 35), ("must", MUST, -30), ("leaf", LEAF, 40), ("sky", SKY, -40), ("ink", INK, 30)])
    return f'<defs>{pats}<filter id="pen"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></defs>'
CSS = ("<style>.l{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:dr calc(var(--t,.45s)*var(--k,1)) ease-out forwards;animation-delay:calc(var(--d,0s)*var(--k,1))}"
       ".f,.w{opacity:0;animation:fi .35s ease-out forwards;animation-delay:calc(var(--d,0s)*var(--k,1))}@keyframes dr{to{stroke-dashoffset:0}}@keyframes fi{to{opacity:1}}"
       ".still .l{animation:none;stroke-dashoffset:0}.still .f,.still .w{animation:none;opacity:1}"
       "@media (prefers-reduced-motion:reduce){.l{animation:none;stroke-dashoffset:0}.f,.w{animation:none;opacity:1}}</style>")
def paper(w, h, margin=True):
    o = f'<rect width="{w}" height="{h}" fill="{CREAM}"/><g stroke="{LINE}" stroke-width="2.2">' + "".join(f'<path d="M0 {y}H{w}"/>' for y in range(60, h, 46)) + "</g>"
    if margin: o += f'<path d="M92 0V{h}" stroke="{MARGIN}" stroke-width="3"/>'
    return o

class Marker(Frame):
    def svg(self, still=False):
        tw = max(340, len(self.caption) * 20 + 90); tape = (f'<g class="f" style="--d:0s"><path d="M{W/2-tw/2} 26 l{tw} -6 l6 58 l{-tw} 8z" fill="{MUST}" fill-opacity=".75" stroke="{INK}" stroke-width="2.5" stroke-opacity=".4"/>'
                f'<text x="{W/2}" y="70" font-family="Patrick Hand" font-size="40" fill="{INK}" text-anchor="middle">{self.caption}</text></g>'
                f'<g class="f" style="--d:0s"><circle cx="70" cy="62" r="30" fill="{CORAL}"/><text x="70" y="74" font-family="Fraunces" font-weight="900" font-size="32" fill="#fff" text-anchor="middle">{self.num}</text></g>')
        return typo_markup(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="dood{" still" if still else ""}" data-len="{min(self.t, 4.6):.2f}" style="--k:{min(1, 4.6 / self.t):.3f}">{CSS}{defs()}'
                           f'{paper(W, H, False)}{tape}<g filter="url(#pen)">{"".join(self.parts)}</g></svg>')
    # --- matn
    ns = 1.0
    def note(self, x, y, s, size=40, color=INK, anchor="middle", rot=0):
        self.text(x, y, s, int(size * self.ns), color, anchor=anchor, font="Patrick Hand", weight=400, rot=rot)
    def big(self, x, y, s, size=60, color=INK, anchor="middle"):
        self.text(x, y, s, size, color, anchor=anchor, font="Fraunces", weight=900)
    # --- qahramon
    def hero(self, x, y, pose="stand", s=1.0, flip=False, face="smile", shirt="coral"):
        k = -1 if flip else 1
        P = lambda dx, dy: (x + k * dx * s, y + dy * s)
        def L(*pts, w=6):
            a = [P(*p) for p in pts]; self.line("M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in a), w=w * s, dur=0.3)
        # soya
        self.fill(f"M{x - 70 * s} {y + 6 * s} a{70 * s} {12 * s} 0 1 0 {140 * s} 0 a{70 * s} {12 * s} 0 1 0 {-140 * s} 0", INK, 0.12)
        # oyoqlar
        L((-16, -70), (-22, 0)); L((16, -70), (24, 0))
        self.line(f"M{P(-22,0)[0]-12*s*k:.1f} {y:.1f} h{24*s*k:.1f} M{P(24,0)[0]-6*s*k:.1f} {y:.1f} h{24*s*k:.1f}", w=8 * s, dur=0.15)
        # tana (kofta)
        bx, by = P(0, -150)
        tw, th = 50 * s, 86 * s
        d = f"M{x - tw:.1f} {y - 64 * s:.1f} Q{x - tw - 4 * s:.1f} {by:.1f} {x - 18 * s:.1f} {by - 6 * s:.1f} L{x + 18 * s:.1f} {by - 6 * s:.1f} Q{x + tw + 4 * s:.1f} {by:.1f} {x + tw:.1f} {y - 64 * s:.1f} Z"
        self.fill(d, H_(shirt)); self.line(d, w=5 * s, dur=0.35)
        # qo'llar
        arms = {"stand": [((-40, -136), (-56, -86)), ((40, -136), (56, -86))],
                "think": [((-40, -136), (-50, -86)), ((40, -136), (30, -110), (8, -168))],
                "shrug": [((-40, -136), (-80, -130), (-92, -168)), ((40, -136), (80, -130), (92, -168))],
                "point": [((-40, -136), (-52, -86)), ((40, -136), (110, -150))],
                "happy": [((-40, -136), (-70, -190), (-78, -226)), ((40, -136), (70, -190), (78, -226))],
                "worry": [((-40, -136), (-40, -196), (-20, -214)), ((40, -136), (40, -196), (20, -214))],
                "phone": [((-40, -136), (-30, -96), (10, -116)), ((40, -136), (36, -100), (18, -118))]}[pose]
        for a in arms:
            L(*a, w=6); ex, ey = P(*a[-1]); self.fill(f"M{ex - 7 * s} {ey} a{7 * s} {7 * s} 0 1 0 {14 * s} 0 a{7 * s} {7 * s} 0 1 0 {-14 * s} 0", SKIN)
        # bosh
        hx, hy = P(0, -196); r = 38 * s
        self.fill(f"M{hx - r} {hy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", SKIN)
        self.line(f"M{hx - r} {hy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", w=5 * s, dur=0.3)
        self.fill(f"M{hx - r - 2} {hy - 4 * s} Q{hx - r} {hy - r - 14 * s} {hx} {hy - r - 6 * s} Q{hx + r} {hy - r - 14 * s} {hx + r + 2} {hy - 4 * s} Q{hx + 10 * s} {hy - 26 * s} {hx - r - 2} {hy - 4 * s}Z", INK)
        ex = 13 * s
        for dx in (-ex, ex): self.fill(f"M{hx + dx - 4} {hy + 4 * s} a4 4.5 0 1 0 8 0 a4 4.5 0 1 0 -8 0", INK)
        mouth = {"smile": f"M{hx - 11 * s} {hy + 17 * s} q{11 * s} {11 * s} {22 * s} 0", "sad": f"M{hx - 11 * s} {hy + 24 * s} q{11 * s} {-9 * s} {22 * s} 0",
                 "open": f"M{hx - 7 * s} {hy + 20 * s} a7 8 0 1 0 14 0 a7 8 0 1 0 -14 0", "flat": f"M{hx - 9 * s} {hy + 21 * s} h{18 * s}"}[face]
        self.line(mouth, w=4 * s, dur=0.15)
        self.fill(f"M{hx - 26 * s} {hy + 12 * s} a7 5 0 1 0 14 0 a7 5 0 1 0 -14 0 M{hx + 12 * s} {hy + 12 * s} a7 5 0 1 0 14 0 a7 5 0 1 0 -14 0", CORAL, 0.35)
        if pose == "think": self.note(hx + 70 * s * k, hy - 40 * s, "?", int(70 * s), CORAL)
        if pose == "worry": self.line(f"M{hx + 46 * s} {hy - 30 * s} q8 14 0 22 q-8 -8 0 -22", w=4, color=SKY, dur=0.2)
        if pose == "happy":
            for a in (-50, -90, -130): self.line(f"M{hx + math.cos(math.radians(a)) * 56 * s:.1f} {hy + math.sin(math.radians(a)) * 56 * s:.1f} l{math.cos(math.radians(a)) * 18 * s:.1f} {math.sin(math.radians(a)) * 18 * s:.1f}", w=5, color=MUST, dur=0.1)
    # --- narsalar
    def rect(self, x, y, w, h, fill="#fff", r=14, lw=5):
        d = f"M{x + r} {y} h{w - 2 * r} q{r} 0 {r} {r} v{h - 2 * r} q0 {r} {-r} {r} h{-(w - 2 * r)} q{-r} 0 {-r} {-r} v{-(h - 2 * r)} q0 {-r} {r} {-r}z"
        if fill: self.fill(d, fill)
        self.line(d, w=lw, dur=0.35)
    def shop(self, x, y, w=460, h=420, sign="OCHIQ"):
        self.rect(x, y + 70, w, h - 70, "#fff", 6)
        for i in range(6):  # ayvon chiziqlari
            c = H_("coral") if i % 2 == 0 else "#fff"
            d = f"M{x - 20 + i * (w + 40) / 6:.1f} {y} h{(w + 40) / 6:.1f} l-8 80 h{-(w + 40) / 6 + 16:.1f} z"; self.fill(d, c); self.line(d, w=4, dur=0.1)
        self.rect(x + 40, y + 140, 180, 200, H_("sky"), 6); self.rect(x + 260, y + 140, 160, h - 140, "#fff", 6)
        self.rect(x + 300, y + 170, 90, 44, MUST, 8, 3); self.note(x + 345, y + 201, sign, 26)
        self.line(f"M{x + 60} {y + 160} l40 40 M{x + 70} {y + 280} l60 -60", w=4, color="#fff", dur=0.1)
    def bill(self, x, y, txt, rot=-8, w=200, h=110, fill="#fff"):
        self.parts.append(f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'); self.rect(x, y, w, h, fill, 8, 4)
        self.note(x + w / 2, y + 48, txt, 34); self.line(f"M{x + 30} {y + 76} h{w - 60}", w=3, color=CORAL, dur=0.1); self.parts.append("</g>")
    def card(self, x, y, w, h, txt, fill=None, size=38, rot=0):
        self.parts.append(f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'); self.rect(x, y, w, h, fill or "#fff", 12, 4.5)
        ls = txt.split("\n")
        for i, t in enumerate(ls): self.note(x + w / 2, y + h / 2 + (i - (len(ls) - 1) / 2) * size * 1.1 + size * 0.34, t, size)
        self.parts.append("</g>")
    def phone(self, x, y, w=230, h=420):
        self.rect(x, y, w, h, "#fff", 30, 6); self.line(f"M{x + w / 2 - 22} {y + 20} h44", w=5, dur=0.1)
    def mic(self, x, y, s=1):
        self.rect(x - 40 * s, y - 120 * s, 80 * s, 130 * s, H_("ink"), 40 * s, 5)
        self.line(f"M{x - 62 * s} {y - 40 * s} q0 80 {62 * s} 80 q{62 * s} 0 {62 * s} -80 M{x} {y + 40 * s} v{40 * s} M{x - 40 * s} {y + 80 * s} h{80 * s}", w=6)
    def arrow(self, x1, y1, x2, y2, color=INK, w=6):
        a = math.atan2(y2 - y1, x2 - x1); L = 22
        self.line(f"M{x1} {y1} Q{(x1 + x2) / 2} {(y1 + y2) / 2 - 30} {x2} {y2}", w=w, color=color, dur=0.3)
        self.line(f"M{x2 - L * math.cos(a - .5):.1f} {y2 - L * math.sin(a - .5):.1f} L{x2} {y2} L{x2 - L * math.cos(a + .5):.1f} {y2 - L * math.sin(a + .5):.1f}", w=w, color=color, dur=0.1)
    def bubble(self, x, y, w, h, txt, tail=(-40, 30), size=40, fill="#fff"):
        tx, ty = tail
        d = f"M{x + 22} {y} h{w - 44} q22 0 22 22 v{h - 44} q0 22 -22 22 h{-(w / 2 - 22 + tx)} l-12 {ty} l-10 {-ty} h{-(w / 2 - 44 - tx - 22)} q-22 0 -22 -22 v{-(h - 44)} q0 -22 22 -22z"
        self.fill(d, fill); self.line(d, w=4.5, dur=0.3)
        ls = txt.split("\n")
        for i, t in enumerate(ls): self.note(x + w / 2, y + h / 2 + (i - (len(ls) - 1) / 2) * size * 1.05 + size * 0.33, t, size)
    def dots(self, x, y, cols, rows, gap=34, r=10, filled=None, color="coral"):
        n = 0
        for j in range(rows):
            for i in range(cols):
                cx, cy = x + i * gap, y + j * gap
                c = H_(color) if (filled is None or n < filled) else "#fff"
                self.fill(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", c); n += 1
