# Reels navbati (@ekspertgapirsin (avval @osish.nuqtasi; 22-11 nomi o‘zgardi)). Videolar GitHub Release'da turadi, bu skript vaqti kelganini Instagram'ga joylaydi.
# Kunlik chiqish soni ZAXIRAGA qarab (Jahongir qoidasi): zaxira = navbatda kutayotganlar + Mac papkada tayyorlar.
#   1–20 → kuniga 1 ta (20:30) · 21–40 → 2 ta (13:00, 20:30) · 41+ → 3 ta (09:00, 13:00, 20:30)
# TRIGGER rejimi (22-10 tasdiqlangan, q['rejim']='trigger' — standart): oldingi reels o'sishdan to'xtashi bilan keyingisi chiqadi:
#   kamida 3 soat o‘tgan (22-10: sinov guruhi 1–2 soatda tugaydi) + oxirgi 2 soatda soatiga <2% (kamida <5) ko'rish o'sishi (content/reels-soatlik.json; 25-10 dan); soatlik o'lchov yo'q bo'lsa 12 soatda;
#   31-10: 1,5 soatda <300 ko'rish bo'lsa (kuchsiz) — darhol keyingisi, kunlik chegaraga sanalmaydi (jami ≤6);
#   14-11: IKKI OQIM (trial ≤3/kun MANUAL + 24 soatdan keyin oddiy nusxa ≤3/kun) — pastdagi izohga qarang; quyidagi 12-11 qoidasi o'rniga.
#   12-11: TRIAL reels — kuchsiz/3 soat qoidasi qo'llanmaydi, faqat o'sish to'xtashi (yoki 6 soat); 3 ta chegaraga sanalmaydi, jami ≤6;
#   6 soatdan keyin baribir (27-10 dan; oldin 24 soat); kuniga ≤3 ta (90 lik rejadan orqada qolinsa ≤4); 23:00–08:00 chiqmaydi; zaxira <7 bo'lsa oddiy jadvalga (kuniga 1 ta, 20:30) qaytadi.
# Vaqt sinovi (22-10 tasdiqlangan, trigger yoqilgach to'xtatildi): kuniga 1 ta bo'lganda 10 ta video kunma-kun 13:00 va 20:30 da almashib chiqadi
# (har biriga "sinov_soat" yoziladi); 10 tasi chiqqach faqat 20:30 qoladi.
# Barqarorlik (tasdiqlangan): son kun boshida qotiriladi va kun davomida o'zgarmaydi;
# pastga tushish kechikadi — 2 tadan 1 taga zaxira 15 dan kam bo'lganda, 3 tadan 2 taga 35 dan kam bo'lganda qaytadi.
# Istisno: kun 0 bilan boshlangan bo'lsa (zaxira bo'sh edi), video kelishi bilan o'sha kunning o'zida ko'tariladi.
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
TZ = timezone(timedelta(hours=5)); Q = "content/reels-queue.json"
if not os.path.exists(Q): sys.exit(0)
q = json.load(open(Q)); now = datetime.now(TZ)
papka = json.load(open("content/reels-papka.json")).get("papkada", []) if os.path.exists("content/reels-papka.json") else []
SLOTS = {1: [(20, 30)], 2: [(13, 0), (20, 30)], 3: [(9, 0), (13, 0), (20, 30)]}
TRIG = q.get("rejim", "trigger") == "trigger"
SINOV = 0 if TRIG else 10 - sum(1 for x in q["navbat"] if x.get("sinov_soat"))
def slots(n, day):
    if n == 1 and SINOV > 0: return [(13, 0)] if day.toordinal() % 2 == 0 else [(20, 30)]
    return SLOTS.get(n, [])
def kvota(z, oldingi=0):
    n = 3 if z >= 41 else 2 if z >= 21 else 1 if z >= 1 else 0
    if z >= 1:
        if oldingi >= 3 and z >= 35: n = max(n, 3)
        if oldingi >= 2 and z >= 15: n = max(n, 2)
    return n
kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
zaxira = len(kut) + len(papka)
old = q.get("kunlik", {}); bugun_s = now.date().isoformat()
if old.get("kun") == bugun_s:
    n = old.get("kuniga", 0)
    if n == 0 and zaxira: n = kvota(zaxira, old.get("oldingi", 0))
else:
    n = kvota(zaxira, old.get("kuniga", 0))
bugun = [x for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ).date() == now.date()]
# Oylik reja (26-10): 19-10 – 18-11 da 90 ta. Kunlik chegara 3 ta; rejadan orqada qolinsa (qolgan ÷ qolgan kun > 3) o'sha kuni 4 tagacha.
REJA_OXIRI, REJA_SONI = datetime(2026, 11, 18, tzinfo=TZ).date(), 90
oldin = sum(1 for x in q["navbat"] if x.get("holat") == "chiqdi" and datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ).date() < now.date())
qolgan_kun = (REJA_OXIRI - now.date()).days + 1
CAP = min(4, max(3, -(-(REJA_SONI - oldin) // qolgan_kun))) if qolgan_kun > 0 and oldin < REJA_SONI else 3
due = [now.replace(hour=h, minute=m, second=0, microsecond=0) for h, m in slots(n, now.date())]
kerak = sum(1 for t in due if t <= now) - len(bugun)
SOAT = json.load(open("content/reels-soatlik.json")) if os.path.exists("content/reels-soatlik.json") else {}
chiq = [x for x in q["navbat"] if x.get("holat") == "chiqdi" and x.get("natija", {}).get("vaqt")]
oxirgi = max(chiq, key=lambda x: datetime.fromisoformat(x["natija"]["vaqt"])) if chiq else None
KUCHSIZ, MAKS_KUN, T_CAP, O_CAP = 300, 6, 3, 3
# 14-11 (Jahongir, "boshla"): IKKI OQIM. 1) TRIAL — yangi video avval trial (MANUAL: Instagram o'zi ochmaydi), kuniga ≤3 ta;
#    keyingi trial oldingi trial'ning ko'rishi o'sishdan to'xtashi bilan (oxirgi 2 o'lchovda soatiga <2%, kamida <5) yoki 6 soatda.
# 2) ODDIY — har bir trial chiqqanidan kamida 24 soat keyin o'sha video oddiy post bo'lib qayta chiqadi ("oddiy_of" = trial media_id,
#    "erta" = eng erta vaqt), trial natijasidan qat'i nazar; kuniga ≤3 ta, oldingi oddiy postdan 3–6 soat keyin (o'sish to'xtasa
#    yoki 1,5 soatda <300 ko'rish bo'lsa — oldinroq). Bir ishga tushishda ko'pi bilan 1 ta post; ikkalasi tayyor bo'lsa oddiy oldin. 23–08 chiqmaydi.
is_tr = lambda x: bool(x.get("trial"))
def oxir(cond):
    c = [x for x in chiq if cond(x)]
    return max(c, key=lambda x: datetime.fromisoformat(x["natija"]["vaqt"])) if c else None
def toxtadi(x, min_h, kuchsiz=False):
    if not x: return 1, "birinchi"
    h = (now - datetime.fromisoformat(x["natija"]["vaqt"])).total_seconds() / 3600
    rows = SOAT.get(x.get("media_id") or "", {}).get("olchov", [])
    if kuchsiz and h >= 1.5 and rows and rows[-1].get("views", 0) < KUCHSIZ: return 1, f"kuchsiz: {h:.1f} soatda {rows[-1].get('views', 0)} ko'rish"
    if h < min_h: return 0, f"oxirgisiga {h:.1f} soat"
    if h >= 6: return 1, f"{h:.1f} soat o'tdi"
    if len(rows) < 3: return 0, f"o'lchov kam ({len(rows)})"
    a_, b_, c_ = [r.get("views", 0) for r in rows[-3:]]
    lim = max(5, c_ * 0.02)
    return (1, f"to'xtadi: +{b_ - a_}, +{c_ - b_} (chegara {lim:.0f})") if (b_ - a_) < lim and (c_ - b_) < lim else (0, f"o'syapti: +{b_ - a_}, +{c_ - b_} (chegara {lim:.0f})")
tanlov = None
# 17-11 (Jahongir, "ishni boshla"): BITTA OQIM, 24/7. Trial'dan keyin qayta yuklash bekor (takror fayl qamrovni tushirdi: v2 trialda 1935, oddiyda 81).
# Har video to'g'ridan-to'g'ri oddiy post; keyingisi oxirgi postning ko'rishi o'sishdan to'xtashi bilan (oxirgi 2 o'lchovda soatiga <2%, kamida <5;
# kamida 2 soat, ko'pi bilan 6 soat). Tungi tanaffus yo'q, "kuchsiz" qoidasi yo'q. Himoya: kuniga jami ≤8 ta.
# "trial" maydoni faqat qo'lda qo'yilgan sinovlar uchun qoladi — trial bo'lgan video keyin oddiy post qilinmaydi.
MAKS_KUN = 8
def trigger_kerak():
    if len(bugun) >= MAKS_KUN: return 0, f"kunlik jami {MAKS_KUN} ta"
    k, sb = toxtadi(oxirgi, 2)
    return k, sb
TRIG_ON = TRIG and zaxira >= 7
if TRIG_ON: kerak, sabab = trigger_kerak(); print("trigger:", sabab)
q["kunlik"] = {"rejim": "trigger" if TRIG_ON else "jadval", "zaxira": zaxira, "kuniga": n, "kun": bugun_s, "oldingi": old.get("oldingi", 0) if old.get("kun") == bugun_s else old.get("kuniga", 0), "yangilandi": now.isoformat(timespec="minutes")}
def joyla(x):
    os.makedirs("/tmp/reel", exist_ok=True)
    url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'jakhongirulugmurodov/jahongir')}/releases/download/{x['release']}/{x['fayl']}"
    open("/tmp/reel/cap.txt", "w").write(x["izoh"])
    env = {**os.environ, "IG_USER_TAGS": ",".join(x.get("teglar", [])), "IG_COLLABS": ",".join(x.get("collab", [])), "IG_TRIAL": x.get("trial", "")}  # "teglar": ["hasankhoja"], "collab": ["mohirustoz"]
    r = subprocess.run(["python3", "scripts/ig_reel.py", url, "/tmp/reel/cap.txt"], capture_output=True, text=True, env=env)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(TZ).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-200:]}
    m = re.search(r'"id": "(\d+)"', r.stdout)
    if m: x["media_id"] = m.group(1)
darhol = [x for x in kut if x.get("darhol")]  # qo'lda "darhol": true qo'yilgani jadvalni kutmaydi (masalan, test)
if darhol:
    joyla(darhol[0]); darhol[0].pop("darhol", None); kerak = 0
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
elif kerak > 0 and kut:
    joyla(tanlov or kut[0])  # bir ishga tushishda ko'pi bilan 1 ta
    if n == 1 and SINOV > 0: kut[0]["sinov_soat"] = "%02d:%02d" % slots(n, now.date())[0]
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
# taxminiy jadval (trigger, 27-10): oldingisidan 3–6 soat keyin — taxminan har 6 soatda, kuniga ≤3 ta, faqat 08:00–23:00
# (aniq vaqtni o'sish hal qiladi: video tez to'xtasa, keyingisi oldinroq chiqadi)
if TRIG_ON:  # 17-11: bitta oqim, 24/7 — taxminan har 3 soatda, kuniga ≤8 ta (aniq vaqtni o'sish hal qiladi)
    kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
    chiq2 = [x for x in q["navbat"] if x.get("holat") == "chiqdi" and x.get("natija", {}).get("vaqt")]
    ox = max(chiq2, key=lambda x: datetime.fromisoformat(x["natija"]["vaqt"])) if chiq2 else None
    t = max(now, datetime.fromisoformat(ox["natija"]["vaqt"]).astimezone(TZ) + timedelta(hours=3)) if ox else now
    sanoq = {now.date(): sum(1 for x in q["navbat"] if x.get("holat") in ("chiqdi", "xato") and datetime.fromisoformat(x["natija"]["vaqt"]).astimezone(TZ).date() == now.date())}
    for x in kut:
        while sanoq.get(t.date(), 0) >= MAKS_KUN: t = (t + timedelta(days=1)).replace(hour=0, minute=0)
        x["vaqt"] = t.isoformat(timespec="minutes"); sanoq[t.date()] = sanoq.get(t.date(), 0) + 1; t += timedelta(hours=3)
    kut = []
# taxminiy jadval: qolganlarni kvota bo'yicha keyingi slotlarga taqsimlash
t = now; i = 0; posted_today = len(bugun) + (1 if kerak > 0 else 0)
day = now.date(); used = posted_today
while i < len(kut) and n:
    sl = slots(n, day)
    for h, mi in sl:
        s = datetime(day.year, day.month, day.day, h, mi, tzinfo=TZ)
        if s <= now or (day == now.date() and used > 0 and sl.index((h, mi)) < used): continue
        if i >= len(kut): break
        kut[i]["vaqt"] = s.isoformat(timespec="minutes"); i += 1
    day = day + timedelta(days=1); used = 0
print(f"zaxira {zaxira}, kuniga {n}, bugun chiqqan {len(bugun)}, hozir kerak {max(kerak,0)}")
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
