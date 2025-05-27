from flask import Flask, request, send_from_directory, jsonify, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('amthanh.html')

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    audio = request.files.get('file')
    if not audio:
        return jsonify({'error':'No file provided'}), 400
    filepath = os.path.join(UPLOAD_FOLDER, 'record.wav')
    audio.save(filepath)
    return jsonify({'status':'ok'}), 200

@app.route('/api/play')
def play_audio():
    return send_from_directory(UPLOAD_FOLDER, 'record.wav', mimetype='audio/wav')


if __name__ == '__main__':
    app.run(debug=True)
