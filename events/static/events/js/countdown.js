/* Countdown timer for event detail page */
(function () {
  const el = document.getElementById('countdown');
  if (!el || !el.dataset.datetime) return;

  const targetStr = el.dataset.datetime;
  const parts = targetStr.split(/[\s-:]/);
  if (parts.length < 5) return;

  const year = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1;
  const day = parseInt(parts[2], 10);
  const hour = parseInt(parts[3], 10);
  const min = parseInt(parts[4], 10);
  const sec = parseInt(parts[5], 10) || 0;

  function pad(n) {
    return n < 10 ? '0' + n : String(n);
  }

  function update() {
    const target = new Date(year, month, day, hour, min, sec);
    const now = new Date();
    const diff = target - now;

    if (diff <= 0) {
      document.getElementById('cd-days').textContent = '0';
      document.getElementById('cd-hours').textContent = '0';
      document.getElementById('cd-mins').textContent = '0';
      document.getElementById('cd-secs').textContent = '0';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    const dEl = document.getElementById('cd-days');
    const hEl = document.getElementById('cd-hours');
    const mEl = document.getElementById('cd-mins');
    const sEl = document.getElementById('cd-secs');
    if (dEl) dEl.textContent = days;
    if (hEl) hEl.textContent = pad(hours);
    if (mEl) mEl.textContent = pad(mins);
    if (sEl) sEl.textContent = pad(secs);
    
    // Add pulse animation when seconds change
    if (sEl && secs % 2 === 0) {
      sEl.parentElement.style.animation = 'none';
      setTimeout(() => { sEl.parentElement.style.animation = 'pulse 0.5s'; }, 10);
    }
  }

  update();
  setInterval(update, 1000);
})();
