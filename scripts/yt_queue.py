# Ekspert gapirsin YouTube kanali — Instagram'ga chiqqan har bir reels shu kuni YouTube Shorts bo'lib ham chiqadi (27-11).
# Manba: content/reels-queue.json (holat "chiqdi"). Holat: content/yt-queue.json {"chiqdi": {fayl: {...}}}.
# Kalitlar faqat muhitdan: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (GitHub Secrets) — chop etilmaydi.
# Kuniga ko'pi bilan MAKS_KUN ta (YouTube API kvotasi: 10 000 birlik, bitta yuklash ~1 600).
# Google tekshiruvidan (audit) o'tguncha API orqali yuklangan video YouTube tomonidan "Private" qilib qulflanadi.
# 27-11: eskilari ham — Instagram'da eng ko'p ko'rilganidan boshlab (yangi reels birinchi navbatda). Soatiga bir marta YouTube statistikasi (panel uchun).
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
def tanla():
    if sinov:
        return next((x for x in rq["navbat"] if x["fayl"] == sinov), None) or sys.exit(f"yt: {sinov} navbatda yo'q")
    if len(bugun) >= MAKS_KUN: return None
    tayyor = lambda x: x.get("holat") == "chiqdi" and vaqt(x) and not (yq["chiqdi"].get(x["fayl"]) or {}).get("ok") \
        and (yq["chiqdi"].get(x["fayl"]) or {}).get("urinish", 0) < 3
    # 1) Yangi: Instagram'ga BOSH dan keyin chiqqanlar — darhol
    yangi = [x for x in rq["navbat"] if tayyor(x) and T(vaqt(x)) >= BOSH]
    if yangi: return sorted(yangi, key=vaqt)[0]
    # 2) Eskilar (27-11, Jahongir: "eskilarini ham yukla") — Instagram'da eng ko'p ko'rilganidan boshlab,
    #    08:00–23:00 oralig'ida, kamida 2 soat oraliq bilan; bugungi yangi reels uchun 1 o'rin qoladi
    if not (8 <= now.hour < 23) or len(bugun) >= MAKS_KUN - 1: return None
    oxirgi = max([T(v["vaqt"]) for v in yq["chiqdi"].values() if v.get("ok")] or [now - timedelta(days=1)])
    if now - oxirgi < timedelta(hours=2): return None
    R = (json.load(open("content/reels-stats.json")).get("reels", {}) if os.path.exists("content/reels-stats.json") else {})
    kor = {}
    for x in rq["navbat"]:
        if x.get("holat") == "chiqdi": kor[x["fayl"]] = max(kor.get(x["fayl"], 0), int(R.get(x.get("media_id") or "-", {}).get("views") or 0))
    eski, korildi = [], set()
    for x in rq["navbat"]:
        if tayyor(x) and T(vaqt(x)) < BOSH and x["fayl"] not in korildi: korildi.add(x["fayl"]); eski.append(x)
    return sorted(eski, key=lambda x: -kor.get(x["fayl"], 0))[0] if eski else None

def token():
    d = urllib.parse.urlencode({"client_id": CID, "client_secret": CS, "refresh_token": RT, "grant_type": "refresh_token"}).encode()
    try: return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=60))["access_token"]
    except urllib.error.HTTPError as e: sys.exit("yt: token xato " + e.read().decode()[:200])
def matn(izoh):
    birinchi = re.sub(r"[\U0001F300-\U0001FAFF☀-➿️#]", "", (izoh or "").strip().split("\n")[0]).strip()
    sarlavha = (birinchi[:90].rsplit(" ", 1)[0] if len(birinchi) > 90 else birinchi) or "Ekspert gapirsin"
    return (sarlavha + " #shorts")[:100], ((izoh or "") + "\n\n#ekspertgapirsin #shorts")[:4900]

def statistika():
    if yq.get("stat_vaqt") and now - T(yq["stat_vaqt"]) < timedelta(hours=1): return
    ids = [v["id"] for v in yq["chiqdi"].values() if v.get("ok") and v.get("id")]
    if not ids: return
    at = token(); byid = {}
    for i in range(0, len(ids), 50):
        u = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode({"part": "statistics,status", "id": ",".join(ids[i:i + 50])})
        try: r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + at}), timeout=60))
        except urllib.error.HTTPError as e: print("yt: statistika xato", e.code); return
        for it in r.get("items", []): byid[it["id"]] = it
    for v in yq["chiqdi"].values():
        it = byid.get(v.get("id"))
        if it:
            st = it.get("statistics", {})
            v.update({"korish": int(st.get("viewCount", 0)), "layk": int(st.get("likeCount", 0)), "izoh_soni": int(st.get("commentCount", 0)),
                      "holat": it.get("status", {}).get("privacyStatus", v.get("holat"))})
    yq["stat_vaqt"] = now.isoformat(timespec="minutes")
    print("yt: statistika yangilandi", len(byid))

x = tanla()
if x is None:
    if not sinov: statistika()
    open(Q, "w").write(json.dumps(yq, ensure_ascii=False, indent=2)); sys.exit(0)

rec = yq["chiqdi"].setdefault(x["fayl"], {})
rec["urinish"] = rec.get("urinish", 0) + 1
rec["manba"] = "yangi" if vaqt(x) and T(vaqt(x)) >= BOSH else "eski"
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
