/* Shared behaviour for pages outside the home page (/data-science, /cybersecurity, project pages). */

// Mobile menu toggle
(function () {
  const toggler = document.querySelector('.nav-toggler');
  const aside = document.querySelector('.aside');
  const main = document.querySelector('.page-main');
  if (!toggler || !aside) return;
  toggler.addEventListener('click', function () {
    aside.classList.toggle('open');
    toggler.classList.toggle('open');
    if (main) main.classList.toggle('open');
  });
})();

// GitHub / live-demo buttons: take URLs from links.js, hide the button while the URL is empty
(function () {
  const links = window.PROJECT_LINKS || {};
  document.querySelectorAll('[data-link-type]').forEach(function (el) {
    const group = links[el.getAttribute('data-link-type')] || {};
    const url = group[el.getAttribute('data-link-key')];
    if (url) {
      el.setAttribute('href', url);
    } else {
      el.remove();
    }
  });
})();
