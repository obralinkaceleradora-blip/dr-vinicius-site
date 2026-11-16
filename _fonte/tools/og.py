# Gera raw/og.png (1200x630) para a prévia de link no WhatsApp/Facebook.
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
base = Path(__file__).resolve().parent.parent
b64 = lambda p: base64.b64encode((base/p).read_bytes()).decode()
html = f'''<html><head><style>
@font-face{{font-family:J;src:url(data:font/woff2;base64,{b64("raw/fonts/jakarta.woff2")})}}
@font-face{{font-family:I;src:url(data:font/woff2;base64,{b64("raw/fonts/instrument-italic.woff2")});font-style:italic}}
body{{margin:0;width:1200px;height:630px;overflow:hidden;font-family:J;color:#12263f;
 background:radial-gradient(700px 420px at 80% 30%,#e2effc,rgba(226,239,252,0) 70%),linear-gradient(180deg,#fff,#eef5fc)}}
.copy{{position:absolute;left:72px;top:96px;width:620px}}
.pill{{display:inline-block;background:#dcebfa;color:#1b3a5f;font-weight:700;font-size:22px;padding:10px 20px;border-radius:99px}}
h1{{font-size:68px;line-height:1.05;letter-spacing:-.025em;margin:28px 0 22px;font-weight:700}}
h1 i{{font-family:I;font-weight:400;color:#1b3a5f;font-size:1.08em}}
p{{font-size:26px;color:#3d4f63;margin:0}} b{{color:#12263f}}
.arch{{position:absolute;right:70px;bottom:0;width:430px;height:470px;border-radius:999px 999px 0 0;background:linear-gradient(170deg,#d6e8fa,#b8d5f1)}}
img{{position:absolute;right:60px;bottom:0;height:600px}}
</style></head><body>
<div class="arch"></div><img src="data:image/png;base64,{b64("raw/retrato-recorte.png")}">
<div class="copy"><span class="pill">Avaliação gratuita em Itajaí</span>
<h1>Volte a sorrir <i>sem esconder os dentes.</i></h1>
<p><b>Dr. Vinícius Trierweiler</b> · CRO-SC 24848<br>Implantes, próteses, lentes e clareamento</p></div>
</body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1200,'height':630})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path=str(base/'raw'/'og.png')); b.close()
print('ok')
