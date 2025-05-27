from flask import Flask, request, send_file, render_template
import os

app = Flask(__name__, template_folder='templates')
UPLOAD_PATH = '/tmp'
RECORD_FILE = 'record.wav'

@app.route('/')
def index():
    exists = os.path.exists(os.path.join(UPLOAD_PATH, RECORD_FILE))
    return render_template('amthanh.html', audio_exists=exists)

@app.route('/upload', methods=['POST'])
def upload():
    file_path = os.path.join(UPLOAD_PATH, RECORD_FILE)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Stream upload: read request body in chunks
    with open(file_path, 'wb') as f:
        chunk_size = 1024 * 16
        while True:
            chunk = request.stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
    return 'OK', 200

@app.route('/audio')
def get_audio():
    file_path = os.path.join(UPLOAD_PATH, RECORD_FILE)
    if not os.path.exists(file_path):
        return 'Not Found', 404
    return send_file(file_path, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
