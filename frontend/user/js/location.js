const geo = navigator.geolocation;

if (navigator.geolocation) {
  geo.getCurrentPosition(logPosition);
}

function logPosition(position) {
  console.log(position.coords);
}
