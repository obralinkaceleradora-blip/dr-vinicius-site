/* Eventos para o GTM (dataLayer): clique_whatsapp, clique_mapa, abriu_faq, comparou_antes_depois, servico_campanha */
(function(){
  var dl = window.dataLayer = window.dataLayer || [];
  var doc = document, root = doc.documentElement;
  var mq = function(q){ return window.matchMedia ? matchMedia(q) : {matches:false}; };
  var reduce = mq('(prefers-reduced-motion: reduce)'), phone = mq('(max-width: 560px)');
  var all = function(sel, el){ return Array.prototype.slice.call((el || doc).querySelectorAll(sel)); };
  var hasIO = 'IntersectionObserver' in window;
  function once(els, fn, th){
    if(!hasIO){ els.forEach(fn); return; }
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); fn(e.target); } }); }, {threshold: th || .5});
    els.forEach(function(el){ io.observe(el); });
  }

  /* cliques */
  doc.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[data-wa],a[data-mapa]');
    if(a) dl.push(a.dataset.wa ? {event:'clique_whatsapp', wa_origem:a.dataset.wa} : {event:'clique_mapa'});
    var s = e.target.closest && e.target.closest('.faq summary');
    if(s && !s.parentNode.open) dl.push({event:'abriu_faq', pergunta:s.textContent});
  });

  /* Título e WhatsApp por campanha: ?s=implante | protese | lentes | clareamento | estetica */
  (function(){
    var LINKS = /*WA_LINKS*/{};
    var HERO = {
      implante:   ['Implantes dentários em Itajaí', 'Volte a mastigar e sorrir <span class="serif mark">com firmeza.</span>', 'Implantes com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos. Planejamento cuidadoso em cada detalhe.'],
      protese:    ['Próteses dentárias em Itajaí', 'Sua prótese confortável, natural <span class="serif mark">e feita sob medida.</span>', 'O Dr. Vinícius é cirurgião-dentista e técnico em prótese há 10 anos. Avalia o seu caso, confecciona a prótese no laboratório próprio e acompanha cada ajuste.'],
      lentes:     ['Lentes de contato dental em Itajaí', 'Um sorriso mais harmônico, <span class="serif mark">com naturalidade.</span>', 'Lentes de contato dental planejadas para o seu rosto pelo Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos.'],
      clareamento:['Clareamento dental em Itajaí', 'Dentes mais claros para <span class="serif mark">sorrir sem receio.</span>', 'Clareamento com acompanhamento profissional do Dr. Vinícius, do início ao fim, ajustado ao seu caso.'],
      estetica:   ['Lentes e clareamento em Itajaí', 'Estética do sorriso <span class="serif mark">com naturalidade.</span>', 'Lentes de contato dental e clareamento com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos.']
    };
    var s = '';
    try { s = (new URLSearchParams(location.search).get('s') || '').toLowerCase(); } catch(e){}
    if(!HERO[s]) return;
    var h = HERO[s];
    doc.getElementById('h-pill').textContent = h[0];
    doc.getElementById('h-title').innerHTML = h[1];
    doc.getElementById('h-lead').textContent = h[2];
    all('a[data-wa]').forEach(function(a){ if(!a.closest('.t-card') && LINKS[s]) a.href = LINKS[s]; });
    var grid = doc.querySelector('.treat');
    (s === 'estetica' ? ['clareamento','lentes'] : [s]).forEach(function(k){ var c = grid.querySelector('[data-servico="'+k+'"]'); if(c) grid.insertBefore(c, grid.firstChild); });
    dl.push({event:'servico_campanha', servico:s});
  })();

  /* comparador antes/depois: arrasta em qualquer ponto da foto (mouse ou dedo); setas do teclado pelo <input> */
  all('.ba').forEach(function(box){
    var input = box.querySelector('input'), sent = false, down = null, drag = false;
    function set(v){ v = Math.max(0, Math.min(100, v)); box.style.setProperty('--pos', v + '%'); input.value = v; }
    function used(){ box._used = true; if(!sent){ sent = true; dl.push({event:'comparou_antes_depois', caso:input.id}); } }
    function at(e){ var r = box.getBoundingClientRect(); set((e.clientX - r.left) / r.width * 100); }
    function end(){ down = null; drag = false; box.classList.remove('dragging'); }
    /* só conta como uso um gesto real da pessoa: valor restaurado pelo navegador (ou pela prévia) não cancela a dica animada */
    input.addEventListener('input', function(e){ set(+input.value); if(e.isTrusted) used(); });
    if(!window.PointerEvent){ input.style.pointerEvents = 'auto'; return; }
    box.addEventListener('pointerdown', function(e){
      if(e.button) return;
      down = [e.clientX, e.clientY];
      if(e.pointerType === 'mouse'){ drag = true; box.classList.add('dragging'); at(e); used(); try{ box.setPointerCapture(e.pointerId); }catch(_){} }
    });
    box.addEventListener('pointermove', function(e){
      if(down === null) return;
      /* no toque, só começa depois de um movimento lateral: tocar para rolar a página não mexe na foto */
      var dx = Math.abs(e.clientX - down[0]), dy = Math.abs(e.clientY - down[1]);
      if(!drag && dx > 8 && dx > dy * 1.5){ drag = true; box.classList.add('dragging'); used(); try{ box.setPointerCapture(e.pointerId); }catch(_){} }
      if(drag) at(e);
    });
    ['pointerup','pointercancel','lostpointercapture'].forEach(function(ev){ box.addEventListener(ev, end); });
  });

  /* marca-texto, contador e dica do comparador: rodam uma vez quando o elemento aparece */
  once(all('.mark'), function(el){ el.classList.add('on'); }, .6);
  if(!reduce.matches){
    once(all('[data-count]'), function(el){
      /* sobe de 1 em 1, desacelerando no fim (~3s no total) */
      var end = +el.dataset.count, n = 0;
      el.textContent = '0';
      function tick(){ n++; el.textContent = n; if(n < end) setTimeout(tick, 120 + Math.pow(n / end, 3) * 380); }
      setTimeout(tick, 500);
    });
    once(all('.ba'), function(box){
      var t0 = null, keys = [[0,50],[.35,30],[.7,68],[1,50]];
      function at(k){ for(var i = 1; i < keys.length; i++){ if(k <= keys[i][0]){ var a = keys[i-1], b = keys[i], u = (k - a[0]) / (b[0] - a[0]); u = u < .5 ? 2*u*u : 1 - Math.pow(-2*u + 2, 2) / 2; return a[1] + (b[1] - a[1]) * u; } } return 50; }
      function step(t){ if(box._used) return; t0 = t0 || t; var k = Math.min(1, (t - t0) / 1600); box.style.setProperty('--pos', at(k) + '%'); if(k < 1) requestAnimationFrame(step); }
      setTimeout(function(){ requestAnimationFrame(step); }, 300);
    }, .6);
  }

  /* celular: dúvidas começam com 4 perguntas e um botão para ver as outras */
  (function(){
    var faq = doc.querySelector('.faq'); if(!faq) return;
    var n = all('details', faq).length; if(n <= 4) return;
    faq.classList.add('short');
    var b = doc.createElement('button'); b.type = 'button'; b.className = 'faq-more';
    b.textContent = 'Ver mais ' + (n - 4) + ' perguntas';
    b.addEventListener('click', function(){ faq.classList.remove('short'); b.remove(); dl.push({event:'abriu_mais_duvidas'}); });
    faq.appendChild(b);
  })();

  /* celular: a barra fixa aparece depois que o botão da abertura sai da tela
     e some enquanto outro botão igual estiver visível (nunca dois na mesma tela) */
  (function(){
    var hero = doc.querySelector('a[data-wa="hero"]');
    if(!hero || !hasIO){ root.classList.add('show-bar'); return; }
    var passed = false, visible = 0, seen = [];
    function sync(){ root.classList.toggle('show-bar', passed && visible === 0); }
    new IntersectionObserver(function(es){ var e = es[es.length - 1]; passed = !e.isIntersecting && e.boundingClientRect.top < 0; sync(); }).observe(hero);
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ var i = seen.indexOf(e.target); if(e.isIntersecting && i < 0) seen.push(e.target); if(!e.isIntersecting && i >= 0) seen.splice(i, 1); });
      visible = seen.length; sync();
    }, {threshold:.6});
    all('main .btn').forEach(function(b){ if(b !== hero) io.observe(b); });
  })();

  /* celular: galeria do laboratório, uma foto por vez, com bolinhas e rolagem automática
     (pausa quando a pessoa toca e quando a galeria sai da tela) */
  (function(){
    var g = doc.querySelector('#diferencial .gallery');
    if(!g) return;
    var shown = function(){ return all('img', g).filter(function(el){ return getComputedStyle(el).display !== 'none'; }); };
    var dots = doc.createElement('div'); dots.className = 'dots'; dots.setAttribute('aria-hidden', 'true');
    all('img:not(.desk-only)', g).forEach(function(){ dots.appendChild(doc.createElement('i')); });
    g.parentNode.insertBefore(dots, g.nextSibling);
    function current(){ var list = shown(), base = list[0].offsetLeft, cur = 0; list.forEach(function(el, i){ if(Math.abs(el.offsetLeft - base - g.scrollLeft) < Math.abs(list[cur].offsetLeft - base - g.scrollLeft)) cur = i; }); return cur; }
    var raf = 0;
    function paint(){ raf = 0; var c = current(); all('i', dots).forEach(function(d, k){ d.classList.toggle('on', k === c); }); }
    g.addEventListener('scroll', function(){ if(!raf) raf = requestAnimationFrame(paint); }, {passive:true}); paint();
    var inView = !hasIO, pausedUntil = 0;
    if(hasIO) new IntersectionObserver(function(es){ inView = es[0].isIntersecting; }, {threshold:.35}).observe(g);
    ['pointerdown','touchstart','wheel','keydown'].forEach(function(ev){ g.addEventListener(ev, function(){ pausedUntil = Date.now() + 6000; }, {passive:true}); });
    /* animação própria: no Safari do iPhone, scrollTo suave dentro de um carrossel com snap às vezes não anda */
    function glide(to){
      var from = g.scrollLeft, t0 = null, dur = 650;
      if(Math.abs(to - from) < 2) return;
      g.style.scrollSnapType = 'none';
      function step(t){
        t0 = t0 || t; var k = Math.min(1, (t - t0) / dur), e = k < .5 ? 4*k*k*k : 1 - Math.pow(-2*k + 2, 3) / 2;
        g.scrollLeft = from + (to - from) * e;
        if(k < 1 && Date.now() >= pausedUntil) requestAnimationFrame(step); else g.style.scrollSnapType = '';
      }
      requestAnimationFrame(step);
    }
    setInterval(function(){
      if(!phone.matches || reduce.matches || !inView || doc.hidden || Date.now() < pausedUntil) return;
      var list = shown(), c = current(), atEnd = c >= list.length - 1;
      glide(atEnd ? 0 : list[c + 1].offsetLeft - list[0].offsetLeft);
    }, 2800);
  })();
})();
