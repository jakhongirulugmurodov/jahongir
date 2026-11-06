# Cinematic navbati akkaunti (06-11 dan @ispanchik.100k) statistikasi: obunachilar va navbatdan chiqqan har bir reels'ning raqamlari.
# Natija: content/cinematic-stats.json ("90 reels" panelidagi Cinematic bo'limi uchun). Token: IG_TOKEN (workflow'da IG_TOKEN_CINEMATIC_YANGI).
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
B = "https://graph.instagram.com/v23.0/"
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen(B + path + "?" + urllib.parse.urlencode(p), timeout=60))
    except urllib.error.HTTPError as e: return json.load(e)
me = get("me", fields="user_id,username,followers_count,media_count")
if not me.get("username"): sys.exit("token ishlamayapti, eski ma'lumot saqlab qolindi: " + json.dumps(me.get("error", me), ensure_ascii=False)[:300])
S = "content/cinematic-stats.json"
old = json.load(open(S)) if os.path.exists(S) else {}
q = json.load(open("content/cinematic-queue.json"))
reels = {}
for x in q["navbat"]:
    mid = x.get("media_id")
    if not mid or x.get("holat") != "chiqdi": continue
    r = get(f"{mid}/insights", metric="views,reach,likes,comments,saved,shares")
    vals = {d["name"]: (d.get("values") or [{}])[0].get("value", 0) for d in r.get("data", [])}
    if not vals: vals = old.get("reels", {}).get(mid, {})
    reels[mid] = {"fayl": x["fayl"], "vaqt": x["natija"]["vaqt"], **{k: v for k, v in vals.items() if k not in ("fayl", "vaqt")}}
kun = datetime.now(timezone.utc).strftime("%Y-%m-%d")
tarix = [t for t in old.get("tarix", []) if t["kun"] != kun] + [{"kun": kun, "obunachi": me.get("followers_count", 0), "korish": sum(v.get("views", 0) for v in reels.values())}]
json.dump({"yangilandi": datetime.now(timezone.utc).isoformat(timespec="minutes"), "akkaunt": me.get("username"),
           "obunachi": me.get("followers_count", 0), "postlar": me.get("media_count", 0), "reels": reels, "tarix": tarix[-120:]},
          open(S, "w"), ensure_ascii=False, indent=2)
print("ok", me.get("username"), me.get("followers_count"), len(reels))
