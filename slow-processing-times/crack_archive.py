import os, time
from flask import (
    Blueprint, g, request, jsonify
)
from enum import Enum

from slow_processing_times.db import get_db

bp = Blueprint('crack_archive', __name__, url_prefix='/crack')
archive_cracks = {}
job_count = 0

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
            'is_cracked': self.is_cracked,
            'password': self.password
        }

@bp.route('/<filename>', methods=['GET'])
def crack(filename):
    #candidate to refactoring
    if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
        resp = jsonify({'file': filename, 'message': 'File not found'})
        resp.status_code = 400
        return resp
    
    global job_count
    if job_count < app.config['JOBS_LIMIT']:
        job_count += 1
        archive_cracks[filename].state = State.CRACKING
        time.sleep(10)
        password = 'the-password'
        archive_cracks[filename].state = State.CRACKED
        archive_cracks[filename].is_cracked = True
        archive_cracks[filename].password = password
        job_count -= 1
        resp = jsonify({'file': filename, 'message': 'Crack successful!', 'password': password})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Jobs limit reached'})
        resp.status_code = 201
        return resp)