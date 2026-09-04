// Events Slider Functionality
(function() {
  'use strict';

  let currentSlide = 0;
  let slideInterval;
  const slideDuration = 4000; // 4 seconds

  function initSlider() {
    const slider = document.getElementById('eventsSlider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.slider-slide');
    const dots = document.querySelectorAll('.slider-dot');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');

    if (slides.length === 0) return;

    function showSlide(index) {
      // Remove active class from all slides and dots
      slides.forEach((slide, i) => {
        slide.classList.remove('active', 'prev');
        if (i < index) {
          slide.classList.add('prev');
        }
      });
      dots.forEach(dot => dot.classList.remove('active'));

      // Add active class to current slide and dot
      if (slides[index]) {
        slides[index].classList.add('active');
      }
      if (dots[index]) {
        dots[index].classList.add('active');
      }

      currentSlide = index;
    }

    function nextSlide() {
      const next = (currentSlide + 1) % slides.length;
      showSlide(next);
    }

    function prevSlide() {
      const prev = (currentSlide - 1 + slides.length) % slides.length;
      showSlide(prev);
    }

    function goToSlide(index) {
      if (index >= 0 && index < slides.length) {
        showSlide(index);
        resetInterval();
      }
    }

    function resetInterval() {
      clearInterval(slideInterval);
      slideInterval = setInterval(nextSlide, slideDuration);
    }

    // Event listeners
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        resetInterval();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        resetInterval();
      });
    }

    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        goToSlide(index);
      });
    });

    // Pause on hover
    const container = slider.closest('.slider-container');
    if (container) {
      container.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
      });

      container.addEventListener('mouseleave', () => {
        resetInterval();
      });
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        prevSlide();
        resetInterval();
      } else if (e.key === 'ArrowRight') {
        nextSlide();
        resetInterval();
      }
    });

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    container.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    });

    container.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    });

    function handleSwipe() {
      const swipeThreshold = 50;
      const diff = touchStartX - touchEndX;

      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          nextSlide();
        } else {
          prevSlide();
        }
        resetInterval();
      }
    }

    // Start auto-slide
    resetInterval();
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSlider);
  } else {
    initSlider();
  }
})();
