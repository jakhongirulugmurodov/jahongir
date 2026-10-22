# Trial reels ruxsatini tekshiradi: trial_params bilan konteyner ochadi, lekin JOYLAMAYDI (konteyner 24 soatda o'zi o'chadi).
# Foydalanish (workflow'da): IG_TOKEN=... python3 scripts/ig_trial_check.py <ochiq video URL>
import json, os, sys, time, urllib.request, urllib.parse
T = os.environ["IG_TOKEN"].strip(); B = "https://graph.instagram.com/v23.0/"
def call(path, method="GET", **p):
    p["access_token"] = T; q = urllib.parse.urlencode(p)
    req = urllib.request.Request(B + path + ("?" + q if method == "GET" else ""), q.encode() if method == "POST" else None)
    try: return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e: return json.load(e)
uid = call("me", fields="user_id").get("user_id")
src = sys.argv[1]
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
try: urllib.request.build_opener(NR).open(urllib.request.Request(src, method="HEAD"), timeout=30)
except urllib.error.HTTPError as e:
    if e.code in (301, 302, 303, 307, 308): src = e.headers["Location"]
c = call(f"{uid}/media", "POST", media_type="REELS", video_url=src, caption="trial tekshiruv (joylanmaydi)",
         trial_params=json.dumps({"graduation_strategy": "SS_PERFORMANCE"}))
print("konteyner:", json.dumps(c, ensure_ascii=False)[:400])
if "id" in c:
    for _ in range(60):
        s = call(c["id"], fields="status_code,status")
        if s.get("status_code") in ("FINISHED", "ERROR"): break
        time.sleep(5)
    print("holat:", json.dumps(s, ensure_ascii=False)[:400], "— JOYLANMADI")
