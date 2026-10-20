# Instagram Reels joylaydi (IG_TOKEN qaysi akkauntniki bo'lsa — @osish.nuqtasi yoki jahongir.olmos). Video ochiq URL orqali (GitHub Release havolasi) beriladi. Foydalanish: python3 scripts/ig_reel.py <ochiq video URL> <caption fayli> [muqova soniyasi ms]
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
# Collab: IG_COLLAB="jahongir.olmos" — bitta post ikkala profilda ko'rinadi (takror joylash o'rniga; takror video tavsiyadan tushadi).
# Hamkor taklifni Instagram ilovasida bir marta qabul qiladi. API rad etsa — collab'siz joylaymiz (post yo'qolmasin).
collab = [u.strip().lstrip("@") for u in os.environ.get("IG_COLLAB", "").split(",") if u.strip()]
c = call(f"{uid}/media", "POST", media_type="REELS", video_url=src, caption=cap, share_to_feed="true",
         **({"collaborators": json.dumps(collab)} if collab else {}), **extra)
if "id" not in c and collab:
    print("collab rad etildi, collab'siz joylanadi:", json.dumps(c.get("error", c), ensure_ascii=False)[:200])
    c = call(f"{uid}/media", "POST", media_type="REELS", video_url=src, caption=cap, share_to_feed="true", **extra)
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
