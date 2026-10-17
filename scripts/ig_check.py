# Instagram ulanishini tekshiradi. Token faqat IG_TOKEN muhit o'zgaruvchisidan olinadi, chop etilmaydi.
import json, os, sys, urllib.request, urllib.parse
T = os.environ.get("IG_TOKEN", "").strip() or sys.exit("IG_TOKEN topilmadi")
def get(path, **p):
    p["access_token"] = T
    try:
        return json.load(urllib.request.urlopen(f"https://graph.instagram.com/v23.0/{path}?" + urllib.parse.urlencode(p), timeout=30))
    except urllib.error.HTTPError as e:
        return json.load(e)
me = get("me", fields="user_id,username,account_type")
print("akkaunt:", json.dumps({k: me.get(k) for k in ("user_id", "username", "account_type")} | ({"xato": me["error"].get("message")} if "error" in me else {}), ensure_ascii=False))
lim = get(f"{me.get('user_id', 'me')}/content_publishing_limit", fields="quota_usage,config")
print("joylash limiti:", json.dumps(lim.get("data", lim.get("error", {})), ensure_ascii=False)[:300])
