# Reels navbati (@osish.nuqtasi). Videolar GitHub Release'da turadi (repozitoriyada emas), bu skript vaqti kelganini
# yuklab olib Instagram'ga joylaydi. Bir ishga tushishda ko'pi bilan 1 ta reels (kuniga 3 ta jadvalga qo'yiladi).
import json, os, subprocess, sys
from datetime import datetime, timezone
Q = "content/reels-queue.json"
if not os.path.exists(Q): sys.exit(0)
q = json.load(open(Q)); now = datetime.now(timezone.utc)
x = next((x for x in sorted(q["navbat"], key=lambda x: x["vaqt"]) if x.get("holat") == "kutmoqda" and datetime.fromisoformat(x["vaqt"]) <= now), None)
if not x: print("reels navbatida vaqti kelgani yo'q"); sys.exit(0)
os.makedirs("/tmp/reel", exist_ok=True)
d = subprocess.run(["gh", "release", "download", x["release"], "-p", x["fayl"], "-D", "/tmp/reel", "--clobber"], capture_output=True, text=True)
if d.returncode: print(d.stderr[-300:]); x["holat"] = "xato"; x["natija"] = {"vaqt": now.isoformat(timespec="minutes"), "xato": "yuklab olinmadi"}
else:
    open("/tmp/reel/cap.txt", "w").write(x["izoh"])
    r = subprocess.run(["python3", "scripts/ig_reel.py", f"/tmp/reel/{x['fayl']}", "/tmp/reel/cap.txt"], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(timezone.utc).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
