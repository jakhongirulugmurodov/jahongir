# "90 Reels" paneli uchun ma'lumot fayllari: content/reels-*.json → 4 ta qator-JSON (navbat, statistika, tarix, papka).
# Foydalanish: python3 tools/reels/panel_data.py <chiqish papka>
import json, os, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
L = lambda f, d: json.load(open(f)) if os.path.exists(f) else d
q = L("content/reels-queue.json", {"navbat": []}); s = L("content/reels-stats.json", {}); p = L("content/reels-papka.json", {})
def spiker(f):  # 26-10 Jahongir: ≤26 Hasanxo‘ja, 27–58 farzand tarbiyasi suhbati, 59–79 Mohir Mirzaxmedov, 80–91 Muhammadali Eshonqulov; 12-11: v*.mp4 — Hasanxon domla («Alohida mavzu»)
    if f.startswith("aziz"): return "Ekspertlar gapirsin"  # 12-11: «Ekspertlar gapirsin» podkasti (boshlovchi Aziz)
    if f.startswith("v"): return "Farzand tarbiyasi"
    try: n = int(f.split("-")[0])
    except ValueError: return ""
    return "Hasanxo‘ja" if n <= 26 else "Farzand tarbiyasi" if n <= 58 else "Mohir Mirzaxmedov" if n <= 79 else "Muhammadali Eshonqulov" if n <= 91 else ""
nav = [{"fayl": x["fayl"], "vaqt": x.get("natija", {}).get("vaqt") or x["vaqt"], "holat": x["holat"], "media_id": x.get("media_id", ""), "spiker": spiker(x["fayl"]),
        "teglar": ", ".join("@" + t for t in x.get("teglar", [])), "collab": ", ".join("@" + t for t in x.get("collab", [])), "trial": "trial" if x.get("trial") else "oddiy" if x.get("oddiy_of") else ""} for x in q["navbat"]]  # 14-11: "oddiy" — trial'dan keyingi oddiy nusxa
st = [{"media_id": k, "fayl": v.get("fayl", ""), "korish": v.get("views", 0), "qamrov": v.get("reach", 0), "layk": v.get("likes", 0),
       "izoh": v.get("comments", 0), "saqlash": v.get("saved", 0), "ulashish": v.get("shares", 0)} for k, v in s.get("reels", {}).items()]
tr = [{"kun": t["kun"], "obunachi": t.get("obunachi", 0), "korish": t.get("korish", 0)} for t in s.get("tarix", [])]
pa = [{"fayl": f, "holat": "tayyor"} for f in p.get("papkada", [])] + [{"fayl": f, "holat": "captionsiz"} for f in p.get("captionsiz", [])]
# Panel bo'sh faylni "o'qib bo'lmadi" deb ko'rsatadi, shuning uchun bo'sh bo'lsa bitta belgi-qator qo'yamiz (sahifa uni yashiradi)
if not nav: nav = [{"fayl": "—", "vaqt": "", "holat": "bosh", "media_id": "", "spiker": "", "teglar": "", "collab": "", "trial": ""}]
if not st: st = [{"media_id": "-", "fayl": "—", "korish": 0, "qamrov": 0, "layk": 0, "izoh": 0, "saqlash": 0, "ulashish": 0}]
if not pa: pa = [{"fayl": "—", "holat": "bosh"}]
def akk(qf, sf, kamp):  # 22-11: Nur Brand va Haya Perfum uchun bir xil jadval
    nq = L(qf, {"navbat": []}); ns = L(sf, {})
    _r = lambda x: ns.get("reels", {}).get(x.get("media_id") or "-", {})
    rows = [{"fayl": x["fayl"], "nom": (x.get("izoh") or "").strip().split("\n")[0][:80], "vaqt": x.get("natija", {}).get("vaqt") or x.get("vaqt", ""), "holat": x["holat"],
       "media_id": x.get("media_id", ""), "korish": _r(x).get("views", ""), "layk": _r(x).get("likes", ""), "saqlash": _r(x).get("saved", ""), "ulashish": _r(x).get("shares", ""),
       "obunachi": ns.get("obunachi", ""), "kampaniya": kamp(x),
       "story": ("chiqdi" if (x.get("story_natija") or {}).get("ok") else "xato" if x.get("story_natija") else "navbatda") if x.get("story") else ""} for x in nq["navbat"]] or [{"fayl": "—", "nom": "", "vaqt": "", "holat": "bosh", "media_id": "", "korish": "", "layk": "", "saqlash": "", "ulashish": "", "obunachi": "", "kampaniya": "", "story": ""}]
    tar = [{"kun": t["kun"], "obunachi": t.get("obunachi", 0), "korish": t.get("korish", 0)} for t in ns.get("tarix", [])] or [{"kun": "", "obunachi": "", "korish": ""}]
    return rows, tar
# 22-11: kuz (nb-01..11, 10–20-noyabr) — tarix; qish (v*_montaj) — joriy
nb, nbt = akk("content/nurbrand-queue.json", "content/nurbrand-stats.json", lambda x: "kuz" if x["fayl"].startswith("nb-") else "qish")
hy, hyt = akk("content/haya-queue.json", "content/haya-stats.json", lambda x: "haya")
# 27-11: Ekspert gapirsin YouTube Shorts (content/yt-queue.json, scripts/yt_queue.py)
_yq = L("content/yt-queue.json", {"chiqdi": {}})
yt = [{"fayl": f, "sarlavha": (v.get("sarlavha") or "").replace(" #shorts", ""), "vaqt": v.get("vaqt", ""), "ok": "ha" if v.get("ok") else "xato",
       "manba": v.get("manba") or ("yangi" if f == "v37.mp4" else ""), "holat": v.get("holat", ""), "korish": v.get("korish", ""), "layk": v.get("layk", ""),
       "url": f"https://www.youtube.com/shorts/{v['id']}" if v.get("id") else ""} for f, v in _yq["chiqdi"].items()]
yt = sorted(yt, key=lambda r: r["vaqt"], reverse=True) or [{"fayl": "—", "sarlavha": "", "vaqt": "", "ok": "", "manba": "", "holat": "", "korish": "", "layk": "", "url": ""}]
_nq = L("content/reels-queue.json", {"navbat": []})
_jami = len({x["fayl"] for x in _nq["navbat"] if x.get("holat") == "chiqdi"})
yt_xulosa = [{"yuklandi": sum(1 for v in _yq["chiqdi"].values() if v.get("ok")), "jami": _jami,
              "korish": sum(int(v.get("korish") or 0) for v in _yq["chiqdi"].values()), "stat_vaqt": _yq.get("stat_vaqt", "")}]
for n, rows in [("navbat", nav), ("statistika", st), ("tarix", tr), ("papka", pa), ("nurbrand", nb), ("nurbrand_tarix", nbt), ("haya", hy), ("haya_tarix", hyt), ("youtube", yt), ("youtube_xulosa", yt_xulosa)]:
    json.dump({"rows": rows}, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
print({"navbat": len(nav), "statistika": len(st), "tarix": len(tr), "papka": len(pa), "obunachi": s.get("obunachi"), "papka_tekshirildi": p.get("tekshirildi")})
