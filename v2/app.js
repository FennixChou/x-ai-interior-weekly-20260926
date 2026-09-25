(() => {
  const cards = [...document.querySelectorAll('.case')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const query = document.getElementById('query');
  let category = 'all';
  function update() {
    const term = query.value.trim().toLocaleLowerCase();
    let shown = 0;
    for (const card of cards) {
      const match = (category === 'all' || card.dataset.cats.split('|').includes(category)) && card.dataset.search.toLocaleLowerCase().includes(term);
      card.hidden = !match;
      if (match) shown++;
    }
    document.getElementById('count').textContent = `顯示 ${shown} / ${cards.length} 則`;
    document.getElementById('empty').hidden = shown !== 0;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === category)));
  }
  buttons.forEach(button => button.addEventListener('click', () => {category = button.dataset.filter; update();}));
  query.addEventListener('input', update);
  function revealAnchor() {
    if (/^#X\d\d$/.test(location.hash)) {
      category = 'all'; query.value = ''; update();
      document.getElementById(location.hash.slice(1))?.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', revealAnchor);
  revealAnchor();
})();
