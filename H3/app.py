from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is in the templates folder

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        image.save(os.path.join(UPLOAD_FOLDER, 'capture.png'))
        return jsonify({'message': 'Image saved!'})
    return jsonify({'message': 'No image received!'}), 400

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio = request.files['audio']
        audio.save(os.path.join(UPLOAD_FOLDER, 'recording.wav'))
        return jsonify({'message': 'Audio saved!'})
    return jsonify({'message': 'No audio received!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
