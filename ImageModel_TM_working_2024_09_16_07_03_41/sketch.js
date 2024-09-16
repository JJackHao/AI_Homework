// Copyright (c) 2019 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/* ===
ml5 Example
Webcam Image Classification using a pre-trained customized model and p5.js
This example uses p5 preload function to create the classifier
=== */

// Classifier Variable
let classifier;
// Model URL
//let imageModelURL = 'https://teachablemachine.withgoogle.com/models/BaNkYVx3m/';
let imageModelURL = 'https://teachablemachine.withgoogle.com/models/bVIx6PNIy/';


// Video
let video;
//let flippedVideo;
// To store the classification
let label = "Waiting...";

// Load the model first
function preload() {
  classifier = ml5.imageClassifier(imageModelURL + 'model.json');
}

function setup() {
  createCanvas(320, 260);
  // Create the video
  video = createCapture(VIDEO,{flipped:true});
  video.size(width, height);
  video.hide();

  //flippedVideo = ml5.flipImage(video)
  // Start classifying
  classifyVideo();
}

function draw() {
  background(0);
  // Draw the video
  image(video, 0, 0);

  // Draw the label
  fill(255);
  textSize(16);
  textAlign(CENTER);
  text(label, width / 2, height - 4);
}

// Get a prediction for the current video frame
function classifyVideo() {
  //flippedVideo = ml5.flipImage(video)
  classifier.classifyStart(video, gotResult);
}

// When we get a result
function gotResult(results) {
  // console.log(results[0]);
  label = results[0].label;
}