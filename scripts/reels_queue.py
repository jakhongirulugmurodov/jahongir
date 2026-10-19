# Reels navbati (@osish.nuqtasi). Videolar GitHub Release'da turadi, bu skript vaqti kelganini yuklab olib Instagram'ga joylaydi.
# Kunlik chiqish soni ZAXIRAGA qarab o'zgaradi (Jahongir qoidasi): zaxira = navbatda kutayotganlar + Mac papkada tayyorlar.
#   zaxira 10–20  → kuniga 1 ta (14:00)
#   zaxira 21–40  → kuniga 2 ta (10:00, 19:00)
#   zaxira 41+    → kuniga 3 ta (09:00, 14:00, 20:00)
# Maqsad: doim ~10 kunlik zaxira qolsin, montaj partiyalab kelsa ham sahifa jim qolmasin.
# Har ishga tushishda kutayotganlarning taxminiy chiqish vaqti ham qayta hisoblanadi (panel uchun).
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/reels-queue.json"
if not os.path.exists(Q): sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
papka = json.load(open("content/reels-papka.json")).get("papkada", []) if os.path.exists("content/reels-papka.json") else []
SLOTS = {1: [(14, 0)], 2: [(10, 0), (19, 0)], 3: [(9, 0), (14, 0), (20, 0)]}
def kvota(z): return 3 if z >= 41 else 2 if z >= 21 else 1 if z >= 1 else 0
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
zaxira = len(kut) + len(papka); n = kvota(zaxira)
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ).date() == now.date()]
due = [now.replace(hour=h, minute=m, second=0, microsecond=0) for h, m in SLOTS.get(n, [])]
kerak = sum(1 for t in due if t <= now) - len(bugun)
q["kunlik"] = {"zaxira": zaxira, "kuniga": n, "yangilandi": now.isoformat(timespec="minutes")}
def joyla(x):
    os.makedirs("/tmp/reel", exist_ok=True)
    d = subprocess.run(["gh", "release", "download", x["release"], "-p", x["fayl"], "-D", "/tmp/reel", "--clobber"], capture_output=True, text=True)
    if d.returncode:
        x["holat"] = "xato"; x["natija"] = {"vaqt": now.isoformat(timespec="minutes"), "xato": "yuklab olinmadi"}; return
    open("/tmp/reel/cap.txt", "w").write(x["izoh"])
    r = subprocess.run(["python3", "scripts/ig_reel.py", f"/tmp/reel/{x['fayl']}", "/tmp/reel/cap.txt"], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
if kerak > 0 and kut:
    joyla(kut[0])  # bir ishga tushishda ko'pi bilan 1 ta
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
# taxminiy jadval: qolganlarni kvota bo'yicha keyingi slotlarga taqsimlash
t = now; i = 0; posted_today = len(bugun) + (1 if kerak > 0 else 0)
day = now.date(); used = posted_today
while i < len(kut) and n:
    for h, mi in SLOTS[n]:
        s = datetime(day.year, day.month, day.day, h, mi, tzinfo=TZ)
        if s <= now or (day == now.date() and used > 0 and SLOTS[n].index((h, mi)) < used): continue
        if i >= len(kut): break
        kut[i]["vaqt"] = s.isoformat(timespec="minutes"); i += 1
    day = day + timedelta(days=1); used = 0
print(f"zaxira {zaxira}, kuniga {n}, bugun chiqqan {len(bugun)}, hozir kerak {max(kerak,0)}")
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
