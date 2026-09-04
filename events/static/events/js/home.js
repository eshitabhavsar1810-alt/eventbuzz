/* Home: search, category, college, date filter */
(function () {
  const searchInput = document.getElementById('searchEvents');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const filterCollege = document.getElementById('filterCollege');
  const filterDate = document.getElementById('filterDate');
  const btnFilter = document.getElementById('btnFilter');
  const eventsGrid = document.getElementById('eventsGrid');
  const eventCards = eventsGrid ? eventsGrid.querySelectorAll('.event-card') : [];

  function filterEvents() {
    const query = (searchInput && searchInput.value.trim().toLowerCase()) || '';
    const activeCategory = document.querySelector('.filter-btn.active');
    const category = (activeCategory && activeCategory.dataset.category) || 'all';
    const collegeId = (filterCollege && filterCollege.value) || '';
    const dateStr = (filterDate && filterDate.value) || '';

    eventCards.forEach(function (card) {
      const title = (card.dataset.title || '').toLowerCase();
      const cat = card.dataset.category || '';
      const matchSearch = !query || title.indexOf(query) !== -1;
      const matchCategory = category === 'all' || cat === category;
      const matchCollege = !collegeId || (card.dataset.collegeId === collegeId);
      const matchDate = !dateStr || (card.dataset.date === dateStr);
      card.style.display = matchSearch && matchCategory && matchCollege && matchDate ? '' : 'none';
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterEvents);
    searchInput.addEventListener('keyup', filterEvents);
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterBtns.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
      filterEvents();
    });
  });

  if (btnFilter) btnFilter.addEventListener('click', filterEvents);
  if (filterCollege) filterCollege.addEventListener('change', filterEvents);
  if (filterDate) filterDate.addEventListener('change', filterEvents);

  const params = new URLSearchParams(window.location.search);
  const collegeParam = params.get('college');
  if (collegeParam && filterCollege) {
    filterCollege.value = collegeParam;
    filterEvents();
  }
})();
