const movieCards = document.querySelectorAll('img');
movieCards.forEach(card => {
  card.addEventListener('click', () => {
    const movieID = card.dataset.id;
    const url = '/info';
    fetch(url, {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: JSON.stringify({ 'id': movieID })
    })
  })
})