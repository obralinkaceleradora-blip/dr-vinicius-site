# Fonte do site (não é servida: bloqueada no .htaccess)

- `src/page.html`, `src/style.css`, `src/app.js`: conteúdo, estilo e eventos do GTM
- `tools/imgs.py`: gera `site/img/*.webp` a partir de `raw/` (fotos de pacientes já com tarja)
- `tools/build.py`: monta `site/index.html` e `dist/artifact.html`. WhatsApp, mensagem, GTM e domínio ficam no `CFG`.

Fluxo (dentro de `_fonte/`): `python3 tools/imgs.py && python3 tools/build.py`, depois copiar `site/index.html` e `site/img/` para a raiz do repo.
