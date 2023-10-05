from flask import Flask, request, jsonify
from voice_to_text import audio_check
from flask_cors import CORS
import speech_recognition as sr
from pydub import AudioSegment
import os
from io import BytesIO
# AudioSegment.converter = "path/to/ffmpeg"
# AudioSegment.ffmpeg = "path/to/ffmpeg"
# AudioSegment.ffprobe = "path/to/ffprobe"
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/compare_audio', methods=['GET', 'POST'])
def audio_to_text():
    paragraph = request.form.get('paragraph')
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # audio_format = file.filename.split('.')[-1]
    try:
        audio = AudioSegment.from_file(file, format="webm", codec="opus")
        audio = audio.set_channels(1).set_frame_rate(16000)
    except Exception as e:
        return jsonify({"error": f"Could not decode file: {e}"}), 400

    return audio_check(audio, paragraph)


if __name__ == '__main__':
    app.run()