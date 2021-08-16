import os
from flask import (
    Blueprint, request, current_app
)
from werkzeug.utils import secure_filename

from .. import utils
from ..enums.state_enum import State
from ..entities.archive_info_entity import ArchiveInfo
from ..blueprints.crack import archives

bp = Blueprint('archive', __name__, url_prefix='/archive')

ALLOWED_EXTENSIONS = set(['zip', ]) # Other extensions may be added
def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_archive():
    if 'file' not in request.files:
        return utils.create_response({'message' : 'No file part in the request'}, 400)   
    
    file = request.files['file']

    if file.filename == '':
        return utils.create_response({'message' : 'No file selected for uploading'}, 400)
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        archives[filename] = ArchiveInfo(state=State.UPLOADING)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        archives[filename].state = State.UPLOADED
        return utils.create_response({'message' : 'File successfully uploaded'}, 201)
    else:
        return utils.create_response({'message' : 'Allowed file types are .rar and .zip'}, 400)

@bp.route('/password', methods=['POST'])
def get_archive_password():
    print(utils.check_filename_in(request).content_length)

    data = request.get_json()
    if data is None:
        return utils.create_response({'message': 'Error: mimetype is not application/json'}, 400)
    try:
        filename = data['filename']
    except KeyError:
        return utils.create_response({'message': 'Key is not recognized. Use \'filename\''}, 400)

    if not utils.archive_exists(filename):
        return utils.create_response({'file': filename, 'message': 'File not found'}, 400)
        
    return utils.create_response({'filename': filename, 'archive_info': archives[filename].serialize()}, 201)
