# Story navbatini bajaradi.
# Qoidalar (Jahongir): bitta blokdagi (bir loyiha/mavzu) story'lar bittada, ketma-ket joylanadi;
# boshqa blokdagi story oldingisidan kamida 1 soat keyin chiqadi.
# Tokenlar muhit o'zgaruvchilarida (TG_BOT_TOKEN, IG_TOKEN).
import json, subprocess, sys
from datetime import datetime, timezone, timedelta
Q = "content/story-queue.json"
q = json.load(open(Q)); now = datetime.now(timezone.utc); N = q["navbat"]
done = [x for x in N if x.get("natija", {}).get("vaqt")]
last = max(done, key=lambda x: x["natija"]["vaqt"]) if done else None
first = next((x for x in N if x.get("holat") == "kutmoqda" and datetime.fromisoformat(x["vaqt"]) <= now), None)
if not first:
    print("navbatda vaqti kelgan story yo'q"); sys.exit(0)
blok = first.get("blok", "")
if last and last.get("blok", "") != blok and now - datetime.fromisoformat(last["natija"]["vaqt"]) < timedelta(hours=1):
    print("boshqa blok: oldingi story'dan 1 soat o'tmagan, kutamiz"); sys.exit(0)
batch = [first] + ([x for x in N if x is not first and x.get("holat") == "kutmoqda" and blok and x.get("blok") == blok])
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-300:]); return r.returncode == 0
for item in batch:
    tg = run(["python3", "scripts/tg_story.py", item["tg_rasm"], item["havola"], *item["maydon"].split(), str(item.get("soat", 24))])
    ig = run(["python3", "scripts/ig_story.py", item["ig_rasm"], item["havola"], item.get("sarlavha", "")])
    item["holat"] = "chiqdi" if tg and ig else ("qisman" if tg or ig else "xato")
    item["natija"] = {"telegram": tg, "instagram": ig, "vaqt": datetime.now(timezone.utc).isoformat(timespec="minutes")}
    print(item.get("sarlavha", "")[:50], "→", item["holat"])
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
