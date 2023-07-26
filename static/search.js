const searchBar = document.querySelector('.search');
const heading = document.querySelector('.heading');

function sendData() {
  const value = document.querySelector('.search-input').value.trim();
  const loader = document.querySelector('.loader');

  if (value === '') return;

  loader.style.display = 'block';
  $.ajax({
      url: '/search_item',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ 'value': value }),
      success: function(response) {
          loader.style.display = 'none';
          if (!response.Title) {
            heading.innerHTML = `No results for ${value}`;
            return;
          }
          displayContent(response);
      },
      error: function(error) {
        loader.style.display = 'none';
      }
  });
}

function displayContent(data) {
  const result = document.querySelector('.result');
  const cardImage = document.querySelector('.card-img-top');
  const moviePlot = document.querySelector('.plot');
  const movieRating = document.querySelector('.rating');
  const releaseDate = document.querySelector('.released');

  result.style.display = 'block';
  heading.innerHTML = `Search result for ${data.Title}`;
  cardImage.src = data.Poster;
  moviePlot.innerHTML = data.Plot;
  movieRating.innerHTML = data.Ratings[0].Value;
  releaseDate.innerHTML = data.Released;
}

searchBar.addEventListener('submit', async (event) => {
  event.preventDefault();
  sendData();
})