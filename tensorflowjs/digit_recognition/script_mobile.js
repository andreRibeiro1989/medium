// define relevant variables
var row = document.getElementById("row");
var col = document.getElementById("col");
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext('2d');
var dragging = false;
var pos = { x: 0, y: 0 };


// define event listeners for both desktop and mobile

// nontouch
canvas.addEventListener('mousedown',  engage);
canvas.addEventListener('mousedown',  setPosition);
canvas.addEventListener('mousemove',  draw);
canvas.addEventListener('mouseup', disengage);

// touch
canvas.addEventListener('touchstart', engage);
canvas.addEventListener('touchmove', setPosition);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', disengage);

// set canvas size
ctx.canvas.width = col.offsetWidth - 50;
ctx.canvas.height = col.offsetWidth - 50;

// detect if it is a touch device
function isTouchDevice() {
  return (
    ('ontouchstart' in window) ||
    (navigator.maxTouchPoints > 0) ||
    (navigator.msMaxTouchPoints > 0)
  );
}


// define basic functions to detect click / release

function engage() {
  dragging = true;
};

function disengage() {
  dragging = false;
};


// get the new position given a mouse / touch event
function setPosition(e) {

  if (isTouchDevice()) {
  	var touch = e.touches[0];
  	pos.x = touch.clientX - row.offsetLeft;
  	pos.y = touch.clientY - row.offsetTop;
  } else {
  
	  pos.x = e.clientX - row.offsetLeft;
  	pos.y = e.clientY - row.offsetTop;
  }
}


// draws a line in a canvas if mouse is pressed
function draw(e) {
  
  e.preventDefault();
  e.stopPropagation();

  // to draw the user needs to be engaged (dragging = True)
  if (dragging) {

    // begin drawing
    ctx.beginPath();
  
    // attributes of the line
    ctx.lineWidth = 40;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'red';

    // get current position, move to new position, create line from current to new
    ctx.moveTo(pos.x, pos.y);
    setPosition(e);
    ctx.lineTo(pos.x, pos.y);

    // draw
    ctx.stroke();
  }
}


// clear canvas
function erase() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}


// defines a TF model load function
async function loadModel(){	
  	
  // loads the model
  model = await tf.loadLayersModel('tensorflow/model.json');    
  
  // warm start the model. speeds up the first inference
  model.predict(tf.zeros([1, 28, 28, 1]))
  
  // return model
  return model
}


// gets an image tensor from a canvas
function getData(){
  return ctx.getImageData(0, 0, canvas.width, canvas.height);
}


// defines the model inference functino
async function predictModel(){
    
  // gets image data
  imageData = getData();
  
  // converts from a canvas data object to a tensor
  image = tf.browser.fromPixels(imageData)
  
  // pre-process image
  image = tf.image.resizeBilinear(image, [28,28]).sum(2).expandDims(0).expandDims(-1)
  
  // gets model prediction
  y = model.predict(image);
  
  // replaces the text in the result tag by the model prediction
  document.getElementById('result').innerHTML = "Prediction: " + y.argMax(1).dataSync();
}

// loads the model
var model = loadModel()
