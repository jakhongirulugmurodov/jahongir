# @osish.nuqtasi statistikasi: obunachilar va har bir chiqqan reels'ning ko'rish/layk/saqlash raqamlari.
# Natija: content/reels-stats.json ("90 reels" paneli uchun). Token: IG_TOKEN (workflow'da IG_TOKEN_OSISH).
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
B = "https://graph.instagram.com/v23.0/"
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen(B + path + "?" + urllib.parse.urlencode(p), timeout=60))
    except urllib.error.HTTPError as e: return json.load(e)
me = get("me", fields="user_id,username,followers_count,media_count")
S = "content/reels-stats.json"
old = json.load(open(S)) if os.path.exists(S) else {}
q = json.load(open("content/reels-queue.json"))
reels = {}
for x in q["navbat"]:
    mid = x.get("media_id")
    if not mid: continue
    r = get(f"{mid}/insights", metric="views,reach,likes,comments,saved,shares")
    vals = {d["name"]: (d.get("values") or [{}])[0].get("value", 0) for d in r.get("data", [])}
    if not vals: vals = old.get("reels", {}).get(mid, {})
    reels[mid] = {"fayl": x["fayl"], "vaqt": x["natija"]["vaqt"], **vals}
tarix = old.get("tarix", [])
kun = datetime.now(timezone.utc).strftime("%Y-%m-%d")
row = {"kun": kun, "obunachi": me.get("followers_count", 0), "korish": sum(v.get("views", 0) for v in reels.values())}
tarix = [t for t in tarix if t["kun"] != kun] + [row]
json.dump({"yangilandi": datetime.now(timezone.utc).isoformat(timespec="minutes"), "akkaunt": me.get("username"),
           "obunachi": me.get("followers_count", 0), "postlar": me.get("media_count", 0), "reels": reels, "tarix": tarix[-120:]},
          open(S, "w"), ensure_ascii=False, indent=2)
print("ok", me.get("username"), me.get("followers_count"), len(reels))
