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
nq = L("content/nurbrand-queue.json", {"navbat": []}); ns = L("content/nurbrand-stats.json", {})  # 10-11: @nur_brand_uzb
def _r(x): return ns.get("reels", {}).get(x.get("media_id") or "-", {})
nb = [{"fayl": x["fayl"], "nom": (x.get("izoh") or "").strip().split("\n")[0][:80], "vaqt": x.get("natija", {}).get("vaqt") or x.get("vaqt", ""), "holat": x["holat"],
       "media_id": x.get("media_id", ""), "korish": _r(x).get("views", ""), "layk": _r(x).get("likes", ""), "saqlash": _r(x).get("saved", ""), "ulashish": _r(x).get("shares", ""),
       "obunachi": ns.get("obunachi", ""),
       "kampaniya": "kuz" if x["fayl"].startswith("nb-") else "qish",  # 22-11: kuz (nb-01..11, 10–20-noyabr) — tarix; qish (v*_montaj) — joriy
       "story": ("chiqdi" if (x.get("story_natija") or {}).get("ok") else "xato" if x.get("story_natija") else "navbatda") if x.get("story") else ""} for x in nq["navbat"]] or [{"fayl": "—", "nom": "", "vaqt": "", "holat": "bosh", "media_id": "", "korish": "", "layk": "", "saqlash": "", "ulashish": "", "obunachi": "", "kampaniya": "", "story": ""}]
nbt = [{"kun": t["kun"], "obunachi": t.get("obunachi", 0), "korish": t.get("korish", 0)} for t in ns.get("tarix", [])] or [{"kun": "", "obunachi": "", "korish": ""}]
for n, rows in [("navbat", nav), ("statistika", st), ("tarix", tr), ("papka", pa), ("nurbrand", nb), ("nurbrand_tarix", nbt)]:
    json.dump({"rows": rows}, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
print({"navbat": len(nav), "statistika": len(st), "tarix": len(tr), "papka": len(pa), "obunachi": s.get("obunachi"), "papka_tekshirildi": p.get("tekshirildi")})
