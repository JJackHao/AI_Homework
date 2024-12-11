from flask import Flask, request, jsonify, render_template
import os

# from pydub import AudioSegment
from model_milestone3 import runModels

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def validate_and_process_wav(input_path, output_path):
#     try:
#         audio = AudioSegment.from_file(input_path)
#         audio.export(output_path, format="wav")
#         return output_path
#     except Exception as e:
#         raise ValueError(f"Invalid WAV file: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-data', methods=['POST'])
def process_data():
    image = request.files.get('image')
    audio = request.files.get('audio')
    image_path = None
    audio_path = None

    if image:
        image_path = os.path.join(UPLOAD_FOLDER, 'capture.png')
        image.save(image_path)

    if audio:
        audio_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
        audio.save(audio_path)
        # raw_audio_path = os.path.join(UPLOAD_FOLDER, 'raw_recording.wav')
        # processed_audio_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
        # audio.save(raw_audio_path)

        # # Validate and process the WAV file
        # try:
        #     audio_path = validate_and_process_wav(raw_audio_path, processed_audio_path)
        # except ValueError as e:
        #     return jsonify({'message': str(e)}), 400
        
    if not image_path or not audio_path:
        return jsonify({'message': 'No image or audio received!'}), 400

    # Run models
    if image_path and audio_path:
        response = runModels("uploads/capture.png", "uploads/recording.wav")

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)