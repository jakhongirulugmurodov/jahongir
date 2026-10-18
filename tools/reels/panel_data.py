# "90 Reels" paneli uchun ma'lumot fayllari: content/reels-*.json → 4 ta qator-JSON (navbat, statistika, tarix, papka).
# Foydalanish: python3 tools/reels/panel_data.py <chiqish papka>
import json, os, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
L = lambda f, d: json.load(open(f)) if os.path.exists(f) else d
q = L("content/reels-queue.json", {"navbat": []}); s = L("content/reels-stats.json", {}); p = L("content/reels-papka.json", {})
nav = [{"fayl": x["fayl"], "vaqt": x["vaqt"], "holat": x["holat"], "media_id": x.get("media_id", "")} for x in q["navbat"]]
st = [{"media_id": k, "fayl": v.get("fayl", ""), "korish": v.get("views", 0), "qamrov": v.get("reach", 0), "layk": v.get("likes", 0),
       "izoh": v.get("comments", 0), "saqlash": v.get("saved", 0), "ulashish": v.get("shares", 0)} for k, v in s.get("reels", {}).items()]
tr = [{"kun": t["kun"], "obunachi": t.get("obunachi", 0), "korish": t.get("korish", 0)} for t in s.get("tarix", [])]
pa = [{"fayl": f, "holat": "tayyor"} for f in p.get("papkada", [])] + [{"fayl": f, "holat": "captionsiz"} for f in p.get("captionsiz", [])]
for n, rows in [("navbat", nav), ("statistika", st), ("tarix", tr), ("papka", pa)]:
    json.dump({"rows": rows}, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
print({"navbat": len(nav), "statistika": len(st), "tarix": len(tr), "papka": len(pa), "obunachi": s.get("obunachi"), "papka_tekshirildi": p.get("tekshirildi")})
