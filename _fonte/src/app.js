(function(){
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[data-wa],a[data-mapa]');
    if(!a) return;
    if(a.dataset.wa) window.dataLayer.push({event:'clique_whatsapp', wa_origem:a.dataset.wa});
    else window.dataLayer.push({event:'clique_mapa'});
  });
  var faq = document.querySelectorAll('.faq details');
  faq.forEach(function(d){ d.addEventListener('toggle', function(){
    if(d.open) window.dataLayer.push({event:'abriu_faq', pergunta:d.querySelector('summary').textContent});
  });});
})();
document.querySelectorAll('.ba input').forEach(function(r){
  var box = r.closest('.ba'), sent = false;
  r.addEventListener('input', function(){
    box.style.setProperty('--pos', r.value + '%');
    if(!sent){ sent = true; (window.dataLayer = window.dataLayer || []).push({event:'comparou_antes_depois', caso:r.id}); }
  });
});
/* Título e WhatsApp por campanha: ?s=implante | protese | lentes | clareamento | estetica */
(function(){
  var LINKS = /*WA_LINKS*/{};
  var HERO = {
    implante:   ['Implantes dentários em Itajaí', 'Volte a mastigar e sorrir <span class="serif mark">com firmeza.</span>', 'Implantes com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos. Planejamento cuidadoso e o olhar de quem fabrica dentes em cada detalhe.'],
    protese:    ['Próteses dentárias em Itajaí', 'Sua prótese confortável, natural <span class="serif mark">e feita sob medida.</span>', 'O Dr. Vinícius é cirurgião-dentista e técnico em prótese há 10 anos. Ele avalia o seu caso, confecciona a prótese no laboratório próprio e acompanha cada ajuste.'],
    lentes:     ['Lentes de contato dental em Itajaí', 'Um sorriso mais harmônico, <span class="serif mark">com naturalidade.</span>', 'Lentes de contato dental planejadas para o seu rosto pelo Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos.'],
    clareamento:['Clareamento dental em Itajaí', 'Dentes mais claros para <span class="serif mark">sorrir sem receio.</span>', 'Clareamento com acompanhamento profissional do Dr. Vinícius, do início ao fim, ajustado ao seu caso.'],
    estetica:   ['Lentes e clareamento em Itajaí', 'Estética do sorriso <span class="serif mark">com naturalidade.</span>', 'Lentes de contato dental e clareamento com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos. Cada detalhe pensado para o seu rosto.']
  };
  var s = (new URLSearchParams(location.search).get('s') || '').toLowerCase();
  if(!HERO[s]) return;
  var h = HERO[s];
  document.getElementById('h-pill').textContent = h[0];
  document.getElementById('h-title').innerHTML = h[1];
  document.getElementById('h-lead').textContent = h[2];
  document.querySelectorAll('a[data-wa]').forEach(function(a){ if(!a.closest('.t-card') && LINKS[s]) a.href = LINKS[s]; });
  var grid = document.querySelector('.treat');
  var first = s === 'estetica' ? ['lentes','clareamento'] : [s];
  first.slice().reverse().forEach(function(k){ var c = grid.querySelector('[data-servico="'+k+'"]'); if(c) grid.prepend(c); });
  window.dataLayer = window.dataLayer || []; window.dataLayer.push({event:'servico_campanha', servico:s});
})();

/* marca-texto, contador, dica no comparador: rodam uma vez quando o elemento aparece */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function once(els, fn, th){
    if(!('IntersectionObserver' in window)){ els.forEach(fn); return; }
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); fn(e.target); } }); }, {threshold: th || .5});
    els.forEach(function(el){ io.observe(el); });
  }
  once(Array.prototype.slice.call(document.querySelectorAll('.mark')), function(el){ el.classList.add('on'); }, .6);
  if(reduce) return;
  once(Array.prototype.slice.call(document.querySelectorAll('[data-count]')), function(el){
    var end = +el.dataset.count, t0 = null;
    function step(t){ t0 = t0 || t; var k = Math.min(1, (t - t0) / 900); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if(k < 1) requestAnimationFrame(step); }
    el.textContent = '0'; requestAnimationFrame(step);
  });
  once(Array.prototype.slice.call(document.querySelectorAll('.ba')), function(box){
    var input = box.querySelector('input'), touched = false, t0 = null;
    input.addEventListener('input', function(){ touched = true; }, {once:true});
    var keys = [[0,50],[.35,30],[.7,68],[1,50]];
    function at(k){ for(var i=1;i<keys.length;i++){ if(k<=keys[i][0]){ var a=keys[i-1], b=keys[i], u=(k-a[0])/(b[0]-a[0]); u=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2; return a[1]+(b[1]-a[1])*u; } } return 50; }
    function step(t){ if(touched) return; t0 = t0 || t; var k = Math.min(1, (t - t0) / 1600); box.style.setProperty('--pos', at(k) + '%'); if(k < 1) requestAnimationFrame(step); }
    setTimeout(function(){ requestAnimationFrame(step); }, 300);
  }, .6);
})();

/* celular: barra fixa só depois que o botão da abertura sai da tela */
(function(){
  var cta = document.querySelector('a[data-wa="hero"]'), root = document.documentElement;
  if(!cta || !('IntersectionObserver' in window)){ root.classList.add('show-bar'); return; }
  new IntersectionObserver(function(es){
    var e = es[0], passou = !e.isIntersecting && e.boundingClientRect.top < 0;
    root.classList.toggle('show-bar', passou);
  }).observe(cta);
})();
