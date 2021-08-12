import os
from flask import (
    Blueprint, g, request, jsonify, current_app
)
from werkzeug.utils import secure_filename

from ..enums.state_enum import State
from ..entities.archive_info_entity import ArchiveInfo
from ..blueprints.crack import archive_cracks

bp = Blueprint('archive', __name__, url_prefix='/archive')

ALLOWED_EXTENSIONS = set(['zip', ]) # Other extensions may be added
def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_archive():
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
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        archive_cracks[filename].state = State.UPLOADED
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are .rar and .zip'})
        resp.status_code = 400
        return resp

@bp.route('/password', methods=['POST'])
def get_archive_password():
    data = request.get_json()
    if data is None:
        resp = jsonify({'message': 'Error: mimetype is not application/json'})
        resp.status_code = 400
        return resp
    try:
        filename = data['filename']
    except KeyError:
        resp = jsonify({'message': 'Key is not recognized. Use \'filename\''})
        resp.status_code = 400
        return resp

    #candidate to refactoring
    if filename not in os.listdir(current_app.config['UPLOAD_FOLDER']):
        resp = jsonify({'file': filename, 'message': 'File not found'})
        resp.status_code = 400
        return resp
    resp = jsonify({'filename': filename, 'archive_info': archive_cracks[filename].serialize()})
    resp.status_code = 201
    return resp