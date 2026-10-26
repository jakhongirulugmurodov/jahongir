# Telegram botdagi bitta tugma: "▶️ Reels hozir chiqsin" → navbatdagi birinchi reels "darhol" belgilanadi, shu daqiqada reels_queue.py joylaydi.
# Claude ishtirok etmaydi. Navbat soqchisi har daqiqada chaqiradi. Token faqat TG_BOT_TOKEN dan, chop etilmaydi.
# Faqat bot Business ulangan akkaunt egasi (content/telegram.json dagi business_connection_id egasi) buyruq bera oladi.
# Buyruqlar (botga shaxsiy yozishmada): /start yoki /panel — tugmali xabar; /chiqar — darhol chiqarish; tugmani bosish — darhol chiqarish.
import json, os, sys, urllib.request, urllib.parse
T = os.environ.get("TG_BOT_TOKEN", "").strip() or sys.exit(0)
Q, S, C = "content/reels-queue.json", "content/tg-buyruq.json", "content/telegram.json"
st = json.load(open(S)) if os.path.exists(S) else {}
def call(m, **p):
    data = urllib.parse.urlencode({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in p.items()}).encode()
    try: return json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{T}/{m}", data, timeout=30))
    except urllib.error.HTTPError as e:
        try: return json.load(e)
        except Exception: return {}
    except Exception: return {}
bc = json.load(open(C)).get("business_connection_id")  # egasining ID'si repoga yozilmaydi — har safar Telegram'dan olinadi
ega = (call("getBusinessConnection", business_connection_id=bc).get("result") or {}).get("user", {}).get("id") if bc else None
if not ega: sys.exit(0)
u = call("getUpdates", offset=st.get("offset", 0), timeout=0, allowed_updates=["message", "callback_query"])
if not u.get("ok"): sys.exit(0)
TUGMA = {"inline_keyboard": [[{"text": "▶️ Reels hozir chiqsin", "callback_data": "chiqar"}]]}
def chiqar():
    q = json.load(open(Q)); kut = [x for x in q["navbat"] if x.get("holat") == "kutmoqda"]
    if not kut: return "Navbat bo‘sh — chiqadigan reels yo‘q."
    d = next((x for x in kut if x.get("darhol")), None)
    if d: return f"{d['fayl']} allaqachon chiqish arafasida (1–2 daqiqa)."
    kut[0]["darhol"] = True; json.dump(q, open(Q, "w"), ensure_ascii=False, indent=2)
    return f"✅ {kut[0]['fayl']} 1–2 daqiqada @osish.nuqtasi sahifasida chiqadi. Qolgan navbat: {len(kut) - 1} ta."
for x in u["result"]:
    st["offset"] = x["update_id"] + 1
    if "callback_query" in x:
        cq = x["callback_query"]
        if cq.get("from", {}).get("id") != ega or cq.get("data") != "chiqar":
            call("answerCallbackQuery", callback_query_id=cq["id"]); continue
        javob = chiqar(); call("answerCallbackQuery", callback_query_id=cq["id"], text=javob[:190])
        call("sendMessage", chat_id=ega, text=javob, reply_markup=TUGMA)
    elif "message" in x:
        m = x["message"]; txt = (m.get("text") or "").strip().lower()
        if m.get("chat", {}).get("type") != "private" or m.get("from", {}).get("id") != ega: continue
        if txt.startswith("/chiqar") or txt == "/start chiqar":
            call("sendMessage", chat_id=ega, text=chiqar(), reply_markup=TUGMA)
        elif txt.startswith("/start") or txt.startswith("/panel"):
            call("sendMessage", chat_id=ega, text="O‘sish Nuqtasi reels navbati. Tugmani bossangiz, navbatdagi reels 1–2 daqiqada chiqadi. Bu xabarni qadab (pin) qo‘ying.", reply_markup=TUGMA)
json.dump(st, open(S, "w"), ensure_ascii=False, indent=1)
