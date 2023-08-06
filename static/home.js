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
  // Add the event listeners to each slider for both touch and mouse events
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

  cards.forEach((card) => {
    card.addEventListener('click', function () {
      const title = this.querySelector('img').getAttribute('data-title');
      const overview = this.querySelector('img').getAttribute('data-overview');
      showPopup(title, overview);
    });
  });
});

function showPopup(title, overview) {
  const popup = document.getElementById('popup');
  const popupMovieInfo = document.getElementById('popup-movie-info');
  overview = overview ? overview : `No plot for ${title}`
  popupMovieInfo.innerHTML = `
    <h1 class='text-danger mb-4'>${title}</h1>
    <p class='lead'>Overview</p>
    <p class='mt-4'>${overview}</p>
  `;
  popup.style.display = 'block';
}

function closePopup() {
  const popup = document.getElementById('popup');
  popup.style.display = 'none';
}

