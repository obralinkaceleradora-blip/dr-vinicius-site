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
  'dominio': 'https://www.SEU-DOMINIO.com.br/',
}
WA = f"https://wa.me/{CFG['whatsapp']}?text={urllib.parse.quote(CFG['mensagem'])}"
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'

def render(embed):
    html = (src/'page.html').read_text()
    def img(m):
        key, alt, *rest = m.group(1).split('|')
        d = IMG[key]
        if embed:
            s = 'data:image/webp;base64,' + base64.b64encode((base/'site'/d['file']).read_bytes()).decode()
        else:
            s = d['file']
        eager = rest and rest[0] == 'eager'
        extra = ' fetchpriority="high"' if eager else ' loading="lazy"'
        return f'<img src="{s}" alt="{alt}" width="{d["w"]}" height="{d["h"]}" decoding="async"{extra}>'
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', img, html)
    return html.replace('{{WA}}', WA.replace('&', '&amp;')).replace('{{WA_SVG}}', WA_SVG)

css = (src/'style.css').read_text()
js = (src/'app.js').read_text()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;600;700&display=swap">'
TITLE = 'Prótese Dentária e Protocolo em Itajaí | Dr. Vinícius Trierweiler'
DESC = 'Dentista e técnico em prótese há 8 anos, com laboratório próprio. Prótese total, protocolo sobre implantes e prótese parcial em Itajaí, SC. Avaliação gratuita.'

schema = {
  "@context": "https://schema.org", "@type": "Dentist",
  "name": "Dr. Vinícius Trierweiler", "description": DESC, "url": CFG['dominio'],
  "telephone": "+55 47 99971-4094", "image": CFG['dominio'] + IMG['hero']['file'],
  "address": {"@type": "PostalAddress", "streetAddress": "Rua Luiz da Silva, 199", "addressLocality": "Itajaí",
              "addressRegion": "SC", "postalCode": "88311-190", "addressCountry": "BR"},
  "areaServed": "Itajaí, SC",
}
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
<meta name="theme-color" content="#132a43">
<link rel="canonical" href="{CFG['dominio']}">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{TITLE}"><meta property="og:description" content="{DESC}">
<meta property="og:image" content="{CFG['dominio']}{IMG['hero']['file']}">
<link rel="preload" as="image" href="{IMG['hero']['file']}" fetchpriority="high">
{FONTS}
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
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
