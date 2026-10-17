# Instagram story joylaydi (jahongir.olmos). Foydalanish: python3 scripts/ig_story.py <ochiq rasm URL>
# Token faqat IG_TOKEN muhit o'zgaruvchisidan olinadi, chop etilmaydi.
import json, os, sys, time, urllib.request, urllib.parse
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
uid = json.load(open("content/instagram.json"))["instagram_user_id"]
B = "https://graph.instagram.com/v23.0/"
def call(path, method="GET", **p):
    p["access_token"] = T
    q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ("?" + q if method == "GET" else ""), q.encode() if method == "POST" else None)
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return json.load(e)
c = call(f"{uid}/media", "POST", media_type="STORIES", image_url=sys.argv[1])
if "id" not in c:
    sys.exit("konteyner xato: " + json.dumps(c.get("error", c), ensure_ascii=False))
for _ in range(20):
    s = call(c["id"], fields="status_code").get("status_code")
    if s == "FINISHED": break
    if s == "ERROR": sys.exit("Instagram rasmni qabul qilmadi")
    time.sleep(3)
r = call(f"{uid}/media_publish", "POST", creation_id=c["id"])
print("natija:", json.dumps({"ok": "id" in r, "id": r.get("id"), "xato": r.get("error", {}).get("message")}, ensure_ascii=False))
sys.exit(0 if "id" in r else 1)
