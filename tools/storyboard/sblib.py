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

def render(title,right,panels,out):
    p=panels
    rows=(len(p)+2)//3; HH=TOP+rows*(PH+40)+10
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}">
<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#C9DCDC"/></pattern></defs>
<rect width="{W}" height="{HH}" fill="#F5F5F3"/><rect width="{W}" height="{HH}" fill="url(#dots)"/>
<text x="{GX}" y="70" font-family="Space Grotesk" font-weight="700" font-size="44" fill="{INK}">{title}<tspan fill="{T}">.</tspan></text>
<text x="{W-GX}" y="70" text-anchor="end" font-family="Caveat" font-weight="700" font-size="34" fill="{P}">{right}</text>
{"".join(p)}</svg>'''
    svg=typo_markup(svg)
    open(out,"w").write(f'<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?x"><style>body{{margin:0}}</style></head><body>{svg}</body></html>')
