# jahongir.olmos statistikasi: obunachilar va lentadagi karusellar natijasi (qamrov, layk, saqlash...).
# Natija: content/blog-stats.json ("Blog jadvali" paneli uchun). Token: IG_TOKEN (asosiy akkaunt).
import json, os, re, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
B = "https://graph.instagram.com/v23.0/"
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen(B + path + "?" + urllib.parse.urlencode(p), timeout=60))
    except urllib.error.HTTPError as e: return json.load(e)
me = get("me", fields="username,followers_count,media_count")
S = "content/blog-stats.json"; old = json.load(open(S)) if os.path.exists(S) else {}
q = json.load(open("content/lenta-queue.json")); posts = {}
for x in q["navbat"]:
    if x["tur"] != "karusel" or x.get("holat") != "chiqdi": continue
    m = re.search(r'"id": "(\d+)"', x.get("natija", {}).get("chiqish", ""))
    if not m: continue
    mid = m.group(1)
    r = get(f"{mid}/insights", metric="views,reach,likes,comments,saved,shares")
    vals = {d["name"]: (d.get("values") or [{}])[0].get("value", 0) for d in r.get("data", [])} or old.get("postlar", {}).get(mid, {})
    posts[mid] = {"fayl": x["fayl"], "vaqt": x["natija"]["vaqt"], **{k: v for k, v in vals.items() if k not in ("fayl", "vaqt")}}
kun = datetime.now(timezone.utc).strftime("%Y-%m-%d")
tarix = [t for t in old.get("tarix", []) if t["kun"] != kun] + [{"kun": kun, "obunachi": me.get("followers_count", 0)}]
json.dump({"yangilandi": datetime.now(timezone.utc).isoformat(timespec="minutes"), "akkaunt": me.get("username"), "obunachi": me.get("followers_count", 0),
           "postlar": posts, "tarix": tarix[-180:]}, open(S, "w"), ensure_ascii=False, indent=2)
print("ok", me.get("username"), me.get("followers_count"), len(posts))
