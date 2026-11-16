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
    implante:   ['Implantes dentários em Itajaí', 'Volte a mastigar e sorrir <span class="serif">com firmeza.</span>', 'Implantes com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos. Planejamento cuidadoso e o olhar de quem fabrica dentes em cada detalhe.'],
    protese:    ['Próteses dentárias em Itajaí', 'Sua prótese confortável, natural <span class="serif">e feita sob medida.</span>', 'O Dr. Vinícius é cirurgião-dentista e técnico em prótese há 10 anos. Ele avalia o seu caso, confecciona a prótese no laboratório próprio e acompanha cada ajuste.'],
    lentes:     ['Lentes de contato dental em Itajaí', 'Um sorriso mais harmônico, <span class="serif">com naturalidade.</span>', 'Lentes de contato dental planejadas para o seu rosto pelo Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos.'],
    clareamento:['Clareamento dental em Itajaí', 'Dentes mais claros para <span class="serif">sorrir sem receio.</span>', 'Clareamento com acompanhamento profissional do Dr. Vinícius, do início ao fim, ajustado ao seu caso.'],
    estetica:   ['Lentes e clareamento em Itajaí', 'Estética do sorriso <span class="serif">com naturalidade.</span>', 'Lentes de contato dental e clareamento com o Dr. Vinícius, cirurgião-dentista e técnico em prótese há 10 anos. Cada detalhe pensado para o seu rosto.']
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
