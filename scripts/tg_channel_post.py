# Telegram kanalga rasm + matn + tugma joylaydi. Foydalanish: python3 scripts/tg_channel_post.py content/kanal/<post>.json
import json, os, sys, uuid, urllib.request
T = os.environ.get("TG_BOT_TOKEN", "").strip() or sys.exit("TG_BOT_TOKEN topilmadi")
p = json.load(open(sys.argv[1])); ch = json.load(open("content/telegram.json"))["kanal"]
fields = {"chat_id": ch, "caption": p["matn"], "parse_mode": "HTML"}
if p.get("tugma"): fields["reply_markup"] = json.dumps({"inline_keyboard": [[{"text": p["tugma"], "url": p["havola"]}]]}, ensure_ascii=False)
b = uuid.uuid4().hex; body = b""
for k, v in fields.items(): body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
body += f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="p.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + open(p["rasm"], "rb").read() + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request(f"https://api.telegram.org/bot{T}/sendPhoto", body, {"Content-Type": f"multipart/form-data; boundary={b}"})
try: r = json.load(urllib.request.urlopen(req, timeout=60))
except urllib.error.HTTPError as e: r = json.load(e)
print("natija:", json.dumps({"ok": r.get("ok"), "message_id": (r.get("result") or {}).get("message_id"), "xato": r.get("description")}, ensure_ascii=False))
sys.exit(0 if r.get("ok") else 1)
