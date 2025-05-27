from flask import Flask, request, send_file, render_template, Response
import os
from tempfile import NamedTemporaryFile
from datetime import datetime

app = Flask(__name__, template_folder='templates')
UPLOAD_DIR = '/tmp'

@app.route('/')
def index():
    audio_exists = os.path.exists(os.path.join(UPLOAD_DIR, 'record.wav'))
    return render_template('amthanh.html', audio_exists=audio_exists)

@app.route('/upload', methods=['POST'])
def upload():
    # Tạo file tạm với timestamp để tránh xung đột
    temp_filename = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    try:
        with open(temp_path, 'wb') as f:
            # Đọc dữ liệu theo chunks 4KB
            while True:
                chunk = request.stream.read(4096)
                if not chunk:
                    break
                f.write(chunk)
        
        # Đổi tên file tạm thành file chính thức
        final_path = os.path.join(UPLOAD_DIR, 'record.wav')
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(temp_path, final_path)
        
        return 'Upload thành công', 200
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return f'Lỗi: {str(e)}', 500

@app.route('/audio')
def get_audio():
    audio_path = os.path.join(UPLOAD_DIR, 'record.wav')
    if not os.path.exists(audio_path):
        return 'Không tìm thấy file âm thanh', 404
    
    # Stream audio với chunked transfer
    def generate():
        with open(audio_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                yield chunk
    
    return Response(generate(), mimetype='audio/wav')

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
