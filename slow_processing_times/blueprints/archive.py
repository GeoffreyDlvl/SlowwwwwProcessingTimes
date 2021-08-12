import os
from flask import (
    Blueprint, request, current_app
)
from werkzeug.utils import secure_filename

from .. import utils
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
        return utils.createResponse({'message' : 'No file part in the request'}, 400)   
    
    file = request.files['file']

    if file.filename == '':
        return utils.createResponse({'message' : 'No file selected for uploading'}, 400)
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        archive_cracks[filename] = ArchiveInfo()
        archive_cracks[filename].state = State.UPLOADING
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        archive_cracks[filename].state = State.UPLOADED
        return utils.createResponse({'message' : 'File successfully uploaded'}, 201)
    else:
        return utils.createResponse({'message' : 'Allowed file types are .rar and .zip'}, 400)

@bp.route('/password', methods=['POST'])
def get_archive_password():
    data = request.get_json()
    if data is None:
        return utils.createResponse({'message': 'Error: mimetype is not application/json'}, 400)
    try:
        filename = data['filename']
    except KeyError:
        return utils.createResponse({'message': 'Key is not recognized. Use \'filename\''}, 400)

    if not utils.archive_exists(filename):
        return utils.createResponse({'file': filename, 'message': 'File not found'}, 400)
        
    return utils.createResponse({'filename': filename, 'archive_info': archive_cracks[filename].serialize()}, 201)