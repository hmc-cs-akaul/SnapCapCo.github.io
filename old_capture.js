(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
    uploadbutton = document.getElementById('upload_photo_btn');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    // if webcam is blocked, display logo instead by removing camera div
    .catch(function(err) {
      div = document.getElementById('cam-container');
      div2 = document.getElementById('canvas');
      dLbtn = document.getElementById('dl-btn');
      div2.remove();
      dLbtn.remove();
      while(div.firstChild){
        div.removeChild(div.firstChild);
        // div2.removeChild(div2.firstChild);
      }

      // user does not allow permission for webcam, display logo instead
      logoImg = "<img src='../images/templogo.jpeg' alt='logo'>";
      div.innerHTML = logoImg;
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);

        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.

        if (isNaN(height)) {
          height = width / (4/3);
        }

        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);

    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }

  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.


  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
      // after taking photo, stop video elt, TODO: replace w/ something else? logo?
      // video.srcObject.getVideoTracks().forEach(track => track.stop());
      //right now it is just black ^^
      // after taking photo, don't allow user to 'upload' a photo, so disable upload button
      uploadbutton.disabled = true;

      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    //  document.write(data);

    //  file_put_contents("myimage.png", base64_decode(explode(",", $_GET['data'])[1]));
     document.querySelector('#dl-btn').href = data;
    } else {
      clearphoto();
    }
  }


  // Set up our event listener to run the startup process
  // once loading is complete.
   window.addEventListener('load', startup, false);
})();
