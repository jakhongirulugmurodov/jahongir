# Instagram'ga VIDEO story joylaydi (token qaysi akkauntniki bo'lsa, o'shanga). 22-11: Nur Brand reels'i bilan birga chiqadigan story.
# Foydalanish: python3 scripts/ig_story_video.py <ochiq video URL>. Token faqat IG_TOKEN muhit o'zgaruvchisidan olinadi, chop etilmaydi.
# Story videosi: 9:16, ≤60 soniya (biz 59 soniyagacha tayyorlaymiz).
import json, os, sys, time, urllib.request, urllib.parse
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
B = "https://graph.instagram.com/v23.0/"
def call(path, method="GET", **p):
    p["access_token"] = T
    q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ("?" + q if method == "GET" else ""), q.encode() if method == "POST" else None)
    try: return json.load(urllib.request.urlopen(req, timeout=90))
    except urllib.error.HTTPError as e: return json.load(e)
uid = call("me", fields="user_id").get("user_id") or sys.exit("akkaunt topilmadi (token?)")
c = call(f"{uid}/media", "POST", media_type="STORIES", video_url=sys.argv[1])
if "id" not in c: sys.exit("konteyner xato: " + json.dumps(c.get("error", c), ensure_ascii=False)[:300])
for _ in range(90):  # video qayta ishlanishi bir necha daqiqa olishi mumkin
    s = call(c["id"], fields="status_code,status").get("status_code")
    if s == "FINISHED": break
    if s == "ERROR": sys.exit("Instagram story videosini qabul qilmadi: " + json.dumps(call(c["id"], fields="status"), ensure_ascii=False)[:300])
    time.sleep(5)
r = call(f"{uid}/media_publish", "POST", creation_id=c["id"])
print("natija:", json.dumps({"ok": "id" in r, "id": r.get("id"), "xato": r.get("error", {}).get("message")}, ensure_ascii=False))
sys.exit(0 if "id" in r else 1)
