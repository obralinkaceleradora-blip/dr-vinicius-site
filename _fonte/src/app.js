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
