from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import logging
from flask_cors import CORS
from chat.text_chat import get_bot_reply
from chat.voice_chat import transcribe_audio
from chat.tts_response import generate_tts
from mood.logger import get_mood_log
from relax.breathing import get_breathing_tips

try:
    from relax.resources import get_resources
except ImportError:
    def get_resources():
        return [
            {"title": "Mental Health Hotline", "url": "https://www.example.com"},
            {"title": "Meditation Guide", "url": "https://www.example.com"}
        ]

from journal.entries import save_entry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "static/audio"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def cleanup_files(directory, max_files=100):
    files = sorted(os.listdir(directory), key=lambda x: os.path.getctime(os.path.join(directory, x)))
    if len(files) > max_files:
        for file in files[:-10]:
            try:
                os.remove(os.path.join(directory, file))
            except OSError:
                pass

@app.route('/chat/text', methods=['POST'])
def chat_text():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    response = get_bot_reply(user_message)
    response_text = "\n".join(response["lines"])
    audio_path = generate_tts(response_text)
    audio_filename = os.path.basename(audio_path) if audio_path else None
    cleanup_files(app.config['AUDIO_FOLDER'])
    return jsonify({
        "lines": response["lines"],
        "emotion": response["emotion"],
        "audio": audio_filename
    })

@app.route('/chat/voice', methods=['POST'])
def chat_voice():
    logger.info("Voice endpoint hit")
    if 'audio' not in request.files:
        logger.error("No audio file provided")
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    logger.info(f"Received file: {file.filename}")
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    transcript = transcribe_audio(file_path)
    response = get_bot_reply(transcript)
    response_text = "\n".join(response["lines"])
    audio_path = generate_tts(response_text)
    audio_filename = os.path.basename(audio_path) if audio_path else None
    cleanup_files(app.config['UPLOAD_FOLDER'])
    cleanup_files(app.config['AUDIO_FOLDER'])
    return jsonify({
        "transcript": transcript,
        "lines": response["lines"],
        "emotion": response["emotion"],
        "audio": audio_filename
    })

@app.route('/audio/<filename>')
def serve_audio(filename):
    try:
        return send_file(os.path.join(app.config['AUDIO_FOLDER'], filename), mimetype="audio/wav")
    except FileNotFoundError:
        logger.error(f"Audio file not found: {filename}")
        return jsonify({"error": "Audio file not found"}), 404

@app.route('/mood/log', methods=['GET'])
def mood_log():
    log = get_mood_log()
    return jsonify(log)

@app.route('/relax/breathing', methods=['GET'])
def breathing_tips():
    return jsonify(get_breathing_tips())

@app.route('/relax/resources', methods=['GET'])
def mental_health_resources():
    return jsonify(get_resources())

@app.route('/journal', methods=['POST'])
def journal_entry():
    data = request.json
    entry = data.get("entry", "")
    if not entry:
        return jsonify({"error": "No journal entry provided"}), 400
    message = save_entry(entry)
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)