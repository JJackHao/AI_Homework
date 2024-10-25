let divData, story_text, speech, startBtn, stopBtn;


function setup(){
    let c = createCanvas(600,600);
    c.parent('canvas-div');
    divData = document.querySelector("#canvas-div");

    speech = new p5.Speech(); // speech synthesis object

    //start button setup
    let startBtnDiv = document.querySelector('#startBtnDiv');
    startBtn = createButton('Start Narrating!');
    startBtn.parent(startBtnDiv);
    startBtn.class('btn btn-primary');
    startBtn.mousePressed(startSpeaking);

    //stop button setup
    let stopBtnDiv = document.querySelector('#stopBtnDiv');
    stopBtn = createButton('Stop Narrating!');
    stopBtn.parent(stopBtnDiv);
    stopBtn.class('btn btn-danger');
    stopBtn.mousePressed(stopSpeaking);

}

function draw(){
    background(33,33,33);
    fill(255);

    rectMode(CENTER);

    story_text = divData.dataset.story

    textSize(18);
    textWrap(WORD);
    text(story_text, width/2,height/2, width-100, height-100);
    
    
}


function startSpeaking(){
    if(story_text !== "Waiting for the story..."){
        speech.speak(story_text);
    }
}

function stopSpeaking(){
    speech.stop();
}