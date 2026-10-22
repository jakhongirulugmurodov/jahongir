# Mac'dan olingan tayyor reels partiyasini GitHub Release'ga yuklaydi va content/reels-queue.json'ga jadval bilan qo'shadi.
# Foydalanish (repo ildizidan): python3 tools/reels/yukla.py <videolar papkasi> <izohlar.json>
# izohlar.json: {"fayl.mp4": "caption", ...} — tartib shu bo'yicha. Release nomi: reels-YYYY-MM.
# Jadval: bu yerdagi vaqt taxminiy; aniq chiqish soni va vaqtini scripts/reels_queue.py zaxiraga qarab har daqiqada qayta hisoblaydi.
import json, os, subprocess, sys, re
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from uztypo import typo
TZ = timezone(timedelta(hours=5)); Q = "content/reels-queue.json"
src, caps = sys.argv[1], json.load(open(sys.argv[2])); q = json.load(open(Q))
slots = [tuple(map(int, s.split(":"))) for s in q["soatlar"]]
last = max([datetime.fromisoformat(x["vaqt"]) for x in q["navbat"]] + [datetime.now(TZ) + timedelta(minutes=30)])
def nxt(t):
    t = t.astimezone(TZ)
    for d in range(0, 4):
        day = (t + timedelta(days=d)).date()
        for h, m in slots:
            c = datetime(day.year, day.month, day.day, h, m, tzinfo=TZ)
            if c > t: return c
tag = "reels-" + datetime.now(TZ).strftime("%Y-%m")
if subprocess.run(["gh", "release", "view", tag], capture_output=True).returncode:
    subprocess.run(["gh", "release", "create", tag, "-t", f"O‘sish Nuqtasi reels {tag[6:]}", "-n", "Instagram uchun tayyor reels (navbat: content/reels-queue.json)"], check=True)
t = last
for name, cap in caps.items():
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", name)
    p = os.path.join(src, name)
    if safe != name: os.replace(p, os.path.join(src, safe)); p = os.path.join(src, safe)
    subprocess.run(["gh", "release", "upload", tag, p, "--clobber"], check=True)
    t = nxt(t); it = {"vaqt": t.isoformat(timespec="minutes"), "release": tag, "fayl": safe, "izoh": typo(cap), "holat": "kutmoqda"}
    teg = [u for u in dict.fromkeys(re.findall(r"@([A-Za-z0-9._]+[A-Za-z0-9_])", cap)) if u != "osish.nuqtasi"]  # caption'dagi @spiker → reels'da belgilanadi
    if teg: it["teglar"] = teg
    q["navbat"].append(it)
    print(t.strftime("%d-%m %H:%M"), safe)
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
