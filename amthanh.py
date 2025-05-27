from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
RECORD_FILE = 'record.wav'

@app.route('/')
def index():
    # Kiểm tra file ghi âm
    audio_path = os.path.join(UPLOAD_FOLDER, RECORD_FILE)
    audio_exists = os.path.exists(audio_path)
    return render_template('amthanh.html', audio_exists=audio_exists)

@app.route('/upload', methods=['POST'])
def upload():
    # Xóa file cũ nếu có
    file_path = os.path.join(UPLOAD_FOLDER, RECORD_FILE)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Nhận file WAV từ client
    audio = request.files.get('audio')
    if not audio:
        return 'Không tìm thấy file audio', 400

    audio.save(file_path)
    return 'Upload thành công', 200

@app.route('/audio')
def get_audio():
    # Trả file WAV để phát
    return send_from_directory(UPLOAD_FOLDER, RECORD_FILE)

if __name__ == '__main__':
    # Local dev
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)