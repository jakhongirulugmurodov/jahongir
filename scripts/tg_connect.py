# Telegram Business ulanishini topadi: business_connection_id va story ruxsatini tekshiradi.
# Token faqat TG_BOT_TOKEN muhit o'zgaruvchisidan olinadi va hech qachon chop etilmaydi.
import json, os, sys, urllib.request, urllib.parse

T = os.environ.get("TG_BOT_TOKEN", "").strip()
if not T:
    sys.exit("TG_BOT_TOKEN secret topilmadi")

def call(m, **p):
    data = urllib.parse.urlencode({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in p.items()}).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{T}/{m}", data, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return json.load(e)

me = call("getMe")
print("bot:", me.get("ok"), me.get("result", {}).get("username"), "| business:", me.get("result", {}).get("can_connect_to_business"))
wh = call("getWebhookInfo").get("result", {})
print("webhook o'rnatilganmi:", bool(wh.get("url")))
u = call("getUpdates", allowed_updates=["business_connection"], timeout=0)
if not u.get("ok"):
    sys.exit("getUpdates xato: " + str(u.get("description")))
bcs = [x["business_connection"] for x in u["result"] if "business_connection" in x]
print("topilgan ulanishlar:", len(bcs))
for b in bcs:
    r = b.get("rights", {})
    print(json.dumps({"id": b["id"], "user": b["user"].get("username"), "enabled": b.get("is_enabled"), "can_manage_stories": r.get("can_manage_stories"), "can_reply": r.get("can_reply"), "rights": sorted(k for k, v in r.items() if v)}, ensure_ascii=False))
if bcs:
    open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a").write(f"bc={bcs[-1]['id']}\n")
