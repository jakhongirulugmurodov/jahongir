# Telegram Business orqali @sp_business_agency profiliga story joylaydi.
# Foydalanish: python3 scripts/tg_story.py <rasm.jpg> <havola> <x% y% w% h%> [soat]
# Token faqat TG_BOT_TOKEN muhit o'zgaruvchisidan olinadi va chop etilmaydi.
import json, os, sys, uuid, urllib.request

T = os.environ.get("TG_BOT_TOKEN", "").strip() or sys.exit("TG_BOT_TOKEN topilmadi")
img, url, x, y, w, h = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:7])
hours = int(sys.argv[7]) if len(sys.argv) > 7 else 24
bc = json.load(open("content/telegram.json"))["business_connection_id"]

fields = {
    "business_connection_id": bc,
    "content": json.dumps({"type": "photo", "photo": "attach://story"}),
    "active_period": str(hours * 3600),
    "areas": json.dumps([{"position": {"x_percentage": x, "y_percentage": y, "width_percentage": w, "height_percentage": h, "rotation_angle": 0, "corner_radius_percentage": 50}, "type": {"type": "link", "url": url}}]),
}
b = uuid.uuid4().hex
body = b""
for k, v in fields.items():
    body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
body += f'--{b}\r\nContent-Disposition: form-data; name="story"; filename="story.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + open(img, "rb").read() + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request(f"https://api.telegram.org/bot{T}/postStory", body, {"Content-Type": f"multipart/form-data; boundary={b}"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=60))
except urllib.error.HTTPError as e:
    r = json.load(e)
print("natija:", json.dumps({"ok": r.get("ok"), "id": (r.get("result") or {}).get("id"), "xato": r.get("description")}, ensure_ascii=False))
sys.exit(0 if r.get("ok") else 1)
