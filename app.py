from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'Remote Gallery Access Server Running'

@app.route('/upload_gallery', methods=['POST'])
def upload_gallery():
    if 'images' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    image = request.files['images']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filepath)
    return jsonify({'message': f'Image {image.filename} uploaded successfully'}), 200

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads')
def list_uploaded_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_urls = [
        f"https://fixedremotegalleryaccess-1.onrender.com/uploads/{filename}"
        for filename in files
    ]
    return jsonify(file_urls)

if __name__ == '__main__':
    app.run(debug=True)