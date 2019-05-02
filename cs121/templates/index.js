var el = x => document.getElementById(x);
var canvas = document.getElementById('canvas')

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}


function analyze() {
    //location.href='results.html';
    var uploadFiles = el('file-input').files;
    var cam = document.getElementById('photo')

    // var campic = cam.src;
    console.log(uploadFiles.length);
    if (uploadFiles.length != 1) {
      // this is not null by default
      if(cam.src != null){
        // look is there is an img?
        console.log("there is a webcam pic");

        // call analyze on webcam pic
        // toDataURL... look up to see if can access in here
        // var canvasData =


        alert(document.images[0].src);

        // console.log("Uploading...")
        // var image = document.getElementById('photo').src;
        // var form = document.getElementById('myForm');
        // var formData = new FormData(form);
        // formData.append("file", image);
        // var xmlhttp = new XMLHttpRequest();
        // xmlhttp.open("POST", "/signup");
        //
        // // check when state changes,
        // xmlhttp.onreadystatechange = function() {
        //
        // if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        //     alert(xmlhttp.responseText);
        //     }
        // }
        //
        // xmlhttp.send(formData);
        // console.log(formData.get('file'));
        // console.log(formData.get('userID'));

      }
      else {
        // var context = canvas.getContext('2d');
        console.log("there is no webcam pic or uploaded file");
        alert('Please select a file or take a photo to analyze!');

      }
     }
    else{
    // edit so that it only changes to 'analyzing...' if there is a photo
      el('analyze-button').innerHTML = 'Analyzing...';
      var xhr = new XMLHttpRequest();
      var loc = window.location
      console.log(`${loc.protocol}`);
      console.log(`${loc.hostname}`);
      console.log(`${loc.port}`);
      // issue here - open on invalid url file....
      //xhr.open('POST', `file//localhost/https/analyze`, true);
      xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
      xhr.onerror = function() {alert (xhr.responseText);}
      xhr.onload = function(e) {
          if (this.readyState === 4) {
              var response = JSON.parse(e.target.responseText);
              el('result-label').innerHTML = `Result = ${response['result']}`;
          }
          el('analyze-button').innerHTML = 'Analyze';
      }

      var fileData = new FormData();
      // need to edit here to take in one or the other (cam or file)
      // for file:
      fileData.append('file', uploadFiles[0]);
      // for webcam:
      //fileData.append(cam.src);

      xhr.send(fileData);
      console.log("file data sent!");
  }
}
