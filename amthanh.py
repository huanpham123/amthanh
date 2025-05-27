from flask import Flask, request, send_file, render_template
import os

app = Flask(__name__, template_folder='templates')

# Lưu vào /tmp thay vì static
UPLOAD_PATH = '/tmp'
RECORD_FILE = 'record.wav'

@app.route('/')
def index():
    file_path = os.path.join(UPLOAD_PATH, RECORD_FILE)
    exists = os.path.exists(file_path)
    return render_template('amthanh.html', audio_exists=exists)

@app.route('/upload', methods=['POST'])
def upload():
    file_path = os.path.join(UPLOAD_PATH, RECORD_FILE)
    # Xóa nếu tồn tại
    if os.path.exists(file_path):
        os.remove(file_path)

    # Hỗ trợ raw body
    data = request.get_data()
    if not data:
        return 'No data', 400

    # Lưu file
    with open(file_path, 'wb') as f:
        f.write(data)
    return 'OK', 200

@app.route('/audio')
def get_audio():
    file_path = os.path.join(UPLOAD_PATH, RECORD_FILE)
    if not os.path.exists(file_path):
        return 'Not Found', 404
    return send_file(file_path, mimetype='audio/wav')
