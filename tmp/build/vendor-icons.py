from pathlib import Path
import re,urllib.request
root=Path(__file__).resolve().parents[2]
url='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
dest=root/'assets/fontawesome'
(dest/'css').mkdir(parents=True,exist_ok=True)
(dest/'webfonts').mkdir(exist_ok=True)
css=urllib.request.urlopen(url,timeout=60).read()
(dest/'css/all.min.css').write_bytes(css)
fonts=set(re.findall(r'\.\./webfonts/([^\)"\x27]+)',css.decode()))
for name in sorted(fonts):
 data=urllib.request.urlopen('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/'+name,timeout=60).read()
 (dest/'webfonts'/name).write_bytes(data)
 print(name,len(data),flush=True)
