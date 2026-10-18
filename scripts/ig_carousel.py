# Instagram karusel joylaydi (jahongir.olmos). Foydalanish: python3 scripts/ig_carousel.py content/lenta/<post>-ig.json
# JSON: {"rasmlar": [ochiq URL, ...], "izoh": "...", "havola": "post URL", "sarlavha": "..."}
# Post ID → havola content/story-map.json ga yoziladi (AI agent izohga "AI" deb yozganga shuni yuboradi).
import json, os, sys, time, urllib.request, urllib.parse
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
spec = json.load(open(sys.argv[1])); uid = json.load(open("content/instagram.json"))["instagram_user_id"]
B = "https://graph.instagram.com/v23.0/"
def call(path, method="GET", **p):
    p["access_token"] = T; q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ("?" + q if method == "GET" else ""), q.encode() if method == "POST" else None)
    try: return json.load(urllib.request.urlopen(req, timeout=90))
    except urllib.error.HTTPError as e: return json.load(e)
def wait(cid):
    for _ in range(40):
        s = call(cid, fields="status_code").get("status_code")
        if s == "FINISHED": return True
        if s == "ERROR": return False
        time.sleep(3)
    return False
kids = []
for u in spec["rasmlar"]:
    c = call(f"{uid}/media", "POST", image_url=u, is_carousel_item="true")
    if "id" not in c: sys.exit("slayd xato: " + u + " " + json.dumps(c.get("error", c), ensure_ascii=False))
    kids.append(c["id"])
for k in kids:
    if not wait(k): sys.exit("Instagram slaydni qabul qilmadi")
c = call(f"{uid}/media", "POST", media_type="CAROUSEL", children=",".join(kids), caption=spec["izoh"])
if "id" not in c or not wait(c["id"]): sys.exit("karusel konteyner xato: " + json.dumps(c.get("error", c), ensure_ascii=False))
r = call(f"{uid}/media_publish", "POST", creation_id=c["id"])
print("natija:", json.dumps({"ok": "id" in r, "id": r.get("id"), "xato": r.get("error", {}).get("message")}, ensure_ascii=False))
if "id" in r and spec.get("havola"):
    m = json.load(open("content/story-map.json"))
    m.setdefault("stories", {})[r["id"]] = {"url": spec["havola"], "title": spec.get("sarlavha", ""), "tur": "karusel"}
    json.dump(m, open("content/story-map.json", "w"), ensure_ascii=False, indent=2)
sys.exit(0 if "id" in r else 1)
