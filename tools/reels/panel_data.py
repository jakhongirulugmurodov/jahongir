# "90 Reels" paneli uchun ma'lumot fayllari: content/reels-*.json → 4 ta qator-JSON (navbat, statistika, tarix, papka).
# Foydalanish: python3 tools/reels/panel_data.py <chiqish papka>
import json, os, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
L = lambda f, d: json.load(open(f)) if os.path.exists(f) else d
q = L("content/reels-queue.json", {"navbat": []}); s = L("content/reels-stats.json", {}); p = L("content/reels-papka.json", {})
def spiker(f):  # 26-10 Jahongir: ≤26 Hasanxo‘ja, 27–58 farzand tarbiyasi suhbati, 59–79 Mohir Mirzaxmedov, 80–91 Muhammadali Eshonqulov
    try: n = int(f.split("-")[0])
    except ValueError: return ""
    return "Hasanxo‘ja" if n <= 26 else "Farzand tarbiyasi" if n <= 58 else "Mohir Mirzaxmedov" if n <= 79 else "Muhammadali Eshonqulov" if n <= 91 else ""
nav = [{"fayl": x["fayl"], "vaqt": x.get("natija", {}).get("vaqt") or x["vaqt"], "holat": x["holat"], "media_id": x.get("media_id", ""), "spiker": spiker(x["fayl"]),
        "teglar": ", ".join("@" + t for t in x.get("teglar", [])), "collab": ", ".join("@" + t for t in x.get("collab", []))} for x in q["navbat"]]
st = [{"media_id": k, "fayl": v.get("fayl", ""), "korish": v.get("views", 0), "qamrov": v.get("reach", 0), "layk": v.get("likes", 0),
       "izoh": v.get("comments", 0), "saqlash": v.get("saved", 0), "ulashish": v.get("shares", 0)} for k, v in s.get("reels", {}).items()]
tr = [{"kun": t["kun"], "obunachi": t.get("obunachi", 0), "korish": t.get("korish", 0)} for t in s.get("tarix", [])]
pa = [{"fayl": f, "holat": "tayyor"} for f in p.get("papkada", [])] + [{"fayl": f, "holat": "captionsiz"} for f in p.get("captionsiz", [])]
# Panel bo'sh faylni "o'qib bo'lmadi" deb ko'rsatadi, shuning uchun bo'sh bo'lsa bitta belgi-qator qo'yamiz (sahifa uni yashiradi)
if not nav: nav = [{"fayl": "—", "vaqt": "", "holat": "bosh", "media_id": "", "spiker": "", "teglar": "", "collab": ""}]
if not st: st = [{"media_id": "-", "fayl": "—", "korish": 0, "qamrov": 0, "layk": 0, "izoh": 0, "saqlash": 0, "ulashish": 0}]
if not pa: pa = [{"fayl": "—", "holat": "bosh"}]
cq = L("content/cinematic-queue.json", {"navbat": []})  # @cinematic.soul52 — alohida navbat (2 haftada 100 ta)
cin = [{"fayl": x["fayl"], "vaqt": x.get("natija", {}).get("vaqt") or x.get("vaqt", ""), "holat": x["holat"], "media_id": x.get("media_id", "")} for x in cq["navbat"]] or [{"fayl": "—", "vaqt": "", "holat": "bosh", "media_id": ""}]
for n, rows in [("navbat", nav), ("statistika", st), ("tarix", tr), ("papka", pa), ("cinematic", cin)]:
    json.dump({"rows": rows}, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
print({"navbat": len(nav), "statistika": len(st), "tarix": len(tr), "papka": len(pa), "obunachi": s.get("obunachi"), "papka_tekshirildi": p.get("tekshirildi")})
