/* EventBuzz - Theme toggle, nav, alerts */
(function () {
  const html = document.documentElement;
  const themeKey = 'eventbuzz-theme';

  function getStoredTheme() {
    return localStorage.getItem(themeKey) || 'light';
  }

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(themeKey, theme);
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    setTheme(getStoredTheme());
    themeToggle.addEventListener('click', function () {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
  }

  const navUserBtn = document.querySelector('.nav-user-btn');
  const navDropdown = document.querySelector('.nav-user-dropdown');
  if (navUserBtn && navDropdown) {
    navUserBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      navDropdown.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      navDropdown.classList.remove('open');
    });
  }

  document.querySelectorAll('.alert-close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      this.closest('.alert').remove();
    });
  });

  function scrollToSection(id) {
    var el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  document.querySelectorAll('a[href*="#events"], a[href*="#colleges"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var path = window.location.pathname.replace(/\/$/, '') || '/';
      var hash = this.getAttribute('href').split('#')[1];
      if (path === '' || path === '/') {
        e.preventDefault();
        if (hash) scrollToSection(hash);
      }
    });
  });

  if (window.location.hash) {
    var id = window.location.hash.slice(1);
    if (id && document.getElementById(id)) {
      setTimeout(function () { scrollToSection(id); }, 100);
    }
  }
})();
