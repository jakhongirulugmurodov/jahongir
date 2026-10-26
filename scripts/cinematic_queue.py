# @cinematic.soul52 reels navbati. Videolar GitHub Release'da (cinematic-YYYY-MM), navbat — content/cinematic-queue.json.
# Reja (26-10, Jahongir): 2 haftada 100 ta reels. Birinchi video chiqqan kundan 14 kun sanaladi; har kuni ertalab
# "qolgan ÷ qolgan kun" hisoblanadi (kuniga ko'pi bilan 8 ta), shuncha slot ochiladi. 23:00–08:00 chiqmaydi, oraliq kamida 90 daqiqa.
# "darhol": true qo'yilgani jadvalni kutmaydi. Token: IG_TOKEN (workflow'da IG_TOKEN_CINEMATIC); token bo'lmasa jim chiqadi.
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/cinematic-queue.json"
if not os.environ.get("IG_TOKEN", "").strip() or not os.path.exists(Q): sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
REJA, KUN, MAKS = q.get("reja_soni", 100), q.get("reja_kun", 14), 8
SLOTS = [(8, 30), (10, 0), (11, 30), (13, 0), (15, 0), (17, 0), (19, 0), (21, 0)]
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
chiq = [x for x in q["navbat"] if x.get("holat") == "chiqdi"]
T = lambda x: datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ)
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and T(x).date() == now.date()]
boshi = datetime.fromisoformat(q["reja_boshi"]).date() if q.get("reja_boshi") else now.date()
qolgan_kun = max(1, (boshi + timedelta(days=KUN) - now.date()).days)
oldin = sum(1 for x in chiq if T(x).date() < now.date())
n = min(MAKS, max(1, -(-(REJA - oldin) // qolgan_kun))) if oldin < REJA else 0
# n ta slotni kun bo'ylab teng taqsimlash
sl = [SLOTS[round(i * (len(SLOTS) - 1) / max(1, n - 1))] for i in range(n)] if n > 1 else SLOTS[3:4] if n else []
due = sum(1 for h, m in sl if now.replace(hour=h, minute=m, second=0, microsecond=0) <= now)
oxirgi = max((T(x) for x in chiq), default=None)
oraliq_ok = not oxirgi or now - oxirgi >= timedelta(minutes=90)
kecha = now.hour < 8 or now.hour >= 23
def joyla(x):
    os.makedirs("/tmp/cin", exist_ok=True)
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    open("/tmp/cin/cap.txt", "w").write(x.get("izoh", ""))
    env = {**os.environ, "IG_USER_TAGS": ",".join(x.get("teglar", [])), "IG_COLLABS": ""}
    r = subprocess.run(["python3", "scripts/ig_reel.py", url, "/tmp/cin/cap.txt"], capture_output=True, text=True, env=env)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
    if x["holat"] == "chiqdi" and not q.get("reja_boshi"): q["reja_boshi"] = now.date().isoformat()
d = next((x for x in kut if x.get("darhol")), None)
if d: joyla(d); d.pop("darhol", None)
elif kut and not kecha and oraliq_ok and due > len(bugun): joyla(kut[0])
q["kunlik"] = {"kun": now.date().isoformat(), "kuniga": n, "bugun": len([x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and T(x).date() == now.date()]),
               "navbatda": len([x for x in q["navbat"] if x.get("holat") == "kutmoqda"])}
out = json.dumps(q, ensure_ascii=False, indent=2)
if out != open(Q).read(): open(Q, "w").write(out)
