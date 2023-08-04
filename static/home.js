const sliders = document.querySelectorAll('.col-12');

let mouseDown = false;
let startX, scrollLeft;

let startDragging = function (e) {
  mouseDown = true;
  startX = e.pageX - e.currentTarget.offsetLeft;
  scrollLeft = e.currentTarget.scrollLeft;
};

let stopDragging = function (event) {
  mouseDown = false;
};

const handleSliderMove = (e) => {
  e.preventDefault();
  if (!mouseDown) { return; }
  const x = e.pageX - e.currentTarget.offsetLeft;
  const scroll = x - startX;
  e.currentTarget.scrollLeft = scrollLeft - scroll;
};

sliders.forEach((slider) => {
  // Add the event listeners to each slider
  slider.addEventListener('mousedown', startDragging, false);
  slider.addEventListener('mouseup', stopDragging, false);
  slider.addEventListener('mouseleave', stopDragging, false);
  slider.addEventListener('mousemove', handleSliderMove);
});
