let divData, story_text, speech, startBtn, stopBtn, canvas;

let slectedImg, horrorImg, fantasyImg, adventureImg, comedyImg, mysteryImg, romanceImg;

let img_is_selected = false;


function preload(){
    horrorImg = loadImage("imgs/horror.jpg"); 
    fantasyImg = loadImage("imgs/fantasy.jpg"); 
    adventureImg = loadImage("imgs/adventure.jpg"); 
    comedyImg = loadImage("imgs/comedy.jpg"); 
    mysteryImg = loadImage("imgs/mystery.jpg"); 
    romanceImg = loadImage("imgs/romance.jpg"); 
    // slectedImg = horrorImg ;
    // story_style = "Horror";
}


function setup(){
    canvas = createCanvas(600,800);
    canvas.parent('canvas-div');
    divData = document.querySelector("#canvas-div");

    speech = new p5.Speech(); // speech synthesis object
    
    story_style = divData.dataset.style;

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

    story_text = divData.dataset.story;

    display_text = "Story style: "+story_style+"\n"+"\n"+story_text

    if(img_is_selected ===true){
        tint(95,95,95, 255);
        image(slectedImg,0,0,600,800);
        
    }

    

    textSize(18);
    textWrap(WORD);
    text(display_text, width/2,height/2, width-100, height-100);
    
    
}


function startSpeaking(){
    if(story_text !== "Waiting for the story..."){

        if(story_style === "Horror"){
            slectedImg = horrorImg;
            img_is_selected = true;
            speech.setVoice(0);
            speech.setPitch(0.01);
            speech.setRate(0.5);
            speech.speak(story_text);
        }
        else if(story_style === "Fantasy"){
            slectedImg = fantasyImg;
            img_is_selected = true;
            speech.setVoice(1);
            speech.setPitch(1);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Adventure"){
            slectedImg = adventureImg;
            img_is_selected = true;
            speech.setVoice(1);
            speech.setPitch(1.5);
            speech.setRate(1.5);
            speech.speak(story_text);
        }
        else if(story_style === "Comedy"){
            slectedImg = comedyImg;
            img_is_selected = true;
            speech.setVoice(2);
            speech.setPitch(2);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Mystery"){
            slectedImg = mysteryImg;
            img_is_selected = true;
            speech.setVoice(0);
            speech.setPitch(2);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else if(story_style === "Romance"){
            slectedImg = romanceImg;
            img_is_selected = true;
            speech.setVoice(2);
            speech.setPitch(1);
            speech.setRate(1);
            speech.speak(story_text);
        }
        else{
            speech.setVoice(0);
            speech.setPitch(1.0);
            speech.setRate(1.0);
            speech.speak(story_text);

        }

        // speech.listVoices();
        
    }
}

function stopSpeaking(){
    speech.stop();
}