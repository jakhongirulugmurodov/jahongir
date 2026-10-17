from sblib import *
robot=lambda x,y,s=1: f'<g transform="translate({x},{y}) scale({s})"><path d="M50 0 v-18" stroke="{INK}" stroke-width="4"/><circle cx="50" cy="-22" r="7" fill="{T}" stroke="{INK}" stroke-width="3"/><rect width="100" height="86" rx="20" fill="{SOFT}" stroke="{INK}" stroke-width="4"/><circle cx="34" cy="40" r="9" fill="{INK}"/><circle cx="66" cy="40" r="9" fill="{INK}"/><path d="M34 64 q16 10 32 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/><rect x="20" y="90" width="60" height="70" rx="12" fill="{SOFT}" stroke="{INK}" stroke-width="4"/></g>'
def offer(l1,l2,btn):
    return (f'<rect x="8" y="8" width="{PW-16}" height="{PH-86}" rx="4" fill="{DEEP}"/>'
            f'<text x="{PW/2}" y="130" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="34" fill="#fff">{l1}</text>'
            f'<text x="{PW/2}" y="176" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="34" fill="#fff">{l2}</text>'
            f'<text x="{PW/2}" y="262" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="34" fill="{SOFT}">pastdagi tugmani bosing</text>'
            f'<path d="M{PW/2} 284 v34 m-14 -14 l14 14 l14 -14" fill="none" stroke="{SOFT}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{PW-60}" cy="70" r="16" fill="{T}"/>')
def msgs(x,y,n,w=200,hi=None):
    o=""
    for i in range(n):
        ww=w-(i*37%70)
        if i==hi: o+=f'<rect x="{x}" y="{y+i*30-4}" width="{w}" height="30" rx="15" fill="#fff" stroke="{T}" stroke-width="4"/><text x="{x+16}" y="{y+i*30+17}" font-family="Caveat" font-weight="700" font-size="24" fill="{DEEP}">SMM kerak! narxi qancha?</text>'
        else: o+=f'<rect x="{x+(i%2)*30}" y="{y+i*30}" width="{ww}" height="22" rx="11" fill="{"#fff" if i%3 else SOFT}" stroke="{INK}" stroke-width="2.5"/>'
    return o
# ---------- post 1 (6 frames)
p=[]
p.append(panel(0, f'<g transform="translate(80,40)"><rect width="400" height="320" rx="14" fill="#fff" stroke="{INK}" stroke-width="4"/><rect width="400" height="46" rx="14" fill="{DEEP}"/><text x="200" y="31" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="20" fill="#fff">Telegram guruh</text>{msgs(24,66,8,330,hi=4)}</g>', "Mijoz guruhda yozdi"))
clock=f'<g transform="translate(320,60)"><circle cx="90" cy="90" r="85" fill="#fff" stroke="{INK}" stroke-width="5"/><path d="M90 90 V30 M90 90 L140 110" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="90" cy="90" r="8" fill="{T}"/></g>'
p.append(panel(1, person(150,150,1,"down","worry")+clock+bubble(300,270,220,70,"3 soat o'tdi...",(-60,22),30,fill="#E9F7F7"), "Siz kech ko'rdingiz"))
hand=person(170,150,1,"point","ok")+person(390,150,1,"point","ok",flip=True)+f'<circle cx="280" cy="208" r="16" fill="{SOFT}" stroke="{INK}" stroke-width="3"/>'+bubble(300,30,230,70,"kelishdik!",(-40,24),32)+f'<text x="70" y="70" font-family="Caveat" font-weight="700" font-size="28" fill="#9AA8A6">raqobatchingiz</text>'
p.append(panel(2, hand, "U boshqasini topib bo'ldi"))
fil=f'<path d="M300 90 h200 l-70 90 v90 l-60 30 v-120z" fill="#E9F7F7" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><rect x="320" y="30" width="150" height="22" rx="11" fill="#fff" stroke="{INK}" stroke-width="2.5"/><rect x="345" y="60" width="120" height="22" rx="11" fill="{SOFT}" stroke="{INK}" stroke-width="2.5"/><rect x="350" y="320" width="100" height="26" rx="13" fill="{T}" stroke="{INK}" stroke-width="3"/><text x="400" y="340" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="24" fill="#fff">mijoz ✓</text><text x="470" y="262" font-family="Caveat" font-weight="700" font-size="26" fill="#9AA8A6">spam ✗</text>'
p.append(panel(3, robot(80,110)+fil, "AI har xabarni o'qiydi"))
notif=f'<g transform="translate(60,50)"><rect width="270" height="96" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/><text x="20" y="40" font-family="Space Grotesk" font-weight="700" font-size="22" fill="{INK}">🔥 Issiq mijoz</text><text x="20" y="74" font-family="Caveat" font-weight="700" font-size="24" fill="{P}">1,5 soatda topildi</text></g>'
stack="".join(f'<rect x="{360+(k%2)*4}" y="{330-k*14}" width="130" height="18" rx="3" fill="{"#fff" if k%3 else SOFT}" stroke="{INK}" stroke-width="3"/>' for k in range(16))
p.append(panel(4, notif+stack+bubble(60,200,250,110,"3 haftada\n300 ga yaqin",(60,24),34,fill="#E9F7F7"), "Sotuvchisiz, 3 haftada"))
p.append(panel(5, offer("Sizning guruhlaringizda","ham ishlaydi","Telegram'da yozing"), "Sizga ham qurib beramiz"))
render("Guruhda mijoz yozadi, siz ko'rmay qolasiz","AI sotuvchi",p,"v1.html")
# ---------- post 2 (3 frames)
ig=lambda x,y,s=1: f'<g transform="translate({x},{y}) scale({s})"><rect width="110" height="110" rx="30" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="55" cy="55" r="24" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="84" cy="26" r="6" fill="{T}"/></g>'
post=f'<g transform="translate(90,40)"><rect width="260" height="320" rx="14" fill="#fff" stroke="{INK}" stroke-width="4"/><rect x="16" y="16" width="228" height="170" rx="8" fill="{SOFT}"/><rect x="16" y="210" width="228" height="40" rx="20" fill="#fff" stroke="{T}" stroke-width="4"/><text x="34" y="237" font-family="Caveat" font-weight="700" font-size="26" fill="{DEEP}">narxi qancha?</text><path d="M30 280 h140 M30 300 h100" stroke="{SOFT}" stroke-width="5" stroke-linecap="round"/></g>'
moon=f'<g transform="translate(400,70)"><path d="M60 0 a60 60 0 1 0 50 90 a48 48 0 1 1 -50 -90z" fill="#E9F7F7" stroke="{INK}" stroke-width="4"/></g><text x="400" y="250" font-family="Caveat" font-weight="700" font-size="30" fill="{P}">javob yo\'q...</text>'
p=[panel(0, post+moon, "Savol javobsiz qoldi")]
p.append(panel(1, robot(70,110)+ig(400,60,.8)+bubble(200,190,320,120,"Assalomu alaykum!\nDirect'ga yozdim",(-110,24),30,fill="#E9F7F7")+f'<text x="230" y="90" font-family="Caveat" font-weight="700" font-size="30" fill="{T}">darhol</text>', "Agent darhol javob beradi"))
p.append(panel(2, offer("Instagram'ingizni","ham ulaymiz","Telegram'da yozing"), "Sizga ham ulab beramiz"))
render("Instagram'da so'rashdi, siz kech ko'rdingizmi","AI sotuvchi",p,"v2.html")
# ---------- post 3 (3 frames)
comp=person(420,150,1,"down","ok",flip=True)+f'<text x="360" y="360" font-family="Caveat" font-weight="700" font-size="28" fill="#9AA8A6">raqobatchingiz</text>'
p=[panel(0, robot(60,110)+comp+bubble(150,30,260,80,"xizmat kerakmi?",(60,24),30)+f'<text x="230" y="250" font-family="Space Grotesk" font-weight="700" font-size="60" fill="#9AA8A6">✗</text>', "Noto'g'ri odamga yozish xavfi")]
cards="".join(f'<g transform="translate({50+(i%4)*24},{60+i*26}) rotate({(-6+i*3)})"><rect width="190" height="66" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M16 24 h110 M16 44 h70" stroke="{SOFT}" stroke-width="5" stroke-linecap="round"/></g>' for i in range(5))
p.append(panel(1, cards+f'<g transform="translate(320,80)"><rect width="200" height="96" rx="14" fill="#E9F7F7" stroke="{INK}" stroke-width="4"/><text x="100" y="64" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="44" fill="{DEEP}">121</text></g><text x="330" y="240" font-family="Caveat" font-weight="700" font-size="30" fill="{T}">✓ yozish kerak</text><text x="330" y="285" font-family="Caveat" font-weight="700" font-size="30" fill="#9AA8A6">✗ kerak emas</text>', "121 ta suhbatdan o'rgandi"))
p.append(panel(2, offer("Sizning xizmatlaringizga","moslab o'qitamiz","Telegram'da yozing"), "Sizga moslab beramiz"))
render("AI noto'g'ri odamga yozmasin","AI sotuvchi",p,"v3.html")
