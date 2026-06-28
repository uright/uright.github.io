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

/* ===== Search trigger wiring =====
 * Chirpy's minified JS binds click on #search-trigger to open its search UI.
 * Our titlebar uses #ur-search-trigger (the visible styled button + Cmd/Ctrl+K).
 * Bridge: clicking #ur-search-trigger or pressing Cmd/Ctrl+K programmatically
 * clicks the Chirpy-internal #search-trigger, which activates Chirpy's search
 * overlay (#search shows, #search-input gets focus, results panel activates).
 * ===== */
(function () {
  var urBtn = document.getElementById('ur-search-trigger');
  var chirpyTrigger = document.getElementById('search-trigger');
  var searchInput = document.getElementById('search-input');

  function activateSearch() {
    // Let Chirpy's own JS handle the state (it bound to #search-trigger click).
    if (chirpyTrigger) {
      chirpyTrigger.click();
    }
    // As a fallback (in case Chirpy JS is not yet ready or took a different path),
    // also directly focus the search input so the user can type immediately.
    if (searchInput) {
      searchInput.focus();
    }
  }

  if (urBtn) {
    urBtn.addEventListener('click', activateSearch);
  }

  document.addEventListener('keydown', function (e) {
    // Cmd+K (mac) or Ctrl+K (win/linux) — open search
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      activateSearch();
    }
  });
})();
