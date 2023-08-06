const movieCards = document.querySelectorAll('img');
movieCards.forEach(card => {
  card.addEventListener('click', () => {
    const movieID = card.dataset.id;
    const url = '/get_info';
    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'id': movieID })
    })
  })
})