from transformers import pipeline
import openai
from openai import OpenAI
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import wave
import numpy as np
from scipy.signal import resample
import torch
import os

def process_facial_sentiment(image_data):
    # Decode the base64 image data and process using facial emotion model
    face_emotion_model = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
    results = face_emotion_model(image_data)
    return results[0]

def process_speech_to_text(audio_path):
    # Decode the base64 audio data and process using Whisper
    with open(audio_path, "rb") as f:
        riff = f.read(4)
        if riff != b"RIFF":
            raise ValueError("File does not start with RIFF id. Please provide a valid WAV file.")

    with wave.open(audio_path, "rb") as wf:
        frame_rate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)

    speech_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    if frame_rate != 16000:
        target_length = int(len(speech_array) * 16000 / frame_rate)
        speech_array = resample(speech_array, target_length)
        frame_rate = 16000
    whisper_processor = AutoProcessor.from_pretrained("openai/whisper-small")
    whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-small")
    audio_features = whisper_processor(audio_data, sampling_rate=16000, return_tensors="pt").input_features
    transcription = whisper_model.generate(audio_features)
    return whisper_processor.batch_decode(transcription, skip_special_tokens=True)[0]

def process_text_sentiment(text):
    # Analyze sentiment of the transcribed text
    sentiment_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

    inputs = sentiment_tokenizer(text, return_tensors="pt")
    outputs = sentiment_model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    labels = ["Negative", "Neutral", "Positive"]
    result = {labels[i]: float(probs[0][i]) for i in range(len(labels))}
    return result

def generate_response(facial_sentiment, text_sentiment):
    """
    msg should be a dict of the form - {"role": "user", "content": scenario}
    """
    client = OpenAI()

    msg_list=[
                {"role": "system", "content": "You are a helpful assistant generating encouraging responses to a CS2 gamer."},
                {
                    "role": "user",
                    "content": (
                        f"The facial sentiment detected is: {facial_sentiment}. "
                        f"The text sentiment detected is: {text_sentiment}. "
                        "Combine these sentiments and generate an encouraging response to a CS2 gamer."
                    )
                }
            ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        max_completion_tokens= 200,
        messages= msg_list
    )
    # print(response)
    out_message = response.choices[0].message.content
    return out_message
