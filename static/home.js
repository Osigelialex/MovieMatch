const sliders = document.querySelectorAll('.col-12');

let mouseDown = false;
let startX, scrollLeft;

let startDragging = function (e) {
  mouseDown = true;
  startX = e.type === 'touchstart' ? e.touches[0].pageX - e.currentTarget.offsetLeft : e.pageX - e.currentTarget.offsetLeft;
  scrollLeft = e.currentTarget.scrollLeft;
};

let stopDragging = function (event) {
  mouseDown = false;
};

const handleSliderMove = (e) => {
  e.preventDefault();
  if (!mouseDown) { return; }
  const x = e.type === 'touchmove' ? e.touches[0].pageX - e.currentTarget.offsetLeft : e.pageX - e.currentTarget.offsetLeft;
  const scroll = x - startX;
  e.currentTarget.scrollLeft = scrollLeft - scroll;
};

sliders.forEach((slider) => {
  slider.addEventListener('mousedown', startDragging, false);
  slider.addEventListener('mouseup', stopDragging, false);
  slider.addEventListener('mouseleave', stopDragging, false);
  slider.addEventListener('mousemove', handleSliderMove);

  slider.addEventListener('touchstart', startDragging, false);
  slider.addEventListener('touchend', stopDragging, false);
  slider.addEventListener('touchcancel', stopDragging, false);
  slider.addEventListener('touchmove', handleSliderMove);
});

document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.card');

  let isDragging = false; // Flag to track dragging

  cards.forEach((card) => {
    card.addEventListener('mousedown', () => {
      isDragging = false;
    });

    card.addEventListener('mousemove', () => {
      isDragging = true;
    });

    card.addEventListener('mouseup', (e) => {
      if (!isDragging) {
        const title = card.querySelector('img').getAttribute('data-title');
        const overview = card.querySelector('img').getAttribute('data-overview');
        const maxLength = 250;
        const truncatedOverview = overview.length > maxLength ? overview.substring(0, maxLength) + '...' : overview;
        const rating = card.querySelector('img').getAttribute('data-vote_average');
        const poster = card.querySelector('img').getAttribute('data-poster');
        showPopup(title, truncatedOverview, rating, poster);
      }
      isDragging = false;
    });
  });
});

function showPopup(title, overview, rating, poster) {
  const popup = document.getElementById('popup');
  const popupMovieInfo = document.getElementById('popup-movie-info');
  const poster_path = `http://image.tmdb.org/t/p/w500/${poster}`;
  overview = overview ? overview : `No plot for ${title}`;
  popupMovieInfo.innerHTML = `
    <img src='${poster_path}' class='img-thumbnail mb-4'>
    <h5 class='mb-2'>${title}</h5>
    <p class='fw-bold'>Overview</p>
    <p class='mt-2'>${overview}</p>
    <p class='mt-2 lead'>Rating: ${rating}</p>
  `;
  popup.style.display = 'block';
}

function closePopup() {
  const popup = document.getElementById('popup');
  popup.style.display = 'none';
}

