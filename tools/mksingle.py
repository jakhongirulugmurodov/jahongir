import sys,re,base64
out=sys.argv[1]
s=open('dist/index.html').read()
css=open('dist/assets/site.css').read()
for n in ['grain.png','grain-strong.png']:
    css=css.replace('url("%s")'%n,'url("data:image/png;base64,%s")'%base64.b64encode(open('dist/assets/'+n,'rb').read()).decode())
js=open('dist/assets/site.js').read()
import os
for dp,_,fs in os.walk('dist/media'):
    for f in sorted(fs):
        if f=='og.jpg': continue
        rel=os.path.relpath(os.path.join(dp,f),'dist')
        b64=base64.b64encode(open(os.path.join(dp,f),'rb').read()).decode()
        s=s.replace('"%s"'%rel,'"data:image/jpeg;base64,%s"'%b64)
        s=s.replace('\\"%s\\"'%rel,'\\"data:image/jpeg;base64,%s\\"'%b64)
s=re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>','',s,flags=re.I)
s=re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>','',s)
s=s.replace('<link rel="stylesheet" href="assets/site.css">','<style>\n'+css+'\n</style>')
s=s.replace('</head>','').replace('<body data-page="home">','').replace('</body>','').replace('</html>','')
s=s.replace('href="index.html#','href="#').replace('href="index.html"','href="#loyihalar"')
s=re.sub(r'<script>window\.D=(.*?);</script>', lambda m: '<script>document.body.dataset.page="home";window.D=Object.assign({single:true},'+m.group(1)+');</script>', s, count=1, flags=re.S)
s=s.replace('<script src="assets/site.js" defer></script>','<script>\n'+js.replace('</script','<\\/script')+'\n</script>')
open(out,'w').write(s); print(len(s)//1024,'KB')
