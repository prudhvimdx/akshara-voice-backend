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

    


@app.route('/compare_audio3', methods=['GET', 'POST'])
def hello_world():
    # data = request.get_json()
    # audio_file = request.files.get('audio')
    paragraph = request.form.get('paragraph')
    print("DATA Print", paragraph)
    # print("DATA Print", audio_file)
    file = request.files['audio']
    audio_data = file.read()
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio_file.write(audio_data)
    temp_audio_file.close()

    # source_audio = AudioSegment.from_file(BytesIO(audio_file), format="flac")
    # print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZzz")
    # wav_audio = source_audio.set_channels(1).set_frame_rate(16000)
    # print("Content Type:", wav_audio.content_type)  # Check the content type
    # # # Check the file header
    # header = wav_audio.read(4)
    # print("File Header:", header)
    # wav_audio.seek(0)  # Seek back to the start of the file
    
    # if header != b'RIFF':
    #     return jsonify({'error': 'Invalid WAV file'}), 400

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # original_text = "The speaker is speaking too quickly or too slowly. Google Speech Recognition is trained on a variety of speech speeds, but it may not be able to accurately transcribe audio that is outside of its expected range."
    return audio_check(temp_audio_file.name, paragraph)


@app.route('/compare_audio2', methods=['GET', 'POST'])
def hello_world_data():
    # data = request.get_json()
    audio_file = request.files.get('audio')
    paragraph = request.form.get('paragraph')
    print("DATA Print", paragraph)
    print("DATA Print", audio_file)

    webm_audio = AudioSegment.from_file(audio_file, format="webm")
    wav_data = webm_audio.set_channels(1).set_frame_rate(16000)  # Adjust as needed
    wav_buffer = BytesIO()
    wav_data.export(wav_buffer, format="wav")

    # Return the WAV data as a downloadable file
    wav_buffer.seek(0)

    return audio_check(wav_buffer, paragraph)



@app.route('/compare_audio1', methods=['GET', 'POST'])
def hello_world_dat():
    # data = request.get_json()
    audio_file = request.files.get('audio')
    paragraph = request.form.get('paragraph')
    print("DATA Print", paragraph)
    print("DATA Print", audio_file)

    import ffmpeg
    input_file = ffmpeg.input(audio_file)
    output_file = ffmpeg.output(input_file, 'output.wav', codec='pcm_s16le', sample_rate=44100) #h246
    # output_file.audio.codec('pcm_s16le')
    # output_file.audio.sample_rate(44100)
    output_file.run()

    return audio_check(output_file, paragraph)

if __name__ == '__main__':
    app.run()