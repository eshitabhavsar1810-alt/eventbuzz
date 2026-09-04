/* Auth form validation */
(function () {
  const form = document.getElementById('authForm');
  if (!form) return;

  const modeSelect = document.querySelector('.auth-select[data-admin-url][data-student-url]');
  if (modeSelect) {
    modeSelect.addEventListener('change', function () {
      const adminUrl = this.getAttribute('data-admin-url');
      const studentUrl = this.getAttribute('data-student-url');
      if (this.value === 'admin' && adminUrl) window.location.href = adminUrl;
      if (this.value === 'student' && studentUrl) window.location.href = studentUrl;
    });
  }

  function showError(input, message) {
    const group = input.closest('.form-group');
    const errEl = group && group.querySelector('.form-error');
    if (errEl) {
      errEl.textContent = message;
      input.setCustomValidity(message || '');
    }
  }

  function clearError(input) {
    const group = input.closest('.form-group');
    const errEl = group && group.querySelector('.form-error');
    if (errEl) errEl.textContent = '';
    input.setCustomValidity('');
  }

  form.querySelectorAll('input').forEach(function (input) {
    input.addEventListener('blur', function () {
      clearError(this);
      if (this.validity.valid) return;
      if (this.validity.valueMissing) showError(this, 'This field is required.');
      else if (this.validity.tooShort) showError(this, 'Too short.');
      else if (this.validity.typeMismatch) showError(this, 'Invalid format.');
    });

    input.addEventListener('input', function () {
      clearError(this);
    });
  });

  form.addEventListener('submit', function (e) {
    let valid = true;
    form.querySelectorAll('input[required]').forEach(function (input) {
      if (!input.value.trim()) {
        showError(input, 'This field is required.');
        valid = false;
      }
    });

    const password1 = form.querySelector('input[name="password1"]');
    const password2 = form.querySelector('input[name="password2"]');
    if (password1 && password2 && password1.value !== password2.value) {
      showError(password2, 'Passwords do not match.');
      valid = false;
    }

    if (!valid) e.preventDefault();
  });
})();
