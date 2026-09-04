// Creative UI Animations and Effects
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // Floating animation for icons
    const icons = document.querySelectorAll('.floating-card i, .illustration-content i');
    icons.forEach((icon, index) => {
      icon.style.animationDelay = `${index * 0.2}s`;
    });

    // Interactive Panel Enhancements
    const interactivePanel = document.getElementById('interactivePanel');
    if (interactivePanel) {
      // Mouse move parallax effect (only when hovering)
      let isHovering = false;
      
      interactivePanel.addEventListener('mouseenter', () => {
        isHovering = true;
      });

      interactivePanel.addEventListener('mousemove', (e) => {
        if (!isHovering) return;
        
        const rect = interactivePanel.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 30;
        const rotateY = (centerX - x) / 30;
        
        interactivePanel.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-15px) scale(1.05)`;
      });

      interactivePanel.addEventListener('mouseleave', () => {
        isHovering = false;
        interactivePanel.style.transform = '';
      });

      // Click interaction
      interactivePanel.addEventListener('click', function() {
        this.style.animation = 'none';
        setTimeout(() => {
          this.style.animation = 'float 4s ease-in-out infinite';
        }, 10);
        
        // Ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'panel-ripple';
        this.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });

      // Icon click interactions
      const iconWrappers = interactivePanel.querySelectorAll('.icon-wrapper');
      iconWrappers.forEach(wrapper => {
        wrapper.addEventListener('click', function(e) {
          e.stopPropagation();
          const icon = this.querySelector('i');
          icon.style.animation = 'none';
          icon.style.transform = 'scale(1.5) rotate(360deg)';
          
          setTimeout(() => {
            icon.style.animation = 'iconFloat 3s ease-in-out infinite';
            icon.style.transform = '';
          }, 600);
        });
      });
    }
  });
})();
