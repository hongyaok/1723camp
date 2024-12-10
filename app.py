from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify, send_from_directory
import os
import random
from score import scores

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
global port
port = int(os.environ.get('PORT', 5000))
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creatorgallery')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def homepage():
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    
    return render_template('index.html', data = scores)

@app.route('/creators_gallery')
def creators_gallery():
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.webp', '.JPG'))]
    size_classes = ['random-size-small', 'random-size-medium', 'random-size-large']
    images = [
        {
            'filename': img,
            'size_class': random.choice(size_classes)  
        }
        for img in image_files
    ]
    random.shuffle(images)
    return render_template('creators_gallery.html', images=images)

@app.route('/creatorgallery/<filename>')
def gall_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)

