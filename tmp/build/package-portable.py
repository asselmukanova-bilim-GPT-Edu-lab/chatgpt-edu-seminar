"""Create a transferable folder using the reviewed decks and local dependencies."""
from pathlib import Path
import shutil,re,zipfile,json,hashlib

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'outputs/Seminar-Portable'
DEST.mkdir(parents=True,exist_ok=True)
for part in (1,2):
 shutil.copytree(ROOT/f'part-{part}',DEST/f'part-{part}',dirs_exist_ok=True)
 for extra in ['fontawesome','plugin-import']:
  shutil.copytree(ROOT/'assets'/extra,DEST/f'part-{part}/assets'/extra,dirs_exist_ok=True)
 shutil.copy2(ROOT/'assets/prompt-activity-qr.png',DEST/f'part-{part}/assets/prompt-activity-qr.png')
for name in ['BilimAI_simulation_v2.html','Показ_на_семинаре.html']:
 shutil.copy2(ROOT/name,DEST/name)

landing=(ROOT/'index.html').read_text(encoding='utf-8')
# The portable home page opens local presentations, not online download copies.
landing=re.sub(r'<p class="small"><a href="https://github\.com/[^<]+</a></p>','',landing)
landing=landing.replace('<main>','<main><p class="small">Переносная версия · Портативті нұсқа. Открывайте этот файл после распаковки всей папки.</p>',1)
(DEST/'index.html').write_text(landing,encoding='utf-8')
readme='''СЕМИНАР CHATGPT EDU — ПЕРЕНОСНАЯ ВЕРСИЯ

1. Скопируйте ВСЮ папку Seminar-Portable на другой компьютер или флешку.
2. Если скачали ZIP: сначала извлеките весь архив в обычную папку.
3. Откройте index.html в этой папке двойным щелчком.
4. Выберите первую или вторую часть семинара.

Не переносите отдельный index.html без соседних папок.
Можно переименовать внешнюю папку Seminar-Portable. Внутренние имена и расположение файлов сохраняйте.
Установка Python, Node.js и локального сервера для показа не требуется.
Используйте современный браузер Chrome, Edge или Firefox. Для 3D-атласа необходим WebGL / аппаратное ускорение.

Без интернета доступны локальные слайды, изображения, шрифты, встроенные игры, модели и симуляция интерфейса.
Для ChatGPT/Codex, социальных сетей, Padlet, формы обратной связи и внешних источников нужен интернет.
QR-коды видны без интернета, но переход по ним открывает онлайн-сервисы.
Звук запускается после нажатия кнопки. Озвучивание синтезатором зависит от установленных голосов компьютера.

Файлы из исходной папки downloads предназначены для онлайн-загрузки ресурсов с GitHub.
В этой переносной папке их нет: открывайте именно местный index.html.
'''
(DEST/'ПРОЧИТАЙТЕ.txt').write_text(readme,encoding='utf-8-sig')

# Static local resources must resolve inside the package. Website links are allowed.
missing=[];remote=[];absolute=[]
for p in DEST.rglob('*'):
 if p.suffix not in ('.html','.css','.js'):continue
 s=p.read_text(encoding='utf-8')
 if re.search(r'file:///|["\x27]C:[/\\]',s):absolute.append(str(p.relative_to(DEST)))
 for m in re.finditer(r'(?:src|href)\s*=\s*["\x27]([^"\x27]+)|url\(\s*["\x27]?([^\s)"\x27]+)',s):
  v=next(x for x in m.groups() if x)
  if v.startswith(('data:','#','javascript:','blob:','tel:','mailto:')) or len(v)>500:continue
  if v.startswith(('https:','http:','//')):
   if m[0].startswith(('src','url')):remote.append((str(p.relative_to(DEST)),v))
   continue
  if any(x in v for x in ['${','<','+','{']):continue
  clean=v.split('?')[0].split('#')[0]
  if clean and not (p.parent/clean).exists():missing.append((str(p.relative_to(DEST)),v))
assert not missing,missing
assert not remote,remote
assert not absolute,absolute
for part in (1,2):
 s=(DEST/f'part-{part}/index.html').read_text(encoding='utf-8')
 assert '<base ' not in s
 slides=json.loads(re.search(r'const slides=(.*?);\s*const chapters=',s,re.S)[1])
 print('Part',part,'slides',len(slides))
manifest={str(p.relative_to(DEST)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in DEST.rglob('*') if p.is_file() and p.name!='manifest.sha256.json'}
(DEST/'manifest.sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT/'outputs/ChatGPT-Edu-Seminar-Portable.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(DEST.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(DEST.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('No missing static resources, remote auto-loaded resources or machine-specific paths.')
print('Files:',len(manifest),'ZIP bytes:',archive.stat().st_size)
print('Open:',DEST/'index.html')
