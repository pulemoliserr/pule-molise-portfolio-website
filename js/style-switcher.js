/* ========================== toggle style switcher =========================== */
const styleSwitcherToggle = document.querySelector('.style-switcher-toggler');

styleSwitcherToggle.addEventListener('click', () => {
  document.querySelector('.style-switcher').classList.toggle('open');
});

// hide style-switcher on scroll
window.addEventListener('scroll', () => {
  if (document.querySelector('.style-switcher').classList.contains('open')) {
    document.querySelector('.style-switcher').classList.remove('open');
  }
});

/* ========================== theme skin colors =========================== */
function setActiveStyle(colorHex) {
  document.documentElement.style.setProperty('--skin-color', colorHex);
  localStorage.setItem('selected-skin', colorHex);
}

// Restore saved skin on load
window.addEventListener('load', () => {
  const savedSkin = localStorage.getItem('selected-skin');
  if (savedSkin) {
    document.documentElement.style.setProperty('--skin-color', savedSkin);
  }
});

/* ========================== theme light and dark mode =========================== */
const dayNight = document.querySelector('.day-night');

dayNight.addEventListener('click', () => {
  dayNight.querySelector('i').classList.toggle('fa-sun');
  dayNight.querySelector('i').classList.toggle('fa-moon');
  document.body.classList.toggle('dark');
  const isDark = document.body.classList.contains('dark');
  localStorage.setItem('theme-mode', isDark ? 'dark' : 'light');
});

window.addEventListener('load', () => {
  const savedTheme = localStorage.getItem('theme-mode');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark');
    dayNight.querySelector('i').classList.add('fa-sun');
  } else {
    dayNight.querySelector('i').classList.add('fa-moon');
  }
});