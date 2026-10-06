"""Package the already reviewed decks without rebuilding their slide content."""
from pathlib import Path
import json, re, sys, zipfile

ROOT=Path(__file__).resolve().parents[2]
SITE='https://asselmukanova-bilim-gpt-edu-lab.github.io/chatgpt-edu-seminar/'
RELEASE='https://github.com/asselmukanova-bilim-GPT-Edu-lab/chatgpt-edu-seminar/releases/download/seminar-2026-10-06/'
(ROOT/'downloads').mkdir(exist_ok=True)
(ROOT/'outputs').mkdir(exist_ok=True)
for part in ([int(sys.argv[1])] if len(sys.argv)>1 else (1,2)):
    folder=ROOT/f'part-{part}'
    source=(folder/'index.html').read_text(encoding='utf-8')
    slides=json.loads(re.search(r'const slides=(.*?);\s*const chapters=',source,re.S).group(1))
    assert len(slides)==(18 if part==1 else 27)
    # All relative URLs, including those constructed by JavaScript, resolve to
    # the published resource directory when this HTML is opened from Downloads.
    downloadable=re.sub(r'<head\b[^>]*>',lambda m:m.group(0)+f'\n<base href="{SITE}part-{part}/">\n',source,count=1,flags=re.I)
    assert downloadable!=source
    downloadable=downloadable.replace('can be bundled, embedded, \n','can be bundled, embedded,\n')
    html_name=f'ChatGPT-Edu-Part-{part}.html'
    (ROOT/'downloads'/html_name).write_text(downloadable,encoding='utf-8')
    zip_path=ROOT/'outputs'/f'ChatGPT-Edu-Part-{part}.zip'
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as package:
        for file in sorted(folder.rglob('*')):
            if file.is_file(): package.write(file,file.relative_to(ROOT).as_posix())
        for name in ['BilimAI_simulation_v2.html','Показ_на_семинаре.html']:
            package.write(ROOT/name,name)
        package.writestr('ОТКРОЙТЕ.txt',f'ChatGPT Edu — часть {part}\nРаспакуйте весь архив. Откройте part-{part}/index.html в браузере.\nСлайдов: {len(slides)}. Переключатель RU / KK.\nНе перемещайте index.html отдельно от папок. Внешние сайты и онлайн-сервисы требуют интернет.\n')
    with zipfile.ZipFile(zip_path) as package: assert package.testzip() is None
    print(f'Part {part}: {len(slides)} slides; HTML {(ROOT/"downloads"/html_name).stat().st_size:,} bytes; ZIP {zip_path.stat().st_size:,} bytes')

landing=ROOT/'index.html'; text=landing.read_text(encoding='utf-8')
for part in (1,2):
    anchor=f'<a href="part-{part}/index.html">Открыть / Ашу →</a>'
    extra=f'<p class="small"><a href="{RELEASE}ChatGPT-Edu-Part-{part}.html">Скачать HTML / HTML жүктеу</a></p><p class="small"><a href="{RELEASE}ChatGPT-Edu-Part-{part}.zip" style="background:#eceaff;color:#3530ff">Архив с ресурсами / Ресурстар мұрағаты</a></p>'
    if extra not in text: text=text.replace(anchor,anchor+extra)
landing.write_text(text,encoding='utf-8')
