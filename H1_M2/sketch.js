let confidence;
let recordedLabel;
let recordedConfidence;
let finalConfidence;

let button;

// Classifier Variable
let classifier, sentiment;
// Model URL
let imageModelURL = 'https://teachablemachine.withgoogle.com/models/bVIx6PNIy/';

// Video
let video;
//let flippedVideo;
// To store the classification
let label = "Waiting...";
let sentimentResult = 0;
let userInput;

// Load the model first
function preload() {
  classifier = ml5.imageClassifier(imageModelURL + 'model.json');
  sentiment = ml5.sentiment('movieReviews');
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
  
  // button = createButton('Record Label and Confidence');
  // button.position(10, height + 260); // Position it below the canvas
  // button.mousePressed(recordLabelAndConfidence);
  
  userInput = createInput();
  userInput.position(10, height + 240);
  
  let analyzeButton = createButton('Submit');
  analyzeButton.position(userInput.x + userInput.width + 10, height + 240);
  analyzeButton.mousePressed(analyze);
}

function draw() {
  background(0);
  // Draw the video
  image(video, 0, 0);

  // Draw the label
  fill(255);
  textSize(16);
  textAlign(CENTER);
  
  if (recordedLabel === 'Pass') {
    finalConfidence = parseFloat(recordedConfidence) + sentimentResult;
    console.log(finalConfidence);
    if (finalConfidence > 1) {
      text("Pass", width / 2, height - 30);
      //console.log(1);
    } else {
      text("Kill", width / 2, height - 30);
    }
  } else if (recordedLabel === 'kill') {
    finalConfidence = 1 - parseFloat(recordedConfidence) + sentimentResult;
    if (finalConfidence < 1) {
      text("Kill", width / 2, height - 30);
      //console.log(2);
    } else {
      text("Pass", width / 2, height - 30);
    }
  }
    
  //text(`${label} (${confidence * 100}%)`, width / 2, height - 4);
  //text(recordedLabel, width / 2, height - 30);
  //text(`Confidence: ${(recordedConfidence * 100).toFixed(2)}%`, width / 2, height - 10);
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
  confidence = results[0].confidence.toFixed(2);
}

// function recordLabelAndConfidence() {
//   // Store the current label and confidence when the button is pressed
//   recordedLabel = label;
//   recordedConfidence = confidence;
// }

function analyze() {
  let sentence = userInput.value();
  sentiment.predict(sentence, gotSResult);
  
  recordedLabel = label;
  recordedConfidence = confidence;
  console.log(sentimentResult);
}

function gotSResult(prediction) {
  // Display sentiment result via the DOM
  sentimentResult = prediction.confidence;
  //console.log(sentimentResult);
}