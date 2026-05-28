/* Divine Theme v4 — small interactions */
(function () {
  'use strict';

  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.d-reveal').forEach(function (el) {
      el.classList.add('in');
    });
    return;
  }

  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var kids = e.target.querySelectorAll(':scope > *');
      if (kids.length > 1) {
        kids.forEach(function (k, i) {
          k.style.transitionDelay = (i * 75) + 'ms';
        });
      }
      e.target.classList.add('in');
      obs.unobserve(e.target);
    });
  }, { threshold: 0.07 });

  function init() {
    document.querySelectorAll('.d-reveal').forEach(function (el) {
      obs.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* Re-run when Shopify theme editor injects new sections */
  document.addEventListener('shopify:section:load', init);
})();
