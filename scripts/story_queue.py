# Story navbatini bajaradi: vaqti kelgan birinchi "kutmoqda" yozuvni Telegram va Instagram'ga joylaydi.
# Bir ishga tushishda faqat bitta story. Tokenlar muhit o'zgaruvchilarida (TG_BOT_TOKEN, IG_TOKEN).
import json, subprocess, sys
from datetime import datetime, timezone
Q = "content/story-queue.json"
q = json.load(open(Q)); now = datetime.now(timezone.utc)
item = next((x for x in q["navbat"] if x.get("holat") == "kutmoqda" and datetime.fromisoformat(x["vaqt"]) <= now), None)
if not item:
    print("navbatda vaqti kelgan story yo'q"); sys.exit(0)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-300:]); return r.returncode == 0
tg = run(["python3", "scripts/tg_story.py", item["tg_rasm"], item["havola"], *item["maydon"].split(), str(item.get("soat", 24))])
ig = run(["python3", "scripts/ig_story.py", item["ig_rasm"], item["havola"], item.get("sarlavha", "")])
item["holat"] = "chiqdi" if tg and ig else ("qisman" if tg or ig else "xato")
item["natija"] = {"telegram": tg, "instagram": ig, "vaqt": now.isoformat(timespec="minutes")}
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
print("holat:", item["holat"])
