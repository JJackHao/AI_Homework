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

    whisper_processor = AutoProcessor.from_pretrained("openai/whisper-small")
    whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-small")
    # Decode the base64 audio data and process using Whisper
    with open(audio_path, "rb") as f:
        riff = f.read(4)
        if riff != b"RIFF":
            raise ValueError("File does not start with RIFF id. Please provide a valid WAV file.")

    with wave.open(audio_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)

    speech_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    if frame_rate != 16000:
        target_length = int(len(speech_array) * 16000 / frame_rate)
        speech_array = resample(speech_array, target_length)
        frame_rate = 16000

    input_features = whisper_processor(speech_array, sampling_rate=frame_rate, return_tensors="pt").input_features

    generated_ids = whisper_model.generate(input_features)
    transcription = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return transcription

def process_text_sentiment(text):
    # Analyze sentiment of the transcribed text
    sentiment_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

    inputs = sentiment_tokenizer(text, return_tensors="pt")
    outputs = sentiment_model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    labels = ["Negative", "Neutral", "Positive"]
    highest_prob_index = torch.argmax(probs, dim=1).item()
    result = labels[highest_prob_index]
    return result

def generate_response(facial_sentiment, text_sentiment, text):
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
                        f"The speech sentiment detected is: {text_sentiment}. "
                        f"The speech detected is: {text}"
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

def runModels(url1, url2):

    # Process facial sentiment if image is provided
    if url1:
        facial_sentiment = process_facial_sentiment(url1)

    # Process speech-to-text if audio is provided
    if url2:
        speech_text = process_speech_to_text(url2)

        if speech_text:
            # Process text sentiment if speech text is available
            text_sentiment = process_text_sentiment(speech_text)

    # Generate final response using facial and text sentiments
    if facial_sentiment is not None or text_sentiment is not None:
        response = generate_response(facial_sentiment, text_sentiment, speech_text)

    return response