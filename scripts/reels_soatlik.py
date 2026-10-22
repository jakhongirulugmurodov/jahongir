# @osish.nuqtasi reels'larining soatlik o'sishi: chiqqanidan keyin 72 soat davomida har ~soatda
# ko'rish/qamrov/saqlash/ulashish yoziladi → content/reels-soatlik.json. Navbat soqchisi har daqiqada chaqiradi,
# lekin har reels uchun so'rov soatiga ko'pi bilan 1 marta ketadi. Token: IG_TOKEN (workflow'da IG_TOKEN_OSISH).
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit(0)
TZ = timezone(timedelta(hours=5)); now = datetime.now(TZ)
Q, S = "content/reels-queue.json", "content/reels-soatlik.json"
q = json.load(open(Q)); d = json.load(open(S)) if os.path.exists(S) else {}
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen("https://graph.instagram.com/v23.0/" + path + "?" + urllib.parse.urlencode(p), timeout=60))
    except Exception as e:
        try: return json.load(e)
        except Exception: return {}
changed = False
for x in q["navbat"]:
    mid = x.get("media_id")
    if x.get("holat") != "chiqdi" or not mid: continue
    t0 = datetime.fromisoformat(x["natija"]["vaqt"])
    if now - t0 > timedelta(hours=72): continue
    rows = d.setdefault(mid, {"fayl": x["fayl"], "chiqdi": x["natija"]["vaqt"], "olchov": []})["olchov"]
    if rows and now - datetime.fromisoformat(rows[-1]["t"]) < timedelta(minutes=55): continue
    r = get(f"{mid}/insights", metric="views,reach,saved,shares")
    v = {m["name"]: (m.get("values") or [{}])[0].get("value", 0) for m in r.get("data", [])}
    if not v: continue
    rows.append({"t": now.isoformat(timespec="minutes"), "soat": round((now - t0).total_seconds() / 3600, 1), **v}); changed = True
if changed:
    json.dump(d, open(S, "w"), ensure_ascii=False, indent=1); print("soatlik yangilandi")
