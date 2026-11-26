# Ekspert gapirsin YouTube kanali — Instagram'ga chiqqan har bir reels shu kuni YouTube Shorts bo'lib ham chiqadi (27-11).
# Manba: content/reels-queue.json (holat "chiqdi"). Holat: content/yt-queue.json {"chiqdi": {fayl: {...}}}.
# Kalitlar faqat muhitdan: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (GitHub Secrets) — chop etilmaydi.
# Kuniga ko'pi bilan MAKS_KUN ta (YouTube API kvotasi: 10 000 birlik, bitta yuklash ~1 600).
# Google tekshiruvidan (audit) o'tguncha API orqali yuklangan video YouTube tomonidan "Private" qilib qulflanadi.
# Qo'lda sinov: YT_SINOV=v36.mp4 python3 scripts/yt_queue.py — shu faylni darhol yuklaydi.
import json, os, re, sys, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/yt-queue.json"; R = "content/reels-queue.json"
BOSH = datetime(2026, 11, 27, tzinfo=TZ)  # shu kundan keyin Instagram'ga chiqqanlar (eskilari alohida qaror bilan)
MAKS_KUN = 6
CID, CS, RT = (os.environ.get(k, "").strip() for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"))
if not (CID and CS and RT) or not os.path.exists(R): sys.exit(0)
if os.path.exists("content/yt-pauza"): print("yt: pauza"); sys.exit(0)
now = datetime.now(TZ)
yq = json.load(open(Q)) if os.path.exists(Q) else {"chiqdi": {}}
rq = json.load(open(R))
T = lambda s: datetime.fromisoformat(s).astimezone(TZ)
def vaqt(x): return (x.get("natija") or {}).get("vaqt") or x.get("vaqt") or ""
bugun = [v for v in yq["chiqdi"].values() if v.get("ok") and T(v["vaqt"]).date() == now.date()]
sinov = os.environ.get("YT_SINOV", "").strip()
if sinov:
    x = next((x for x in rq["navbat"] if x["fayl"] == sinov), None) or sys.exit(f"yt: {sinov} navbatda yo'q")
else:
    if len(bugun) >= MAKS_KUN: sys.exit(0)
    kut = [x for x in rq["navbat"] if x.get("holat") == "chiqdi" and vaqt(x) and T(vaqt(x)) >= BOSH
           and not (yq["chiqdi"].get(x["fayl"]) or {}).get("ok") and (yq["chiqdi"].get(x["fayl"]) or {}).get("urinish", 0) < 3]
    if not kut: sys.exit(0)
    x = sorted(kut, key=vaqt)[0]

def token():
    d = urllib.parse.urlencode({"client_id": CID, "client_secret": CS, "refresh_token": RT, "grant_type": "refresh_token"}).encode()
    try: return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=60))["access_token"]
    except urllib.error.HTTPError as e: sys.exit("yt: token xato " + e.read().decode()[:200])
def matn(izoh):
    birinchi = re.sub(r"[\U0001F300-\U0001FAFF☀-➿️#]", "", (izoh or "").strip().split("\n")[0]).strip()
    sarlavha = (birinchi[:90].rsplit(" ", 1)[0] if len(birinchi) > 90 else birinchi) or "Ekspert gapirsin"
    return (sarlavha + " #shorts")[:100], ((izoh or "") + "\n\n#ekspertgapirsin #shorts")[:4900]

rec = yq["chiqdi"].setdefault(x["fayl"], {})
rec["urinish"] = rec.get("urinish", 0) + 1
try:
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    os.makedirs("/tmp/yt", exist_ok=True); f = "/tmp/yt/" + x["fayl"]
    urllib.request.urlretrieve(url, f)
    at = token(); title, desc = matn(x.get("izoh"))
    meta = {"snippet": {"title": title, "description": desc, "categoryId": "27", "defaultLanguage": "uz", "tags": ["ekspert gapirsin", "podkast", "shorts"]},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    size = os.path.getsize(f)
    req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", json.dumps(meta).encode(),
                                 {"Authorization": "Bearer " + at, "Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = urllib.request.urlopen(req, timeout=60).headers["Location"]
    put = urllib.request.Request(loc, open(f, "rb").read(), {"Authorization": "Bearer " + at, "Content-Type": "video/mp4"}, method="PUT")
    r = json.load(urllib.request.urlopen(put, timeout=900))
    rec.update({"ok": True, "id": r["id"], "vaqt": now.isoformat(timespec="minutes"), "holat": r.get("status", {}).get("privacyStatus"), "sarlavha": title})
    rec.pop("xato", None)
    print("yt: chiqdi", x["fayl"], r["id"], rec["holat"])
except urllib.error.HTTPError as e:
    rec.update({"ok": False, "vaqt": now.isoformat(timespec="minutes"), "xato": f"{e.code} {e.read().decode()[:300]}"}); print("yt: xato", x["fayl"], rec["xato"])
except Exception as e:
    rec.update({"ok": False, "vaqt": now.isoformat(timespec="minutes"), "xato": str(e)[:300]}); print("yt: xato", x["fayl"], rec["xato"])
open(Q, "w").write(json.dumps(yq, ensure_ascii=False, indent=2))
