/* 5-star rating interaction on review page */
(function () {
  const starRating = document.getElementById('starRating');
  const ratingInput = document.getElementById('ratingInput');
  if (!starRating || !ratingInput) return;

  const stars = starRating.querySelectorAll('.star');

  function setRating(value) {
    const v = parseInt(value, 10);
    ratingInput.value = v;
    stars.forEach(function (star, i) {
      if (i < v) star.classList.add('filled');
      else star.classList.remove('filled');
    });
  }

  stars.forEach(function (star) {
    star.addEventListener('click', function () {
      setRating(star.dataset.value);
    });
    star.addEventListener('mouseenter', function () {
      const v = parseInt(star.dataset.value, 10);
      stars.forEach(function (s, i) {
        if (i < v) s.classList.add('filled');
        else s.classList.remove('filled');
      });
    });
  });

  starRating.addEventListener('mouseleave', function () {
    const current = parseInt(ratingInput.value, 10) || 0;
    setRating(current);
  });

  const initial = ratingInput.value;
  if (initial) setRating(initial);
})();
