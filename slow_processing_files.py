import os
import time
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from enum import Enum

class State(str, Enum):
    NONE      = 'None'
    UPLOADING = 'Uploading'
    UPLOADED  = 'Uploaded'
    CRACKING  = 'Cracking'
    CRACKED   = 'Cracked'

class ArchiveInfo:
    state = State.NONE
    is_cracked = False
    password = None

    def serialize(self):  
        return {           
            'state': self.state,
            'is_cracked': self.cracked,
            'password': self.password
        }

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['zip', 'rar'])

archive_cracks = {}

def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_archive():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp      
        
    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        archive_cracks[filename] = ArchiveInfo()
        archive_cracks[filename].state = State.UPLOADING
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        archive_cracks[filename].state = State.UPLOADED
        resp = jsonify({'message' : 'File successfully uploaded', 'filename': filename, 'archive_info': archive_cracks[filename].serialize()})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are .rar and .zip'})
        resp.status_code = 400
        return resp

@app.route('/crack/<filename>', methods=['GET'])
def crack(filename):
    if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
        return jsonify({'file': filename, 'message': 'File not found'})
    archive_cracks[filename].state = State.CRACKING
    time.sleep(10)
    archive_cracks[filename].state = State.CRACKED
    return jsonify({'file': filename, 'message': 'Crack successful!', 'password': 'the-password'})