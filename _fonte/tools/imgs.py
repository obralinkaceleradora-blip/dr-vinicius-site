# Gera as imagens do site a partir das extraidas do PDF (raw/). Saida: site/img/<nome>-<hash>.webp + img_map.json
import json, hashlib, glob, sys
from pathlib import Path
from PIL import Image
base = Path(__file__).resolve().parent.parent
raw, out = base/'raw', base/'site'/'img'
out.mkdir(parents=True, exist_ok=True)
for f in list(out.glob('*.webp')) + list(out.glob('*.jpg')): f.unlink()
def src(n): return Image.open(glob.glob(str(raw/f'img-{n}.*'))[0]).convert('RGB')
jobs = {}
TARJA = {'039':(170,395,560,455),'040':(170,362,560,442),'041':(170,370,520,435)}
# antes/depois: colagens de print (barra preta em cima/embaixo), metade de cima = antes
for i, n in enumerate(['028','029','030'], 1):
    im = src(n).crop((0,103,532,1049)); h = im.height//2
    jobs[f'caso{i}-antes'] = im.crop((0,0,532,h)); jobs[f'caso{i}-depois'] = im.crop((0,h,532,im.height))
from PIL import ImageDraw
def tarja(im, box):
    # cobre os olhos (no PDF a tarja era um objeto separado e nao vem na imagem extraida)
    ImageDraw.Draw(im).rectangle(box, fill=(0,0,0)); return im
jobs['caso4-antes'] = tarja(src('039'), TARJA['039']); jobs['caso4-depois'] = tarja(src('040'), TARJA['040'])
jobs['paciente-5'] = tarja(src('041'), TARJA['041']); jobs['paciente-6'] = src('238')
jobs['vinicius-lab'] = src('217').crop((0,150,532,1049))
jobs['vinicius'] = src('001')
pick = {'hero':'084','protocolo':'063','total':'085','ppr':'129','placa':'140',
 'g1':'061','g2':'073','g3':'193','g4':'195','g5':'302','g6':'182','g7':'279','g8':'301','g9':'074','g10':'162','g11':'173','g12':'083'}
for k,n in pick.items(): jobs[k] = src(n)
jobs['retrato'] = Image.open(raw/'retrato-recorte.png').convert('RGBA')
for k,f,h in [('logo-dr','logo-dr-escuro.png',96),('logo-maestria','logo-maestria.png',120)]:
    im = Image.open(raw/f).convert('RGBA'); jobs[k] = im.resize((round(im.width*h/im.height), h), Image.LANCZOS)
jobs['lentes'] = Image.open(raw/'capa-lentes.jpg').convert('RGB')  # capa do card de lentes
jobs['protese-capa'] = Image.open(raw/'capa-protese.jpg').convert('RGB').crop((85, 242, 1045, 1058))  # capa do card de próteses
jobs['retrato-m'] = jobs['retrato'].resize((520, round(jobs['retrato'].height*520/jobs['retrato'].width)), Image.LANCZOS)
og = raw/'og.png'
m = {}
for k, im in jobs.items():
    if k == 'retrato': im = im.resize((780, 1040), Image.LANCZOS)
    elif im.width > 640 and not k.startswith(('logo', 'retrato')):  # nenhuma foto aparece maior que ~400px na página
        im = im.resize((640, round(im.height*640/im.width)), Image.LANCZOS)
    tmp = out/'_tmp.webp'; im.save(tmp, 'WEBP', quality=78, method=6)
    h = hashlib.md5(tmp.read_bytes()).hexdigest()[:8]
    name = f'{k}-{h}.webp'; tmp.rename(out/name)
    m[k] = {'file': f'img/{name}', 'w': im.width, 'h': im.height}
if og.exists():  # imagem de compartilhamento (WhatsApp/Facebook) em JPG
    im = Image.open(og).convert('RGB'); tmp = out/'_og.jpg'; im.save(tmp, 'JPEG', quality=86, optimize=True, progressive=True)
    h = hashlib.md5(tmp.read_bytes()).hexdigest()[:8]; tmp.rename(out/f'og-{h}.jpg')
    m['og'] = {'file': f'img/og-{h}.jpg', 'w': im.width, 'h': im.height}
(base/'img_map.json').write_text(json.dumps(m, indent=1))
print(len(m), 'imagens', sum((out/v['file'][4:]).stat().st_size for v in m.values())//1024, 'KB')
