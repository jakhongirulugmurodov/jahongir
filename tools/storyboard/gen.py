import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
from uztypo import typo_markup
# 6-panel hand-drawn storyboard for the "Nega yozib boraman" post
INK="#17211F"; T="#16A6A9"; SOFT="#9AD2D2"; DEEP="#0A4E50"; P="#0E7E80"
W,H=1800,1160; PW,PH=560,470; GX,GY=30,30; TOP=110
def person(x,y,s=1,arm="down",face="ok",flip=False):
    f=-1 if flip else 1
    hx,hy=x,y; r=26*s
    o=[f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="4"/>']
    # eyes
    o.append(f'<circle cx="{hx+f*8*s}" cy="{hy-4*s}" r="3" fill="{INK}"/><circle cx="{hx+f*-4*s}" cy="{hy-4*s}" r="3" fill="{INK}"/>')
    if face=="ok": o.append(f'<path d="M{hx-8*s} {hy+9*s} q{8*s} {7*s} {16*s} 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif face=="worry": o.append(f'<path d="M{hx-8*s} {hy+13*s} q{8*s} {-7*s} {16*s} 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M{hx+f*26*s} {hy-18*s} q6 10 0 16 q-6-6 0-16z" fill="{SOFT}" stroke="{INK}" stroke-width="2"/>')
    elif face=="wow": o.append(f'<circle cx="{hx}" cy="{hy+11*s}" r="{5*s}" fill="none" stroke="{INK}" stroke-width="3"/>')
    b=hy+r; o.append(f'<path d="M{hx} {b} L{hx} {b+80*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="M{hx} {b+80*s} L{hx-24*s} {b+140*s} M{hx} {b+80*s} L{hx+24*s} {b+140*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round" fill="none"/>')
    if arm=="down": o.append(f'<path d="M{hx} {b+20*s} L{hx-30*s} {b+65*s} M{hx} {b+20*s} L{hx+30*s} {b+65*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    elif arm=="phone": o.append(f'<path d="M{hx} {b+20*s} L{hx+f*34*s} {b+40*s} L{hx+f*30*s} {b+6*s} M{hx} {b+20*s} L{hx-f*26*s} {b+62*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round" fill="none"/><rect x="{hx+f*30*s-11}" y="{b-22*s}" width="22" height="36" rx="4" fill="{SOFT}" stroke="{INK}" stroke-width="3" transform="rotate({f*-12} {hx+f*30*s} {b})"/>')
    elif arm=="up": o.append(f'<path d="M{hx} {b+20*s} L{hx-34*s} {b-10*s} M{hx} {b+20*s} L{hx+34*s} {b-10*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    elif arm=="point": o.append(f'<path d="M{hx} {b+20*s} L{hx+f*52*s} {b+10*s} M{hx} {b+20*s} L{hx-f*26*s} {b+62*s}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    return "".join(o)
def bubble(x,y,w,h,txt,tail=(0,40),size=30,fill="#fff"):
    tx,ty=tail
    lines=txt.split("\n"); ls="".join(f'<tspan x="{x+w/2}" dy="{0 if i==0 else size*1.15}">{l}</tspan>' for i,l in enumerate(lines))
    return (f'<path d="M{x+20} {y} h{w-40} q20 0 20 20 v{h-40} q0 20 -20 20 h{-(w/2-40)+tx} l{-14} {ty} l{-6} {-ty} h{-(w/2-20)-tx} q-20 0 -20 -20 v{-(h-40)} q0 -20 20 -20z" fill="{fill}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<text x="{x+w/2}" y="{y+h/2-(len(lines)-1)*size*0.55+size*0.35}" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="{size}" fill="{INK}">{ls}</text>')
def panel(i,body,cap):
    c,r=i%3,i//3; x=GX+c*(PW+30); y=TOP+r*(PH+40)
    return (f'<g transform="translate({x},{y})"><g filter="url(#rough)"><rect x="0" y="0" width="{PW}" height="{PH-70}" rx="6" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<g>{body}</g></g>'
            f'<circle cx="34" cy="34" r="20" fill="{T}"/><text x="34" y="42" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="22" fill="#fff">{i+1}</text>'
            f'<text x="{PW/2}" y="{PH-28}" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="34" fill="{INK}">{cap}</text></g>')
p=[]
# 1: client asks
p.append(panel(0, person(150,150,1,"down","ok")+person(420,150,1,"point","ok",flip=True)+f'<rect x="200" y="300" width="170" height="16" rx="4" fill="{SOFT}" stroke="{INK}" stroke-width="3"/>'+bubble(250,30,280,90,'Oldin nima\nqilgansiz?',(-60,30),30),
  "Har safar shu savol"))
# 2: scrolling screenshots
shots="".join(f'<rect x="{x}" y="{y}" width="46" height="70" rx="5" fill="#fff" stroke="{INK}" stroke-width="3" transform="rotate({a} {x+23} {y+35})"/><path d="M{x+8} {y+20} h30 M{x+8} {y+32} h22" stroke="{SOFT}" stroke-width="4" transform="rotate({a} {x+23} {y+35})"/>' for x,y,a in [(300,40,-12),(370,90,8),(440,40,-4),(330,170,14),(430,170,-10),(380,250,6),(470,260,-16)])
p.append(panel(1, person(170,150,1,"phone","worry")+shots+bubble(40,20,200,70,"qayerda edi...?",(40,30),28),
  "Eng yaxshi ishlar esdan chiqardi"))
# 3: lightbulb
bulb=f'<g transform="translate(280,40)"><path d="M0 70 a50 50 0 1 1 60 0 v22 h-60z" fill="#E9F7F7" stroke="{INK}" stroke-width="4"/><path d="M6 104 h48 M10 116 h40" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M-40 10 l-22-12 M30 -30 v-22 M100 10 l22-12 M-36 60 h-22 M96 60 h22" stroke="{T}" stroke-width="5" stroke-linecap="round"/></g>'
p.append(panel(2, person(140,180,1,"up","wow")+bulb+bubble(250,215,290,120,'Yozilmagan ish =\nko\'rinmagan ish',(-90,24),32,fill="#E9F7F7"),
  "Shunda tushundim"))
# 4: calendar with pins + folder
cal=f'<g transform="translate(70,60)"><rect width="260" height="240" rx="10" fill="#fff" stroke="{INK}" stroke-width="4"/><rect width="260" height="44" rx="10" fill="{DEEP}"/><text x="130" y="31" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="22" fill="#fff">Oktabr</text>'
for r in range(4):
    for c in range(5):
        cal+=f'<rect x="{16+c*48}" y="{58+r*44}" width="38" height="34" rx="4" fill="none" stroke="{SOFT}" stroke-width="2.5"/>'
for c,r in [(0,1),(2,1),(3,2),(1,3),(4,0),(2,3),(4,2)]:
    cal+=f'<circle cx="{35+c*48}" cy="{75+r*44}" r="9" fill="{T}" stroke="{INK}" stroke-width="2"/>'
cal+='</g>'
fold=f'<g transform="translate(360,120)"><path d="M0 20 h50 l14 -16 h70 v150 h-134z" fill="{SOFT}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><rect x="14" y="40" width="106" height="100" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M28 64 h70 M28 84 h56 M28 104 h64" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M0 60 h134 v94 h-134z" fill="{SOFT}" fill-opacity=".85" stroke="{INK}" stroke-width="4"/></g>'
p.append(panel(3, cal+fold+f'<text x="427" y="96" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="28" fill="{P}">+1 har kuni</text>',
  "Har kuni bitta yozuv"))
# 5: voice -> bot -> post
wave="".join(f'<rect x="{60+i*14}" y="{170-h/2}" width="7" height="{h}" rx="3" fill="{T}"/>' for i,h in enumerate([20,44,30,62,38,70,26,50,34,18]))
phone=f'<rect x="40" y="70" width="170" height="200" rx="18" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="125" cy="236" r="16" fill="{DEEP}"/><rect x="119" y="226" width="12" height="18" rx="6" fill="#fff"/>'
bot=f'<g transform="translate(250,110)"><rect width="100" height="86" rx="20" fill="{SOFT}" stroke="{INK}" stroke-width="4"/><circle cx="34" cy="40" r="9" fill="{INK}"/><circle cx="66" cy="40" r="9" fill="{INK}"/><path d="M34 64 h32" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M50 0 v-18" stroke="{INK}" stroke-width="4"/><circle cx="50" cy="-22" r="7" fill="{T}" stroke="{INK}" stroke-width="3"/></g>'
page=f'<g transform="translate(400,80)"><rect width="120" height="160" rx="6" fill="#fff" stroke="{INK}" stroke-width="4"/><path d="M18 30 h84 M18 52 h70 M18 74 h80 M18 96 h56" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><path d="M30 126 l12 12 l26 -28" stroke="{T}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
arr=lambda x1,x2,y: f'<path d="M{x1} {y} C{x1+20} {y-20} {x2-20} {y-20} {x2} {y}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M{x2-12} {y-10} L{x2} {y} L{x2-14} {y+6}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
p.append(panel(4, phone+wave+bot+page+arr(215,245,160)+arr(355,395,160)+f'<text x="125" y="310" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="28" fill="{P}">1 daqiqa</text><text x="460" y="290" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="28" fill="{P}">tasdiqlayman</text>',
  "Keyingi qadam: ovozli xabar"))
# 6: growing stacks
st=""
for i,(lbl,n) in enumerate([("1 kun",1),("1 oy",6),("1 yil",16)]):
    x=70+i*160
    for k in range(n):
        st+=f'<rect x="{x+(k%2)*4}" y="{300-k*14}" width="110" height="18" rx="3" fill="{"#fff" if k%3 else SOFT}" stroke="{INK}" stroke-width="3"/>'
    st+=f'<text x="{x+55}" y="350" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="32" fill="{INK}">{lbl}</text>'
st+=f'<g transform="translate(400,40)"><circle cx="50" cy="0" r="0"/></g>'+bubble(200,30,220,70,"300+ yozuv",(60,26),34,fill="#E9F7F7")
p.append(panel(5, st, "Eng aniq portfolio shu"))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#C9DCDC"/></pattern></defs>
<rect width="{W}" height="{H}" fill="#F5F5F3"/><rect width="{W}" height="{H}" fill="url(#dots)"/>
<text x="{GX}" y="70" font-family="Space Grotesk" font-weight="700" font-size="44" fill="{INK}">Nega har kuni yozib boraman<tspan fill="{T}">.</tspan></text>
<text x="{W-GX}" y="70" text-anchor="end" font-family="Caveat" font-weight="700" font-size="34" fill="{P}">6 kadrda</text>
{"".join(p)}</svg>'''
svg=typo_markup(svg)
open("sb.svg","w").write(svg)
open("sb.html","w").write(f'<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{{margin:0}}</style></head><body>{svg}</body></html>')
