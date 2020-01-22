// navigator.permissions.query({ name: "geolocation" }).then(function(result) {
//   if (result.state === "granted") {
//     console.log(result);
//   }
// });

const geo = navigator.geolocation;

if (navigator.geolocation) {
  geo.getCurrentPosition(logPosition);
}

function logPosition(position) {
  console.log(position.coords);
}
