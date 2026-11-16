# Monta site/index.html (producao, imagens em arquivo) e dist/artifact.html (preview, imagens embutidas).
import json, re, base64, urllib.parse
from pathlib import Path
base = Path(__file__).resolve().parent.parent
src = base/'src'
IMG = json.loads((base/'img_map.json').read_text())
CFG = {
  'whatsapp': '5547999714094',
  'mensagem': 'Olá, vim pelo site e gostaria de agendar minha avaliação gratuita.',
  'gtm': '',  # ex.: GTM-XXXXXXX (preencher quando tiver)
  'dominio': 'https://drviniciustrierweiler.com.br/',
}
# mensagem do WhatsApp por serviço (cards e links com ?s=servico na URL do anúncio)
MSGS = {
  '': CFG['mensagem'],
  'implante': 'Olá, vim pelo site e gostaria de agendar uma avaliação gratuita para implante.',
  'protese': 'Olá, vim pelo site e gostaria de agendar uma avaliação gratuita para prótese.',
  'lentes': 'Olá, vim pelo site e gostaria de agendar uma avaliação gratuita para lentes de contato dental.',
  'clareamento': 'Olá, vim pelo site e gostaria de agendar uma avaliação gratuita para clareamento.',
  'estetica': 'Olá, vim pelo site e gostaria de agendar uma avaliação gratuita para lentes ou clareamento.',
}
def wa(key=''): return f"https://wa.me/{CFG['whatsapp']}?text={urllib.parse.quote(MSGS[key])}"
WA = wa()
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'

# no celular a foto ocupa ~330px; 44vw faz telas 3x escolherem a versão de 520px (nítida e bem mais leve)
SIZES = {'retrato': '(max-width: 860px) 44vw, 470px'}

def render(embed):
    html = (src/'page.html').read_text()
    def img(m):
        key, alt, *rest = m.group(1).split('|')
        d = IMG[key]
        if embed:
            s = 'data:image/webp;base64,' + base64.b64encode((base/'site'/d['file']).read_bytes()).decode()
        else:
            s = d['file']
        eager = 'eager' in rest
        extra = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
        m_key = key + '-m'
        if not embed and m_key in IMG:  # versão menor para celular
            extra += f' srcset="{IMG[m_key]["file"]} {IMG[m_key]["w"]}w, {d["file"]} {d["w"]}w" sizes="{SIZES.get(key, "100vw")}"'
        cls = ''.join(f' class="{r[2:]}"' for r in rest if r.startswith('c:'))
        return f'<img src="{s}" alt="{alt}" width="{d["w"]}" height="{d["h"]}"{cls}{extra}>'
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', img, html)
    html = re.sub(r'\{\{WA:(\w+)\}\}', lambda m: wa(m.group(1)).replace('&', '&amp;'), html)
    return html.replace('{{WA}}', WA.replace('&', '&amp;')).replace('{{WA_SVG}}', WA_SVG)

def minify_css(t):
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    t = re.sub(r'\s*\n\s*', '', t)
    t = re.sub(r'\s*([{};])\s*', r'\1', t)
    return t.replace(';}', '}')
css = minify_css((src/'style.css').read_text())
js = (src/'app.js').read_text().replace('/*WA_LINKS*/{}', json.dumps({k: wa(k) for k in MSGS}, ensure_ascii=False))
js = re.sub(r'\n\s+', '\n', re.sub(r'/\*.*?\*/', '', js, flags=re.S)).strip()  # tira comentários e indentação
# fontes hospedadas no próprio site (produção); o preview usa o Google Fonts
import hashlib, shutil
(base/'site'/'fonts').mkdir(parents=True, exist_ok=True)
for f in (base/'site'/'fonts').glob('*.woff2'): f.unlink()
FONT_FILES = {}
for name in ['jakarta', 'instrument-italic']:
    data = (base/'raw'/'fonts'/f'{name}.woff2').read_bytes()
    fn = f"{name}-{hashlib.md5(data).hexdigest()[:8]}.woff2"
    (base/'site'/'fonts'/fn).write_bytes(data); FONT_FILES[name] = 'fonts/' + fn
FONTS_LOCAL = (f'<link rel="preload" as="font" type="font/woff2" href="{FONT_FILES["jakarta"]}" crossorigin>'
  f'<link rel="preload" as="font" type="font/woff2" href="{FONT_FILES["instrument-italic"]}" crossorigin>'
  '<style>'
  f'@font-face{{font-family:"Plus Jakarta Sans";src:url({FONT_FILES["jakarta"]}) format("woff2");font-weight:200 800;font-style:normal;font-display:swap}}'
  f'@font-face{{font-family:"Instrument Serif";src:url({FONT_FILES["instrument-italic"]}) format("woff2");font-weight:400;font-style:italic;font-display:swap}}'
  '</style>')
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap">'
TITLE = 'Implantes, Próteses e Lentes em Itajaí | Dr. Vinícius Trierweiler'
DESC = 'Recupere a confiança no seu sorriso. Implantes, próteses, lentes de contato dental e clareamento em Itajaí, SC, com dentista e técnico em prótese há 10 anos. Avaliação gratuita.'

schema = {
  "@context": "https://schema.org", "@type": "Dentist",
  "name": "Dr. Vinícius Trierweiler", "description": DESC, "url": CFG['dominio'],
  "telephone": "+55 47 99971-4094", "image": CFG['dominio'] + IMG['og']['file'],
  "address": {"@type": "PostalAddress", "streetAddress": "Rua Luiz da Silva, 199", "addressLocality": "Itajaí",
              "addressRegion": "SC", "postalCode": "88311-190", "addressCountry": "BR"},
  "areaServed": "Itajaí, SC",
  "hasMap": "https://www.google.com/maps/search/?api=1&query=Rua+Luiz+da+Silva+199+Cordeiros+Itaja%C3%AD+SC",
  "medicalSpecialty": "Dentistry",
  "founder": {"@type": "Person", "name": "Vinícius Gregório Trierweiler", "jobTitle": "Cirurgião-dentista", "identifier": "CRO-SC 24848"},
}
# dúvidas frequentes também vão como dados estruturados
_faq = re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', (src/'page.html').read_text(), flags=re.S)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a).strip()}} for q, a in _faq]}

# ícones, robots e sitemap
for f in (base/'raw'/'icons').iterdir(): shutil.copy(f, base/'site'/f.name)
import datetime
(base/'site'/'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nSitemap: {CFG['dominio']}sitemap.xml\n")
(base/'site'/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{CFG["dominio"]}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n</urlset>\n')
(base/'site'/'site.webmanifest').write_text(json.dumps({"name": "Dr. Vinícius Trierweiler", "short_name": "Dr. Vinícius", "start_url": "/", "display": "browser",
  "background_color": "#ffffff", "theme_color": "#ffffff", "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False))
ICONS = '<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">'
gtm_head = gtm_body = ''
if CFG['gtm']:
    gtm_head = ("<script>window.dataLayer=window.dataLayer||[];(function(){var done=false;function load(){if(done)return;done=true;"
      "dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});var s=document.createElement('script');s.async=true;"
      f"s.src='https://www.googletagmanager.com/gtm.js?id={CFG['gtm']}';document.head.appendChild(s);}}"
      "addEventListener('load',function(){setTimeout(load,1500)});['scroll','pointerdown','keydown','touchstart'].forEach(function(e){addEventListener(e,load,{once:true,passive:true})});})();</script>")
    gtm_body = f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={CFG["gtm"]}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'

prod = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{CFG['dominio']}">
{ICONS}
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:url" content="{CFG['dominio']}"><meta property="og:site_name" content="Dr. Vinícius Trierweiler">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:title" content="{TITLE}"><meta property="og:description" content="{DESC}">
<meta property="og:image" content="{CFG['dominio']}{IMG['og']['file']}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<link rel="preload" as="image" href="{IMG['retrato']['file']}" imagesrcset="{IMG['retrato-m']['file']} {IMG['retrato-m']['w']}w, {IMG['retrato']['file']} {IMG['retrato']['w']}w" imagesizes="{SIZES['retrato']}" fetchpriority="high">
{FONTS_LOCAL}
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
{gtm_head}
<style>{css}</style>
</head>
<body>
{gtm_body}
{render(False)}
<script>{js}</script>
</body>
</html>
'''
(base/'site'/'index.html').write_text(prod)
# tira de site/img o que a página não usa
for f in (base/'site'/'img').iterdir():
    if f.name not in prod: f.unlink()

art = f'''<title>Dr. Vinícius Trierweiler</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>{css}</style>
{render(True)}
<script>{js}</script>
'''
(base/'dist').mkdir(exist_ok=True)
(base/'dist'/'artifact.html').write_text(art)
print('ok', len(prod)//1024, 'KB index;', len(art)//1024, 'KB artifact')
