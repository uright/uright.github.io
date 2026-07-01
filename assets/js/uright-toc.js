/* ===== TOC scroll bridge =====
 * Chirpy initializes tocbot assuming the *window* is the scroll container, but
 * our IDE shell scrolls inside <main class="ur-main"> instead. That breaks two
 * things for the right-rail TOC (#toc):
 *
 *   1. Clicking a TOC link relies on the native anchor jump / tocbot's scrollTo,
 *      which targets window scroll — so the heading lands clipped at the top of
 *      <main> (or doesn't move correctly).
 *   2. The active-link highlight (scrollspy) reads window.scrollY, which never
 *      changes, so the wrong entry stays highlighted.
 *
 * This shim makes both follow .ur-main's scroll: smooth-scroll to the clicked
 * heading with a breathing-room offset, and recompute the active link from
 * .ur-main's scrollTop.
 * ===== */
(function () {
  var main = document.querySelector('.ur-main');
  var toc = document.getElementById('toc');
  if (!main || !toc) return;

  // The .ur-tabstrip is sticky at the top of <main>, overlaying the top --tab-h
  // pixels of scrolled content. Clear it plus breathing room so a heading
  // scrolled-to via a TOC click lands below the tab strip, not under it.
  // Mirrors `scroll-margin-top` on headings in _sass/uright/_views.scss.
  var tabH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--tab-h'), 10) || 36;
  var OFFSET = tabH + 16;

  function headings() {
    // tocbot renders <a class="toc-link" href="#heading-id"> entries.
    var links = toc.querySelectorAll('a.toc-link, a[href^="#"]');
    var out = [];
    links.forEach(function (link) {
      var id = decodeURIComponent((link.getAttribute('href') || '').slice(1));
      if (!id) return;
      var target = document.getElementById(id);
      if (target) out.push({ link: link, target: target });
    });
    return out;
  }

  function scrollToTarget(target) {
    // Position of the heading relative to <main>'s scroll origin.
    var top = target.getBoundingClientRect().top
            - main.getBoundingClientRect().top
            + main.scrollTop
            - OFFSET;
    main.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
  }

  // Intercept TOC clicks: stop the native window-based jump, scroll <main> instead.
  toc.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link || !toc.contains(link)) return;
    var id = decodeURIComponent((link.getAttribute('href') || '').slice(1));
    var target = id && document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    scrollToTarget(target);
    // Reflect the section in the URL without triggering another jump.
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  });

  // Scrollspy: highlight the entry for the heading nearest the top of <main>.
  var entries = [];
  function refresh() { entries = headings(); }
  refresh();

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      if (!entries.length) return;
      var mainTop = main.getBoundingClientRect().top;
      var current = entries[0];
      entries.forEach(function (entry) {
        var rel = entry.target.getBoundingClientRect().top - mainTop;
        if (rel - OFFSET <= 1) current = entry;
      });
      entries.forEach(function (entry) {
        entry.link.classList.toggle('is-active-link', entry === current);
      });
    });
  }

  main.addEventListener('scroll', onScroll, { passive: true });

  // tocbot builds #toc asynchronously; re-read entries once it has rendered.
  var observer = new MutationObserver(function () { refresh(); onScroll(); });
  observer.observe(toc, { childList: true, subtree: true });

  // Initial paint.
  onScroll();
})();
