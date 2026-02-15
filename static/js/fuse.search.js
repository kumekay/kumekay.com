document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const toolRows = document.querySelectorAll('.tool-row');
  let fuse;

  // Fetch the search index
  fetch('/utoolek/index.json')
    .then(res => res.json())
    .then(data => {
      fuse = new Fuse(data, {
        keys: ['title', 'description', 'tags'],
        threshold: 0.3,
        ignoreLocation: true
      });
    });

  searchInput.addEventListener('input', function() {
    const query = this.value.trim();

    if (!query || !fuse) {
      toolRows.forEach(row => row.style.display = '');
      return;
    }

    const results = fuse.search(query);
    const matchedTitles = new Set(results.map(r => r.item.title));

    toolRows.forEach(row => {
      const title = row.getAttribute('data-title');
      row.style.display = matchedTitles.has(title) ? '' : 'none';
    });
  });
});
