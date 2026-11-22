# @haya.perfum (Haya Perfum) reels navbati — nurbrand_queue.py nusxasi (22-11). Videolar GitHub Release'da (haya-YYYY-MM), navbat — content/haya-queue.json.
# 10-11 (Jahongir): kuniga 1 ta. 22-11: endi har kuni SHOM kirishi bilan (Toshkentda quyosh botishi, har kuni hisoblanadi);
# reels bilan birga uning storysi ham chiqadi ("story": release'dagi tayyor story videosi). Kechikib qolsa, shu kuni 23:00 gacha chiqadi.
# "darhol": true — jadvalni kutmaydi. content/haya-pauza fayli bor ekan — hech narsa chiqmaydi. Token: IG_TOKEN (IG_TOKEN_NURBRAND).
import json, os, re, subprocess, sys, math
from datetime import datetime, timezone, timedelta, date
TZ = timezone(timedelta(hours=5)); Q = "content/haya-queue.json"
if not os.environ.get("IG_TOKEN", "").strip() or not os.path.exists(Q): sys.exit(0)
if os.path.exists("content/haya-pauza"): print("haya: pauza"); sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
T = lambda s: datetime.fromisoformat(s).astimezone(TZ)
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and T(x["natija"]["vaqt"]).date() == now.date()]
from datetime import date
BOSH = date(2026, 11, 23)  # 22-11: Jahongir — "videolar dushanbadan chiqsin"
def shom(d):  # Toshkent (41.30N, 69.24E) quyosh botishi (NOAA usuli, refraksiya bilan), mahalliy vaqt
    lat, lon = 41.2995, 69.2401; n = d.timetuple().tm_yday; g = 2 * math.pi / 365 * (n - 1 + (18 - 12) / 24)
    eq = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    de = 0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(lat)) * math.cos(de)) - math.tan(math.radians(lat)) * math.tan(de)))
    m = 720 - 4 * (lon - ha) - eq + 5 * 60 + 2  # +2 daqiqa: shom kirgandan keyin
    return datetime(d.year, d.month, d.day, int(m // 60), int(m % 60), tzinfo=TZ)
URL = lambda x, f: f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{f}"
def story(x):
    r = subprocess.run(["python3", "scripts/ig_story_video.py", URL(x, x["story"])], capture_output=True, text=True, env=os.environ)
    print("story:", r.stdout.strip(), r.stderr.strip()[-300:])
    m = re.search(r'"id": "(\d+)"', r.stdout)
    x["story_natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "ok": bool(m and r.returncode == 0), "id": m.group(1) if m else None, "chiqish": (r.stdout + r.stderr).strip()[-200:]}
def joyla(x):
    os.makedirs("/tmp/haya", exist_ok=True)
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    open("/tmp/haya/cap.txt", "w").write(x.get("izoh", ""))
    env = {**os.environ, "IG_USER_TAGS": "", "IG_COLLABS": ""}
    r = subprocess.run(["python3", "scripts/ig_reel.py", url, "/tmp/haya/cap.txt"], capture_output=True, text=True, env=env)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
    if x["holat"] == "chiqdi" and x.get("story"): story(x)
# Jadval (ko'rinish uchun): kutayotganlar ketma-ket kunlarning shom vaqtiga
kun = now.date() if not bugun and now < shom(now.date()).replace(hour=23, minute=0) else now.date() + timedelta(days=1)
kun = max(kun, BOSH)
for x in kut:
    if not x.get("darhol"): x["vaqt"] = shom(kun).isoformat(timespec="minutes"); kun += timedelta(days=1)
# Reels'i chiqib, storysi hali chiqmaganlar (masalan 22-11 dagi 4K sinov) — shomdan keyin storysi chiqadi
qarz = next((x for x in q["navbat"] if x.get("holat") == "chiqdi" and x.get("story") and not x.get("story_natija")), None)
d = next((x for x in kut if x.get("darhol")), None)
if d: joyla(d); d.pop("darhol", None)
elif kut and not bugun and shom(now.date()) <= now and now.hour < 23 and T(kut[0]["vaqt"]).date() <= now.date(): joyla(kut[0])
elif qarz and (qarz.get("story_darhol") or (shom(now.date()) <= now and now.hour < 23)): story(qarz); qarz.pop("story_darhol", None)  # "story_darhol": true — storyni hozir
else:
    open(Q, "w").write(json.dumps(q, ensure_ascii=False, indent=2)); sys.exit(0)
open(Q, "w").write(json.dumps(q, ensure_ascii=False, indent=2))
