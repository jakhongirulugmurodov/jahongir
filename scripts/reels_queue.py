# Reels navbati (@osish.nuqtasi). Videolar GitHub Release'da turadi, bu skript vaqti kelganini Instagram'ga joylaydi.
# Kunlik chiqish soni ZAXIRAGA qarab (Jahongir qoidasi): zaxira = navbatda kutayotganlar + Mac papkada tayyorlar.
#   1–20 → kuniga 1 ta (20:30) · 21–40 → 2 ta (13:00, 20:30) · 41+ → 3 ta (09:00, 13:00, 20:30)
# TRIGGER rejimi (22-10 tasdiqlangan, q['rejim']='trigger' — standart): oldingi reels o'sishdan to'xtashi bilan keyingisi chiqadi:
#   kamida 3 soat o‘tgan (22-10: sinov guruhi 1–2 soatda tugaydi) + oxirgi 2 soatda soatiga <5 ko'rish (content/reels-soatlik.json); soatlik o'lchov yo'q bo'lsa 12 soatda;
#   24 soatdan keyin baribir; kuniga ≤3 ta; 23:00–08:00 chiqmaydi; zaxira <7 bo'lsa oddiy jadvalga (kuniga 1 ta, 20:30) qaytadi.
# Vaqt sinovi (22-10 tasdiqlangan, trigger yoqilgach to'xtatildi): kuniga 1 ta bo'lganda 10 ta video kunma-kun 13:00 va 20:30 da almashib chiqadi
# (har biriga "sinov_soat" yoziladi); 10 tasi chiqqach faqat 20:30 qoladi.
# Barqarorlik (tasdiqlangan): son kun boshida qotiriladi va kun davomida o'zgarmaydi;
# pastga tushish kechikadi — 2 tadan 1 taga zaxira 15 dan kam bo'lganda, 3 tadan 2 taga 35 dan kam bo'lganda qaytadi.
# Istisno: kun 0 bilan boshlangan bo'lsa (zaxira bo'sh edi), video kelishi bilan o'sha kunning o'zida ko'tariladi.
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/reels-queue.json"
if not os.path.exists(Q): sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
papka = json.load(open("content/reels-papka.json")).get("papkada", []) if os.path.exists("content/reels-papka.json") else []
SLOTS = {1: [(20, 30)], 2: [(13, 0), (20, 30)], 3: [(9, 0), (13, 0), (20, 30)]}
TRIG = q.get("rejim", "trigger") == "trigger"
SINOV = 0 if TRIG else 10 - sum(1 for x in q["navbat"] if x.get("sinov_soat"))
def slots(n, day):
    if n == 1 and SINOV > 0: return [(13, 0)] if day.toordinal() % 2 == 0 else [(20, 30)]
    return SLOTS.get(n, [])
def kvota(z, oldingi=0):
    n = 3 if z >= 41 else 2 if z >= 21 else 1 if z >= 1 else 0
    if z >= 1:
        if oldingi >= 3 and z >= 35: n = max(n, 3)
        if oldingi >= 2 and z >= 15: n = max(n, 2)
    return n
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
zaxira = len(kut) + len(papka)
old = q.get("kunlik", {}); bugun_s = now.date().isoformat()
if old.get("kun") == bugun_s:
    n = old.get("kuniga", 0)
    if n == 0 and zaxira: n = kvota(zaxira, old.get("oldingi", 0))
else:
    n = kvota(zaxira, old.get("kuniga", 0))
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ).date() == now.date()]
due = [now.replace(hour=h, minute=m, second=0, microsecond=0) for h, m in slots(n, now.date())]
kerak = sum(1 for t in due if t <= now) - len(bugun)
SOAT = json.load(open("content/reels-soatlik.json")) if os.path.exists("content/reels-soatlik.json") else {}
chiq = [x for x in q["navbat"] if x.get("holat") == "chiqdi" and x.get("natija", {}).get("vaqt")]
oxirgi = max(chiq, key=lambda x: datetime.fromisoformat(x["natija"]["vaqt"])) if chiq else None
def trigger_kerak():
    if now.hour < 8 or now.hour >= 23 or len(bugun) >= 3: return 0, "tun (23–08) yoki kunlik 3 ta"
    if not oxirgi: return 1, "birinchi video"
    h = (now - datetime.fromisoformat(oxirgi["natija"]["vaqt"])).total_seconds() / 3600
    if h < 3: return 0, f"oxirgisiga {h:.1f} soat"
    if h >= 24: return 1, "24 soat o'tdi"
    rows = SOAT.get(oxirgi.get("media_id") or "", {}).get("olchov", [])
    if len(rows) < 3: return (1, "o'lchov yo'q, 12 soat o'tdi") if h >= 12 else (0, "o'lchov kam")
    a, b, c = [r.get("views", 0) for r in rows[-3:]]
    return (1, f"to'xtadi: +{b - a}, +{c - b}") if (b - a) < 5 and (c - b) < 5 else (0, f"o'syapti: +{b - a}, +{c - b}")
TRIG_ON = TRIG and zaxira >= 7
if TRIG_ON: kerak, sabab = trigger_kerak(); print("trigger:", sabab)
q["kunlik"] = {"rejim": "trigger" if TRIG_ON else "jadval", "zaxira": zaxira, "kuniga": n, "kun": bugun_s, "oldingi": old.get("oldingi", 0) if old.get("kun") == bugun_s else old.get("kuniga", 0), "yangilandi": now.isoformat(timespec="minutes")}
def joyla(x):
    os.makedirs("/tmp/reel", exist_ok=True)
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    open("/tmp/reel/cap.txt", "w").write(x["izoh"])
    env = {**os.environ, "IG_USER_TAGS": ",".join(x.get("teglar", []))}  # navbat elementidagi "teglar": ["hasankhoja"]
    r = subprocess.run(["python3", "scripts/ig_reel.py", url, "/tmp/reel/cap.txt"], capture_output=True, text=True, env=env)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
darhol = [x for x in kut if x.get("darhol")]  # qo'lda "darhol": true qo'yilgani jadvalni kutmaydi (masalan, test)
if darhol:
    joyla(darhol[0]); darhol[0].pop("darhol", None); kerak = 0
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
elif kerak > 0 and kut:
    joyla(kut[0])  # bir ishga tushishda ko'pi bilan 1 ta
    if n == 1 and SINOV > 0: kut[0]["sinov_soat"] = "%02d:%02d" % slots(n, now.date())[0]
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
# taxminiy jadval (trigger): har ~10 soatda bittadan, tungi 00–08 soat o'tkazib yuboriladi (aniq vaqtni o'sish hal qiladi)
if TRIG_ON:
    t = max(now, datetime.fromisoformat(oxirgi["natija"]["vaqt"]) + timedelta(hours=10)) if oxirgi else now
    for x in kut:
        if t.hour >= 23: t = (t + timedelta(days=1)).replace(hour=8, minute=0)
        elif t.hour < 8: t = t.replace(hour=8, minute=0)
        x["vaqt"] = t.isoformat(timespec="minutes"); t += timedelta(hours=10)
    kut = []
# taxminiy jadval: qolganlarni kvota bo'yicha keyingi slotlarga taqsimlash
t = now; i = 0; posted_today = len(bugun) + (1 if kerak > 0 else 0)
day = now.date(); used = posted_today
while i < len(kut) and n:
    sl = slots(n, day)
    for h, mi in sl:
        s = datetime(day.year, day.month, day.day, h, mi, tzinfo=TZ)
        if s <= now or (day == now.date() and used > 0 and sl.index((h, mi)) < used): continue
        if i >= len(kut): break
        kut[i]["vaqt"] = s.isoformat(timespec="minutes"); i += 1
    day = day + timedelta(days=1); used = 0
print(f"zaxira {zaxira}, kuniga {n}, bugun chiqqan {len(bugun)}, hozir kerak {max(kerak,0)}")
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
