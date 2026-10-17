# Playwright helper: serve brand fonts locally in place of Google Fonts
import os
import os as _o
FD=_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'fonts')+'/'
FACES=[("Space Grotesk","space-grotesk",[400,500,700]),("Hanken Grotesk","hanken-grotesk",[400,500,600,700]),("Caveat","caveat",[500,700])]
def css():
    out=[]
    for fam,slug,ws in FACES:
        for w in ws:
            for sub in ("latin","latin-ext"):
                out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;font-display:swap;src:url(https://fonts.gstatic.com/local/{slug}-{sub}-{w}-normal.woff2) format('woff2');}}")
    return "\n".join(out)
async def route(r):
    u=r.request.url
    if u.startswith("https://fonts.googleapis.com/css"):
        return await r.fulfill(body=css(),content_type="text/css",headers={"access-control-allow-origin":"*"})
    if u.startswith("https://fonts.gstatic.com/local/"):
        f=u.rsplit("/",1)[1]; slug=f.split("-latin")[0]
        path=FD+f
        if os.path.exists(path): return await r.fulfill(path=path,content_type="font/woff2",headers={"access-control-allow-origin":"*"})
    await r.abort()
