# "Blog jadvali" paneli uchun ma'lumot: lenta navbati (kanal + karusel), story navbati, karusel natijalari, obunachilar.
# Foydalanish: python3 tools/blog_panel_data.py <chiqish papka>
import json, os, re, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
L = lambda f, d=None: json.load(open(f)) if os.path.exists(f) else d
def nom(fayl):
    d = L(fayl, {})
    if d.get("sarlavha"): return d["sarlavha"]
    m = re.search(r"<b>(.*?)</b>", d.get("matn", ""), re.S)
    return re.sub(r"^#\d+\s*·\s*", "", m.group(1)) if m else os.path.basename(fayl)
def num(fayl):
    pid = os.path.basename(fayl).replace("-ig.json", "").replace(".json", "")
    return L(f"content/posts/{pid}.json", {}).get("raqam")
rows = []
for x in L("content/lenta-queue.json", {"navbat": []})["navbat"]:
    rows.append({"id": f"{x['tur']}:{os.path.basename(x['fayl'])}", "vaqt": x["vaqt"], "joy": "Instagram karusel" if x["tur"] == "karusel" else "Telegram kanal",
                 "post": nom(x["fayl"]), "raqam": num(x["fayl"]) or "", "holat": x["holat"]})
for i, x in enumerate(L("content/story-queue.json", {"navbat": []})["navbat"]):
    rows.append({"id": f"story:{i}", "vaqt": x["vaqt"], "joy": "Story (TG + IG)", "post": x.get("sarlavha", ""), "raqam": "",
                 "holat": {"chiqdi": "chiqdi", "kutmoqda": "kutmoqda"}.get(x["holat"], x["holat"])})
st = L("content/blog-stats.json", {})
nat = [{"media_id": k, "post": nom("content/lenta/" + v["fayl"].split("/")[-1]) if os.path.exists("content/lenta/" + v["fayl"].split("/")[-1]) else v["fayl"],
        "korish": v.get("views", 0), "qamrov": v.get("reach", 0), "layk": v.get("likes", 0), "izoh": v.get("comments", 0), "saqlash": v.get("saved", 0), "ulashish": v.get("shares", 0)}
       for k, v in st.get("postlar", {}).items()]
tr = st.get("tarix", [])
for n, r in [("jadval", rows), ("natija", nat), ("obunachi", tr)]:
    json.dump({"rows": r}, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
print(len(rows), len(nat), len(tr))
