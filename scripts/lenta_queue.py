# Lenta navbati: Telegram kanal postlari va Instagram karusellari. Vaqti kelgan hamma elementlarni tartib bilan joylaydi.
# Karusel elementlari sukut bo'yicha Reels bo'lib chiqadi ("format": "karusel" qo'yilsa — odatdagi karusel).
# Jadval (Jahongir): odatda kuniga 2 ta lenta posti, muhim kunlarda 4–5 tagacha. Vaqtlarni navbatga qo'yishda shu hisobga olinadi.
import json, subprocess, sys
from datetime import datetime, timezone
Q = "content/lenta-queue.json"
q = json.load(open(Q)); now = datetime.now(timezone.utc)
due = [x for x in q["navbat"] if x.get("holat") == "kutmoqda" and datetime.fromisoformat(x["vaqt"]) <= now]
if not due: print("lentada vaqti kelgan post yo'q"); sys.exit(0)
S = {"kanal": "scripts/tg_channel_post.py", "karusel": "scripts/ig_carousel.py"}
for x in sorted(due, key=lambda x: x["vaqt"]):
    if x["tur"] == "karusel" and x.get("format", "reels") == "reels":
        # Reels-birinchi: slaydlar videoga yig'ilib Reels bo'lib chiqadi (obuna bo'lmaganlarga ham ko'rinadi); o'tmasa — odatdagi karusel
        r = subprocess.run(["python3", "scripts/ig_slideshow_reel.py", x["fayl"]], capture_output=True, text=True)
        print("reels", x["fayl"], r.stdout.strip()[-300:], r.stderr.strip()[-300:])
        if r.returncode == 0:
            x["chiqdi_format"] = "reels"
        else:
            r = subprocess.run(["python3", S["karusel"], x["fayl"]], capture_output=True, text=True)
            x["chiqdi_format"] = "karusel (reels o'tmadi)"
    else:
        r = subprocess.run(["python3", S[x["tur"]], x["fayl"]], capture_output=True, text=True)
    print(x["tur"], x["fayl"], r.stdout.strip()[-300:], r.stderr.strip()[-300:])
    x["holat"] = "chiqdi" if r.returncode == 0 else "xato"
    x["natija"] = {"vaqt": datetime.now(timezone.utc).isoformat(timespec="minutes"), "chiqish": (r.stdout + r.stderr).strip()[-300:]}
json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
