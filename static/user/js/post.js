    const user_response = {};

const geo = navigator.geolocation;

if (navigator.geolocation) {
  geo.getCurrentPosition(logPosition);
}

function logPosition(position) {
  user_response.lat = position.coords.latitude;
  user_response.lon = position.coords.longitude;
  console.log(position.coords);
  console.log(">>>>", user_response);
}

// camera stream video element
let videoElm = document.querySelector("#camera-stream");
// flip button element
let flipBtn = document.querySelector("#flip-btn");

// default user media options
let defaultsOpts = { audio: false, video: true };
let shouldFaceUser = true;

// check whether we can use facingMode
let supports = navigator.mediaDevices.getSupportedConstraints();
if (supports["facingMode"] === true) {
  flipBtn.disabled = false;
}

let stream = null;

function capture() {
  defaultsOpts.video = { facingMode: shouldFaceUser ? "environment" : "user" };
  navigator.mediaDevices
    .getUserMedia(defaultsOpts)
    .then(function(_stream) {
      stream = _stream;
      videoElm.srcObject = stream;
      videoElm.play();
    })
    .catch(function(err) {
      console.log(err);
    });
}

flipBtn.addEventListener("click", function() {
  if (stream == null) return;
  // we need to flip, stop everything
  stream.getTracks().forEach(t => {
    t.stop();
  });
  // toggle / flip
  shouldFaceUser = !shouldFaceUser;
  capture();
});

capture();
const captureCanvas = document.querySelector("#captureCanvas");
const addPhoto = document.querySelector("#addPhoto");
addPhoto.addEventListener("click", function() {
  var ctx = captureCanvas.getContext("2d");
  var img = new Image();

  ctx.drawImage(videoElm, 0, 0, captureCanvas.width, captureCanvas.height);
  img.src = captureCanvas.toDataURL("image/png");
  img.width = 240;
//  console.log('XXXXXXXXXX',img.src);
  user_response.img = img.src;
  captureCanvas.appendChild(img);
});

const postToServer = document.querySelector("#postToServer");

postToServer.addEventListener("click", function() {
  console.log(user_response);
  fetch('/user_response/',
  {
    method: 'POST',
    headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(user_response)});
});
