# @nur_brand_uzb (Nur Brand) reels navbati. Videolar GitHub Release'da (nurbrand-YYYY-MM), navbat — content/nurbrand-queue.json.
# 10-11 (Jahongir): kuniga 1 ta, soat 19:00 da (har bir videoning "vaqt"i — uning kuni). Kechikib qolsa, shu kuni 23:00 gacha chiqadi.
# "darhol": true — jadvalni kutmaydi. content/nurbrand-pauza fayli bor ekan — hech narsa chiqmaydi. Token: IG_TOKEN (IG_TOKEN_NURBRAND).
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/nurbrand-queue.json"
if not os.environ.get("IG_TOKEN", "").strip() or not os.path.exists(Q): sys.exit(0)
if os.path.exists("content/nurbrand-pauza"): print("nurbrand: pauza"); sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
T = lambda s: datetime.fromisoformat(s).astimezone(TZ)
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and T(x["natija"]["vaqt"]).date() == now.date()]
def joyla(x):
    os.makedirs("/tmp/nb", exist_ok=True)
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    open("/tmp/nb/cap.txt", "w").write(x.get("izoh", ""))
    env = {**os.environ, "IG_USER_TAGS": "", "IG_COLLABS": ""}
    r = subprocess.run(["python3", "scripts/ig_reel.py", url, "/tmp/nb/cap.txt"], capture_output=True, text=True, env=env)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
d = next((x for x in kut if x.get("darhol")), None)
if d: joyla(d); d.pop("darhol", None)
elif kut and not bugun and 10 <= now.hour < 23 and T(kut[0]["vaqt"]) <= now: joyla(kut[0])
else: sys.exit(0)
open(Q, "w").write(json.dumps(q, ensure_ascii=False, indent=2))
