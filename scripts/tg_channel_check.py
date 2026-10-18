# Bot kanalda admin ekanini va post yozish ruxsatini tekshiradi (hech narsa joylamaydi).
import json, os, sys, urllib.request, urllib.parse
T = os.environ.get("TG_BOT_TOKEN", "").strip() or sys.exit("TG_BOT_TOKEN topilmadi")
CH = os.environ.get("TG_CHANNEL", "@jahongir_on_blog")
def call(m, **p):
    try: return json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{T}/{m}", urllib.parse.urlencode(p).encode(), timeout=30))
    except urllib.error.HTTPError as e: return json.load(e)
me = call("getMe")["result"]
ch = call("getChat", chat_id=CH)
print("kanal:", json.dumps({k: ch.get("result", {}).get(k) for k in ("id", "title", "username", "type")} if ch.get("ok") else {"xato": ch.get("description")}, ensure_ascii=False))
m = call("getChatMember", chat_id=CH, user_id=me["id"])
r = m.get("result", {})
print("bot:", json.dumps({"status": r.get("status"), "can_post_messages": r.get("can_post_messages"), "can_edit_messages": r.get("can_edit_messages"), "xato": m.get("description")}, ensure_ascii=False))
