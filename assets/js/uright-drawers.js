(function () {
  var scrim = document.getElementById('ur-scrim');
  var explorer = document.querySelector('.ur-explorer');
  var rail = document.querySelector('.ur-rail');
  var expBtn = document.getElementById('ur-explorer-toggle');
  var railBtn = document.getElementById('ur-rail-toggle');

  function close() {
    if (explorer) explorer.classList.remove('is-open');
    if (rail) rail.classList.remove('is-open');
    if (scrim) { scrim.classList.remove('is-open'); scrim.hidden = true; }
    if (expBtn) expBtn.setAttribute('aria-expanded', 'false');
    if (railBtn) railBtn.setAttribute('aria-expanded', 'false');
  }

  function open(panel, btn) {
    close();
    if (panel) panel.classList.add('is-open');
    if (scrim) { scrim.hidden = false; requestAnimationFrame(function () { scrim.classList.add('is-open'); }); }
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }

  if (expBtn) expBtn.addEventListener('click', function () {
    explorer && explorer.classList.contains('is-open') ? close() : open(explorer, expBtn);
  });
  if (railBtn) railBtn.addEventListener('click', function () {
    rail && rail.classList.contains('is-open') ? close() : open(rail, railBtn);
  });
  if (scrim) scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
