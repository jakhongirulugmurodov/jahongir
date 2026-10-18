# Instagram Reels joylaydi (O'sish Nuqtasi: @osish.nuqtasi). Video lokal fayldan "resumable upload" bilan yuboriladi,
# ochiq URL kerak emas. Foydalanish: python3 scripts/ig_reel.py <video.mp4> <caption fayli> [muqova soniyasi ms]
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
c = call(f"{uid}/media", "POST", media_type="REELS", upload_type="resumable", caption=cap, share_to_feed="true", **extra)
if "id" not in c: sys.exit("konteyner xato: " + json.dumps(c.get("error", c), ensure_ascii=False))
size = os.path.getsize(video)
req = urllib.request.Request(f"https://rupload.facebook.com/ig-api-upload/{V}/{c['id']}", open(video, "rb").read(),
                             {"Authorization": f"OAuth {T}", "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"})
try: up = json.load(urllib.request.urlopen(req, timeout=600))
except urllib.error.HTTPError as e: up = json.load(e)
if not up.get("success"): sys.exit("yuklash xato: " + json.dumps(up, ensure_ascii=False)[:300])
for _ in range(120):  # video ishlov berilishi bir necha daqiqa olishi mumkin
    s = call(c["id"], fields="status_code,status")
    if s.get("status_code") == "FINISHED": break
    if s.get("status_code") == "ERROR": sys.exit("Instagram videoni qabul qilmadi: " + str(s.get("status")))
    time.sleep(5)
else: sys.exit("ishlov berish juda uzoq davom etdi")
r = call(f"{uid}/media_publish", "POST", creation_id=c["id"])
print("natija:", json.dumps({"ok": "id" in r, "id": r.get("id"), "xato": r.get("error", {}).get("message")}, ensure_ascii=False))
sys.exit(0 if "id" in r else 1)
