# Kontent Markazi (artefakt) "Navbat" bo'limi uchun qisqa jadval: content/*-queue.json → bitta JSON.
# Foydalanish: python3 tools/kontent_markazi_navbat.py <chiqish.json>  (repo ildizida, git pull'dan keyin)
import json, sys, os
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); now = datetime.now(TZ)
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
def when(v):
    try: d = datetime.fromisoformat(v).astimezone(TZ)
    except Exception: return v or ""
    day = "bugun" if d.date() == now.date() else "ertaga" if d.date() == (now + timedelta(days=1)).date() else d.strftime("%d.%m")
    return f"{day} {d:%H:%M}"
def title(path):
    d = load(path)
    return (d.get("sarlavha") or d.get("izoh") or os.path.basename(path)).split("\n")[0][:80]
def wait(q):
    return sorted([x for x in q.get("navbat", []) if x.get("holat") == "kutmoqda"], key=lambda x: x.get("vaqt", ""))
reels = [{"vaqt": when(x.get("vaqt")), "nom": (x.get("izoh") or x.get("fayl", "")).split("\n")[0][:80]} for x in wait(load("content/reels-queue.json"))]
lq = wait(load("content/lenta-queue.json"))
lenta = [{"vaqt": when(x["vaqt"]), "nom": title(x["fayl"])} for x in lq if x.get("tur") == "karusel"]
kanal = [{"vaqt": when(x["vaqt"]), "nom": title(x["fayl"])} for x in lq if x.get("tur") == "kanal"]
story = [{"vaqt": when(x.get("vaqt")), "nom": x.get("nom") or x.get("izoh") or x.get("fayl") or "story"} for x in wait(load("content/story-queue.json"))]
posts = sorted([f for f in os.listdir("content/posts") if f.endswith(".json")], reverse=True)[:4]
sayt = [{"vaqt": f[:10][8:10] + "." + f[:10][5:7], "nom": title("content/posts/" + f)} for f in posts]
out = {"yangilandi": now.strftime("%d.%m %H:%M"), "reels": reels, "lenta": lenta, "kanal": kanal, "story": story, "sayt": sayt,
       "izoh": "Saytda — oxirgi e’lon qilinganlar"}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(f"reels {len(reels)}, lenta {len(lenta)}, kanal {len(kanal)}, story {len(story)}, sayt {len(sayt)}")
