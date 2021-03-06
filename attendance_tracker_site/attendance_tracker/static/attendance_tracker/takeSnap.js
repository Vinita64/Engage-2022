(function () {
  let width = 320;
  let height = 0;

  let streaming = false;

  let video = null;
  let canvas = null;
  let photo = null;
  let startbutton = null;

  let uploadForm = null;
  let imageData = null;
  //Initializing

  function startup() {
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    photo = document.getElementById("photo");
    startbutton = document.getElementById("startbutton");
    uploadForm = document.getElementById("checkImage");
    imageData = document.getElementById("studentPic");

    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then(function (stream) {
        video.srcObject = stream;
        video.play();
      })
      .catch(function (err) {
        console.log("An error occurred: " + err);
      });

    video.addEventListener(
      "canplay",
      function (ev) {
        if (!streaming) {
          height = video.videoHeight / (video.videoWidth / width);

          if (isNaN(height)) {
            height = width / (4 / 3);
          }

          video.setAttribute("width", width);
          video.setAttribute("height", height);
          canvas.setAttribute("width", width);
          canvas.setAttribute("height", height);
          streaming = true;
        }
      },
      false
    );

    startbutton.addEventListener(
      "click",
      function (ev) {
        takepicture();
        ev.preventDefault();
      },
      false
    );

    uploadForm.addEventListener("submit", checkImage);

    clearphoto();
  }

  //Remove photo
  function clearphoto() {
    let context = canvas.getContext("2d");
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    photo.setAttribute("src", "");
  }
  
  //Take snapshot
  function takepicture() {
    let context = canvas.getContext("2d");
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      let data = canvas.toDataURL("image/png");
      photo.setAttribute("src", data);
    } else {
      clearphoto();
    }
  }
  function checkImage(event) {
    event.preventDefault();
    const photoBase64 = photo.getAttribute("src");
    if (Boolean(photoBase64)) {
      imageData.value = photo.getAttribute("src");
      uploadForm.submit();
      clearphoto();
    } else {
      console.error("no photo taken");
    }
  }

  window.addEventListener("load", startup, false);
})();
