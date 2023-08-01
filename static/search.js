const searchBar = document.querySelector('.search');
const heading = document.querySelector('.heading');
const result = document.querySelector('.result');

function sendData() {
  result.style.display = 'none';
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
          displayContent(response);
      },
      error: function(error) {
        loader.style.display = 'none';
      }
  });
}

function displayContent(data) {
  const cardImage = document.querySelector('.card-img-top');
  const cardTitle = document.querySelector('.card-title')
  const moviePlot = document.querySelector('.plot');
  const movieRating = document.querySelector('.rating');
  const language = document.querySelector('.language')
  const releaseDate = document.querySelector('.released');

  result.style.display = 'block';
  heading.innerHTML = `Search result for ${data[0].original_title}`;
  cardTitle.innerHTML = 'Overview'
  cardImage.src = `http://image.tmdb.org/t/p/w500/${data[0].poster_path}`;
  moviePlot.innerHTML = data[0].overview;
  movieRating.innerHTML = `Rating: ${data[0].vote_average}`;
  language.innerHTML = `Language: ${data[0].original_language}`;
  releaseDate.innerHTML = `Release Date: ${data[0].release_date}`;
  console.log(cardImage.src)
}

searchBar.addEventListener('submit', async (event) => {
  event.preventDefault();
  sendData();
})