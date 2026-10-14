(function () {
  var root = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* language */
  var baseTitle = document.title;
  function setLang(l) {
    root.lang = l; root.dir = l === 'ar' ? 'rtl' : 'ltr'; root.dataset.lang = l;
    store('lang', l); moveBar(); tick();
  }
  $$('[data-lang-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(root.dataset.lang === 'ar' ? 'en' : 'ar'); });
  });

  /* theme */
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = root.dataset.theme === 'ink' ? 'paper' : 'ink';
      root.dataset.theme = t; store('theme', t);
    });
  });

  /* Cairo clock */
  var clocks = $$('[data-clock]');
  function tick() {
    var fmt;
    try {
      fmt = new Intl.DateTimeFormat(root.dataset.lang === 'ar' ? 'ar-EG' : 'en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Africa/Cairo' });
    } catch (e) { return; }
    var s = fmt.format(new Date());
    clocks.forEach(function (c) { c.textContent = s; });
  }
  if (clocks.length) { tick(); setInterval(tick, 30000); }

  $$('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });

  /* reveal on scroll */
  var items = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  /* nav indicator follows the section in view */
  var nav = $('.nav'), links = $$('.nav a');
  var active = null;
  function moveBar() {
    if (!nav) return;
    var a = active || null;
    if (!a) { nav.style.setProperty('--bar-o', 0); return; }
    var n = nav.getBoundingClientRect(), r = a.getBoundingClientRect();
    nav.style.setProperty('--bar-x', (r.left - n.left) + 'px');
    nav.style.setProperty('--bar-w', r.width + 'px');
    nav.style.setProperty('--bar-o', 1);
  }
  var sections = links.map(function (a) {
    var id = (a.getAttribute('href') || '').split('#')[1];
    return id && document.getElementById(id);
  });
  if (sections.some(Boolean) && 'IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = sections.indexOf(e.target);
        if (e.isIntersecting && i > -1) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          active = links[i]; active.classList.add('is-active'); moveBar();
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { if (s) so.observe(s); });
  }
  links.forEach(function (a) {
    a.addEventListener('mouseenter', function () { var keep = active; active = a; moveBar(); active = keep; });
  });
  if (nav) nav.addEventListener('mouseleave', moveBar);
  window.addEventListener('resize', moveBar);

  /* work filters */
  var chips = $$('[data-filter]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.dataset.filter;
      chips.forEach(function (x) { var on = x === c; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
      $$('.card[data-kinds]').forEach(function (card) {
        var show = f === 'all' || card.dataset.kinds.split(' ').indexOf(f) > -1;
        card.classList.toggle('is-hidden', !show);
        if (show) card.classList.add('in');
      });
      $$('.archive tr[data-kinds]').forEach(function (tr) {
        tr.hidden = !(f === 'all' || tr.dataset.kinds === f);
      });
    });
  });

  /* copy email */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var out = $('.copied', b), done = function () {
        out.textContent = root.dataset.lang === 'ar' ? 'تم النسخ ✓' : 'Copied ✓';
        setTimeout(function () { out.textContent = ''; }, 1800);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, function () { location.href = 'mailto:' + b.dataset.copy; });
      else location.href = 'mailto:' + b.dataset.copy;
    });
  });

  /* lightbox */
  var lb = $('[data-lightbox]'), zooms = $$('[data-zoom]'), idx = 0, lastFocus = null;
  if (lb && zooms.length) {
    var lbImg = $('img', lb), lbCap = $('figcaption', lb);
    function show(i) {
      idx = (i + zooms.length) % zooms.length;
      var src = $('img', zooms[idx]), fig = zooms[idx].closest('figure'), cap = fig && $('figcaption', fig);
      lbImg.src = src.currentSrc || src.src; lbImg.alt = src.alt;
      lbCap.innerHTML = cap ? cap.innerHTML : '';
    }
    function open(i) { lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; $('.lightbox__close', lb).focus(); }
    function close() { lb.hidden = true; document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
    zooms.forEach(function (z, i) { z.addEventListener('click', function () { open(i); }); });
    $('.lightbox__close', lb).addEventListener('click', close);
    $('.lightbox__prev', lb).addEventListener('click', function () { show(idx - 1); });
    $('.lightbox__next', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      var rtl = root.dir === 'rtl';
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(idx + (rtl ? -1 : 1));
      if (e.key === 'ArrowLeft') show(idx + (rtl ? 1 : -1));
    });
  }
})();
