# "Doodle" storyboard uslubi: katak qog'oz, marker bilan chizilgan dinamik odamchalar
# (tanasi teal marker bilan bo'yalgan), oyoq ostida kulrang soya, harakat chiziqlari.
# Har element "chizilib" chiqadi: chiziqlar pathLength=1 + CSS animatsiya, bo'yoqlar sekin paydo bo'ladi.
# Loyiha: "Shaxsiy blog tizimi". Boshqa loyihalar boshqa uslubda bo'ladi.
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from uztypo import typo_markup

INK = "#17211F"; TEAL = "#0E7E80"; SOFT = "#9AD2D2"; DEEP = "#0A4E50"; GREY = "#9AA5A3"; PAPER = "#FBFBF8"; GRID = "#DDE7E6"
W, H = 1200, 900

class Frame:
    """Bitta kadr. add_* metodlari elementlarni chizish tartibida qo'shadi (har biriga kechikish)."""
    def __init__(self, caption, num):
        self.caption, self.num = caption, num
        self.parts = []; self.t = 0.35  # birinchi element kechikishi (s)

    def _d(self, dur):
        d = self.t; self.t += dur * 0.62; return d

    def line(self, d, w=5, color=INK, dur=0.45, extra=""):
        self.parts.append(f'<path class="l" d="{d}" pathLength="1" stroke="{color}" stroke-width="{w}" style="--d:{self._d(dur):.2f}s;--t:{dur}s" {extra}/>')

    def fill(self, d, color=TEAL, op=1, dur=0.35, extra=""):
        self.parts.append(f'<path class="f" d="{d}" fill="{color}" fill-opacity="{op}" style="--d:{self._d(dur):.2f}s" {extra}/>')

    def text(self, x, y, s, size=40, color=INK, anchor="middle", font="Caveat", weight=700, dur=0.5, rot=0):
        tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
        self.parts.append(f'<text class="w" x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{color}" text-anchor="{anchor}"{tr} style="--d:{self._d(dur):.2f}s">{s}</text>')

    def raw(self, svg, dur=0.4):
        self.parts.append(f'<g class="f" style="--d:{self._d(dur):.2f}s">{svg}</g>')

    # --- odamcha -------------------------------------------------------
    def person(self, x, y, pose="stand", s=1.0, flip=False, face="smile", fx=None):
        """x,y = oyoqlar orasidagi yer nuqtasi. pose: stand, worry, walk, run, point, cheer, think, phone, press, read."""
        P = POSES[pose]; k = -1 if flip else 1
        def pt(p):  # mahalliy (dx,dy) → global
            return (x + k * p[0] * s, y + p[1] * s)
        def path(pts):
            a = [pt(p) for p in pts]
            d = f"M{a[0][0]:.1f} {a[0][1]:.1f}"
            for i in range(1, len(a)):
                (x0, y0), (x1, y1) = a[i - 1], a[i]
                mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.06, (y0 + y1) / 2 - (x1 - x0) * 0.06
                d += f" Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}"
            return d
        # yer soyasi (kulrang shtrix)
        sw = 70 * s
        sh = " ".join(f"M{x - sw + i * 9 * s:.1f} {y + 8 * s + (i % 2) * 3:.1f} l{26 * s:.1f} {-3 * s:.1f}" for i in range(int(2 * sw / (9 * s)) - 2))
        self.line(sh, w=4 * s, color=GREY, dur=0.3, extra='stroke-opacity=".55" stroke-linecap="round"')
        neck, hip = P["neck"], P["hip"]
        # tana: teal marker (to'rtburchakka yaqin, egiluvchan)
        nx, ny = neck; hx, hy = hip
        ang = math.atan2(hy - ny, hx - nx); px, py = -math.sin(ang) * 15, math.cos(ang) * 15
        body = [(nx + px, ny + py + 4), (hx + px * 1.1, hy + py), (hx - px * 1.1, hy - py), (nx - px, ny - py + 4)]
        b = [pt(p) for p in body]
        self.fill(f"M{b[0][0]:.1f} {b[0][1]:.1f} L{b[1][0]:.1f} {b[1][1]:.1f} L{b[2][0]:.1f} {b[2][1]:.1f} L{b[3][0]:.1f} {b[3][1]:.1f}Z", TEAL, 0.9, extra=f'stroke="{TEAL}" stroke-opacity=".9" stroke-width="{9 * s:.1f}" stroke-linejoin="round"')
        # oyoqlar, tana chizig'i, qo'llar
        for leg in ("legL", "legR"):
            self.line(path([hip] + P[leg]), w=5.5 * s, dur=0.35)
            fx_, fy_ = pt(P[leg][-1]); self.line(f"M{fx_ - 9 * s * k:.1f} {fy_:.1f} q{9 * s * k:.1f} {-6 * s:.1f} {20 * s * k:.1f} 0", w=5 * s, dur=0.2)
        self.line(path([neck, hip]), w=5 * s, dur=0.3)
        for arm in ("armL", "armR"):
            self.line(path([P["sh"]] + P[arm]), w=5 * s, dur=0.35)
            ax, ay = pt(P[arm][-1]); self.line(f"M{ax:.1f} {ay:.1f} m-6 0 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0", w=4 * s, dur=0.15)
        # bosh va yuz
        hx_, hy_ = pt(P["head"]); r = 19 * s
        self.line(f"M{hx_ - r:.1f} {hy_:.1f} a{r} {r} 0 1 0 {2 * r:.1f} 0 a{r} {r} 0 1 0 {-2 * r:.1f} 0", w=5 * s, dur=0.35)
        e = 6 * s * k; fy = hy_ - 2 * s
        self.fill(f"M{hx_ + e - 2.5:.1f} {fy:.1f} a2.6 2.6 0 1 0 5 0 a2.6 2.6 0 1 0 -5 0", INK)
        self.fill(f"M{hx_ + e + 8 * k - 2.5:.1f} {fy:.1f} a2.6 2.6 0 1 0 5 0 a2.6 2.6 0 1 0 -5 0", INK)
        mx = hx_ + 7 * s * k; my = hy_ + 8 * s
        mouth = {"smile": f"M{mx - 6 * s:.1f} {my:.1f} q{6 * s:.1f} {6 * s:.1f} {12 * s:.1f} 0",
                 "sad": f"M{mx - 6 * s:.1f} {my + 4 * s:.1f} q{6 * s:.1f} {-6 * s:.1f} {12 * s:.1f} 0",
                 "open": f"M{mx - 4 * s:.1f} {my:.1f} a4 5 0 1 0 8 0 a4 5 0 1 0 -8 0",
                 "flat": f"M{mx - 5 * s:.1f} {my + 2 * s:.1f} h{10 * s:.1f}"}[face]
        self.line(mouth, w=3.5 * s, dur=0.2)
        # effektlar
        for f in (fx or P.get("fx", [])):
            self.effect(f, hx_, hy_, x, y, s, k)

    def effect(self, kind, hx, hy, x, y, s, k):
        if kind == "sweat":
            self.line(f"M{hx + 26 * s * k:.1f} {hy - 18 * s:.1f} q{6 * k} 10 0 16 q{-6 * k} -6 0 -16", w=3.5, color=TEAL, dur=0.2)
            self.line(f"M{hx - 30 * s * k:.1f} {hy - 26 * s:.1f} l{-10 * k} -8 M{hx - 34 * s * k:.1f} {hy - 10 * s:.1f} l-14 0", w=4, dur=0.2)
        elif kind == "shine":
            for a in (-60, -90, -120, -30, -150):
                r0, r1 = 34 * s, 48 * s; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                self.line(f"M{hx + ca * r0:.1f} {hy + sa * r0:.1f} L{hx + ca * r1:.1f} {hy + sa * r1:.1f}", w=4, dur=0.12)
        elif kind == "q":
            self.text(hx + 34 * s * k, hy - 34 * s, "?", size=int(54 * s), color=TEAL)
        elif kind == "swirl":
            self.line(f"M{hx:.1f} {hy - 34 * s:.1f} c-14 -6 -10 -22 4 -22 c16 0 18 18 2 22 c-10 2 -12 -10 -2 -10", w=3.5, dur=0.3)
        elif kind == "speed":
            for i in range(3):
                self.line(f"M{x - 46 * s * k:.1f} {y - (80 + i * 22) * s:.1f} l{-46 * s * k:.1f} 0", w=4, dur=0.12)
        elif kind == "puff":
            cx = x - 60 * s * k; cy = y - 6 * s
            self.line(f"M{cx:.1f} {cy:.1f} a10 10 0 0 1 14 -12 a12 12 0 0 1 22 2 a9 9 0 0 1 4 16 z", w=3.5, dur=0.25)
            self.line(f"M{cx - 30 * k:.1f} {cy - 4:.1f} a7 7 0 1 1 12 -4 a7 7 0 1 1 -12 4", w=3, dur=0.2)

    # --- narsalar ------------------------------------------------------
    def phone(self, x, y, s=1.0, screen=None, rot=0):
        w, h = 120 * s, 210 * s
        g = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
        self.parts.append(f'<g{g}>');
        self.fill(f"M{x + 4} {y + 4} h{w - 8} v{h - 8} h{-(w - 8)} z", "#fff")
        self.line(f"M{x + 16} {y} h{w - 32} q16 0 16 16 v{h - 32} q0 16 -16 16 h{-(w - 32)} q-16 0 -16 -16 v{-(h - 32)} q0 -16 16 -16 z", w=5)
        self.line(f"M{x + w / 2 - 14} {y + 14} h28", w=4, dur=0.1)
        if screen: screen(x, y, w, h)
        self.parts.append('</g>')

    def story_ring(self, cx, cy, r=26, label=None, color=TEAL):
        self.line(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", w=5, color=color, dur=0.3)
        self.fill(f"M{cx - r + 7} {cy} a{r - 7} {r - 7} 0 1 0 {2 * (r - 7)} 0 a{r - 7} {r - 7} 0 1 0 {-2 * (r - 7)} 0", SOFT, 0.9)
        if label: self.text(cx, cy + r + 30, label, size=26)

    def tg(self, cx, cy, s=1.0):
        r = 34 * s
        self.fill(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", SOFT)
        self.line(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", w=5, dur=0.3)
        self.line(f"M{cx - 18 * s} {cy + 2 * s} L{cx + 18 * s} {cy - 14 * s} L{cx + 10 * s} {cy + 18 * s} L{cx - 2 * s} {cy + 6 * s} Z M{cx - 2 * s} {cy + 6 * s} L{cx + 4 * s} {cy + 16 * s}", w=4, dur=0.3)

    def ig(self, cx, cy, s=1.0):
        a = 32 * s
        self.fill(f"M{cx - a + 12} {cy - a} h{2 * a - 24} q12 0 12 12 v{2 * a - 24} q0 12 -12 12 h{-(2 * a - 24)} q-12 0 -12 -12 v{-(2 * a - 24)} q0 -12 12 -12z", SOFT)
        self.line(f"M{cx - a + 14} {cy - a} h{2 * a - 28} q14 0 14 14 v{2 * a - 28} q0 14 -14 14 h{-(2 * a - 28)} q-14 0 -14 -14 v{-(2 * a - 28)} q0 -14 14 -14z", w=5, dur=0.3)
        self.line(f"M{cx - 13 * s} {cy} a{13 * s} {13 * s} 0 1 0 {26 * s} 0 a{13 * s} {13 * s} 0 1 0 {-26 * s} 0", w=4.5, dur=0.25)
        self.fill(f"M{cx + 17 * s} {cy - 19 * s} a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0", INK)

    def browser(self, x, y, w, h, title="jahongir.onagy.app"):
        self.fill(f"M{x} {y} h{w} v{h} h{-w} z", "#fff")
        self.line(f"M{x + 10} {y} h{w - 20} q10 0 10 10 v{h - 20} q0 10 -10 10 h{-(w - 20)} q-10 0 -10 -10 v{-(h - 20)} q0 -10 10 -10z", w=5, dur=0.4)
        self.line(f"M{x} {y + 44} h{w}", w=4, dur=0.2)
        for i in range(3): self.fill(f"M{x + 22 + i * 22} {y + 22} a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0", [GREY, SOFT, TEAL][i])
        self.text(x + w / 2 + 20, y + 31, title, size=24, color=GREY, font="Hanken Grotesk", weight=600)

    def arrow(self, d, w=5, color=INK, dashed=False, head=None):
        extra = 'stroke-dasharray="0"' if not dashed else ""
        self.line(d, w=w, color=color, dur=0.4)
        if head:
            (x, y, a) = head; L = 18
            p1 = (x - L * math.cos(math.radians(a - 28)), y - L * math.sin(math.radians(a - 28)))
            p2 = (x - L * math.cos(math.radians(a + 28)), y - L * math.sin(math.radians(a + 28)))
            self.line(f"M{p1[0]:.1f} {p1[1]:.1f} L{x} {y} L{p2[0]:.1f} {p2[1]:.1f}", w=w, color=color, dur=0.15)

    def bubble(self, x, y, w, h, s, tail=(-40, 26), size=34, fill="#fff"):
        tx, ty = tail
        self.fill(f"M{x} {y} h{w} v{h} h{-w} z", fill)
        self.line(f"M{x + 18} {y} h{w - 36} q18 0 18 18 v{h - 36} q0 18 -18 18 h{-(w / 2 - 18 + tx)} l{-10} {ty} l{-8} {-ty} h{-(w / 2 - 36 - tx - 18)} q-18 0 -18 -18 v{-(h - 36)} q0 -18 18 -18z", w=4.5, dur=0.4)
        lines = s.split("\n")
        for i, t in enumerate(lines):
            self.text(x + w / 2, y + h / 2 + (i - (len(lines) - 1) / 2) * size * 1.05 + size * 0.33, t, size=size)

    def clock(self, cx, cy, r=60):
        self.fill(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", "#fff")
        self.line(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", w=5, dur=0.35)
        self.line(f"M{cx} {cy} v{-r * 0.62} M{cx} {cy} l{r * 0.45} {r * 0.2}", w=6, dur=0.25)

    def lines(self, x, y, w, n=3, gap=26, color=SOFT):
        for i in range(n):
            ww = w * (1 - 0.18 * (i % 2)); self.fill(f"M{x} {y + i * gap} h{ww:.0f} v12 h{-ww:.0f} z", color, 1, dur=0.12)

    def pill(self, x, y, w, h, s, fill=TEAL, color="#fff", size=30):
        self.fill(f"M{x + h / 2} {y} h{w - h} a{h / 2} {h / 2} 0 0 1 0 {h} h{-(w - h)} a{h / 2} {h / 2} 0 0 1 0 {-h}z", fill)
        self.line(f"M{x + h / 2} {y} h{w - h} a{h / 2} {h / 2} 0 0 1 0 {h} h{-(w - h)} a{h / 2} {h / 2} 0 0 1 0 {-h}z", w=4, dur=0.25)
        self.text(x + w / 2, y + h / 2 + size * 0.36, s, size=size, color=color, font="Space Grotesk", weight=700)

    def box(self, x, y, w, h, fill="#fff", rot=0):
        g = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
        self.parts.append(f"<g{g}>"); self.fill(f"M{x} {y} h{w} v{h} h{-w} z", fill)
        self.line(f"M{x + 8} {y} h{w - 16} q8 0 8 8 v{h - 16} q0 8 -8 8 h{-(w - 16)} q-8 0 -8 -8 v{-(h - 16)} q0 -8 8 -8z", w=4.5, dur=0.3)
        self.parts.append("</g>")

    def folder(self, x, y, w, h, label):
        self.fill(f"M{x} {y + 14} h{w} v{h - 14} h{-w} z", SOFT)
        self.line(f"M{x} {y + h} V{y} h{w * 0.38} l14 14 H{x + w} V{y + h} Z", w=4.5, dur=0.3)
        self.text(x + w / 2, y + h + 34, label, size=28)

    # --- yig'ish -------------------------------------------------------
    def svg(self):
        grid = "".join(f'<path d="M{i} 0V{H}" />' for i in range(0, W + 1, 40)) + "".join(f'<path d="M0 {j}H{W}" />' for j in range(0, H + 1, 40))
        ribbon_w = max(300, len(self.caption) * 21 + 90); rx = (W - ribbon_w) / 2
        rib = (f'<g class="f" style="--d:0s"><path d="M{rx - 34} 52 l34 -8 v58 l-34 8 l14 -29z" fill="#E9F3F3" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M{rx + ribbon_w + 34} 52 l-34 -8 v58 l34 8 l-14 -29z" fill="#E9F3F3" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M{rx} 34 q{ribbon_w / 2} -10 {ribbon_w} 0 v66 q{-ribbon_w / 2} -10 {-ribbon_w} 0z" fill="#fff" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
               f'<text x="{W / 2}" y="82" font-family="Caveat" font-weight="700" font-size="42" fill="{INK}" text-anchor="middle">{self.caption}</text></g>'
               f'<g class="f" style="--d:0s"><circle cx="64" cy="66" r="26" fill="{TEAL}"/><text x="64" y="76" font-family="Space Grotesk" font-weight="700" font-size="28" fill="#fff" text-anchor="middle">{self.num}</text></g>')
        css = ("<style>.l{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:dr calc(var(--t,.45s)*var(--k,1)) ease-out forwards;animation-delay:calc(var(--d,0s)*var(--k,1))}"
               ".f,.w{opacity:0;animation:fi .35s ease-out forwards;animation-delay:calc(var(--d,0s)*var(--k,1))}"
               "@keyframes dr{to{stroke-dashoffset:0}}@keyframes fi{to{opacity:1}}"
               ".still .l{animation:none;stroke-dashoffset:0}.still .f,.still .w{animation:none;opacity:1}"
               "@media (prefers-reduced-motion:reduce){.l{animation:none;stroke-dashoffset:0}.f,.w{animation:none;opacity:1}}</style>")
        return typo_markup(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="dood" data-len="{min(self.t, 4.6):.2f}" style="--k:{min(1, 4.6 / self.t):.3f}">{css}'
                f'<rect width="{W}" height="{H}" fill="{PAPER}"/><g stroke="{GRID}" stroke-width="2">{grid}</g>'
                f'{rib}{"".join(self.parts)}</svg>')

# Pozalar: mahalliy koordinatalar (y yuqoriga manfiy). neck/hip — tana, sh — yelka, head — bosh markazi.
POSES = {
    "stand": dict(head=(0, -150), neck=(0, -128), hip=(0, -66), sh=(0, -118),
                  armL=[(-22, -86), (-30, -58)], armR=[(22, -86), (30, -58)], legL=[(-14, -32), (-22, 0)], legR=[(14, -32), (22, 0)]),
    "worry": dict(head=(0, -148), neck=(0, -126), hip=(2, -64), sh=(0, -116),
                  armL=[(-34, -136), (-14, -164)], armR=[(34, -136), (14, -164)], legL=[(-16, -32), (-26, 0)], legR=[(12, -30), (18, 0)], fx=["sweat"]),
    "walk": dict(head=(8, -150), neck=(5, -128), hip=(0, -66), sh=(5, -118),
                 armL=[(-12, -90), (-30, -70)], armR=[(22, -92), (36, -74)], legL=[(-14, -34), (-32, -2)], legR=[(16, -34), (26, 0)]),
    "run": dict(head=(26, -144), neck=(18, -124), hip=(0, -66), sh=(16, -114),
                armL=[(-14, -100), (-36, -116)], armR=[(40, -98), (58, -118)], legL=[(-30, -44), (-62, -40)], legR=[(26, -34), (14, 0)], fx=["speed", "puff"]),
    "point": dict(head=(0, -150), neck=(0, -128), hip=(0, -66), sh=(0, -118),
                  armL=[(-20, -86), (-28, -60)], armR=[(40, -122), (82, -128)], legL=[(-14, -32), (-22, 0)], legR=[(14, -32), (22, 0)]),
    "cheer": dict(head=(0, -168), neck=(0, -146), hip=(0, -84), sh=(0, -136), air=True,
                  armL=[(-30, -170), (-44, -204)], armR=[(30, -170), (44, -204)], legL=[(-24, -54), (-46, -30)], legR=[(24, -54), (46, -30)], fx=["shine"]),
    "think": dict(head=(2, -150), neck=(0, -128), hip=(0, -66), sh=(0, -118),
                  armL=[(-24, -90), (-6, -108)], armR=[(26, -98), (12, -138)], legL=[(-12, -32), (-20, 0)], legR=[(14, -32), (20, 0)], fx=["q"]),
    "phone": dict(head=(4, -148), neck=(0, -126), hip=(0, -64), sh=(0, -116),
                  armL=[(-16, -88), (16, -100)], armR=[(24, -92), (30, -104)], legL=[(-14, -32), (-22, 0)], legR=[(14, -32), (22, 0)]),
    "press": dict(head=(14, -146), neck=(8, -124), hip=(-4, -64), sh=(8, -114),
                  armL=[(-18, -90), (-26, -64)], armR=[(44, -104), (70, -88)], legL=[(-20, -32), (-32, 0)], legR=[(10, -32), (20, 0)]),
    "slump": dict(head=(16, -132), neck=(8, -116), hip=(-2, -60), sh=(8, -108),
                  armL=[(0, -78), (4, -46)], armR=[(22, -80), (28, -50)], legL=[(-14, -30), (-20, 0)], legR=[(14, -30), (20, 0)], fx=["swirl"]),
}
