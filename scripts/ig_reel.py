# Instagram Reels joylaydi (O'sish Nuqtasi: @osish.nuqtasi). Video ochiq URL orqali (GitHub Release havolasi) beriladi. Foydalanish: python3 scripts/ig_reel.py <ochiq video URL> <caption fayli> [muqova soniyasi ms]
# Token faqat IG_TOKEN muhit o'zgaruvchisidan (workflow'da IG_TOKEN_OSISH), chop etilmaydi.
import json, os, sys, time, urllib.request, urllib.parse
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
video, capf = sys.argv[1], sys.argv[2]; cap = open(capf).read().strip()
V = "v23.0"; B = f"https://graph.instagram.com/{V}/"
def call(path, method="GET", **p):
    p["access_token"] = T; q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ("?" + q if method == "GET" else ""), q.encode() if method == "POST" else None)
    try: return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e: return json.load(e)
uid = call("me", fields="user_id").get("user_id") or sys.exit("akkaunt topilmadi (token?)")
extra = {"thumb_offset": sys.argv[3]} if len(sys.argv) > 3 else {}
# Instagram Login (graph.instagram.com) faqat ochiq video_url qabul qiladi (resumable yuklash faqat Facebook Login'da).
# Repo ochiq: Release havolasi -> GitHub vaqtinchalik imzolangan havolaga yo'naltiradi; oxirgi havolani beramiz.
src = video
if src.startswith("http"):
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    try: urllib.request.build_opener(NoRedir).open(urllib.request.Request(src, method="HEAD"), timeout=30)
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308): src = e.headers["Location"]
# Belgilanadigan akkauntlar (IG_USER_TAGS="hasankhoja,boshqa"): reels ichida "user_tags" sifatida; rad etilsa tegsiz qayta uriniladi
tags = [u.strip().lstrip("@") for u in os.environ.get("IG_USER_TAGS", "").split(",") if u.strip()]
if tags: extra["user_tags"] = json.dumps([{"username": u} for u in tags])
c = call(f"{uid}/media", "POST", media_type="REELS", video_url=src, caption=cap, share_to_feed="true", **extra)
if "id" not in c and tags:
    print("user_tags rad etildi, tegsiz qayta urinamiz:", json.dumps(c.get("error", c), ensure_ascii=False)[:200])
    extra.pop("user_tags"); c = call(f"{uid}/media", "POST", media_type="REELS", video_url=src, caption=cap, share_to_feed="true", **extra)
if "id" not in c: sys.exit("konteyner xato: " + json.dumps(c.get("error", c), ensure_ascii=False))
for _ in range(120):  # video ishlov berilishi bir necha daqiqa olishi mumkin
    s = call(c["id"], fields="status_code,status")
    if s.get("status_code") == "FINISHED": break
    if s.get("status_code") == "ERROR": sys.exit("Instagram videoni qabul qilmadi: " + str(s.get("status")))
    time.sleep(5)
else: sys.exit("ishlov berish juda uzoq davom etdi")
r = call(f"{uid}/media_publish", "POST", creation_id=c["id"])
print("natija:", json.dumps({"ok": "id" in r, "id": r.get("id"), "xato": r.get("error", {}).get("message")}, ensure_ascii=False))
sys.exit(0 if "id" in r else 1)
