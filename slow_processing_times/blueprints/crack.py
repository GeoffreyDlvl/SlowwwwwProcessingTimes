import os, time
from flask import (
    Blueprint, g, request, jsonify, current_app
)

from ..enums.state_enum import State
from ..entities.archive_info_entity import ArchiveInfo
from slow_processing_times.db import get_db

bp = Blueprint('crack', __name__, url_prefix='/crack')

# Global
job_count = 0
archive_cracks = {}

# Init - TODO: load from db
#for archive_name in os.listdir(current_app.config['UPLOAD_FOLDER']):
#    archive_cracks[archive_name] = ArchiveInfo()
archive_cracks["myarchive.zip"] = ArchiveInfo()

@bp.route('/<filename>', methods=['GET'])
def crack(filename):
    #candidate to refactoring
    if filename not in os.listdir(current_app.config['UPLOAD_FOLDER']):
        resp = jsonify({'file': filename, 'message': 'File not found'})
        resp.status_code = 400
        return resp
    
    global job_count
    if job_count < current_app.config['JOBS_LIMIT']:
        job_count += 1
        db = get_db()
        # TODO: Check if archive has already been cracked
        archive_cracks[filename].state = State.CRACKING
        time.sleep(10)
        job_count -= 1
        password = 'the-password'
        try:
            db.execute(
                "INSERT INTO cracked_password (md5_checksum, filename, password) VALUES (?, ?, ?)",
                ("the_checksum", filename, password),
            )
            db.commit()
        except db.IntegrityError: #TODO: get this before crack attempt
            resp = jsonify({'message': 'Archive has already been cracked', 
            'archive_info': archive_cracks[filename].serialize()})
            resp.status_code = 201
            return resp
        else:
            archive_cracks[filename].state = State.CRACKED
            archive_cracks[filename].is_cracked = True
            archive_cracks[filename].password = password
            resp = jsonify({'file': filename, 'message': 'Crack successful!', 'password': password})
            resp.status_code = 201
            return resp
    else:
        resp = jsonify({'message': 'Jobs limit reached'})
        resp.status_code = 201
        return resp

@bp.route('/jobs', methods=['GET','POST'])
def jobs():
    if request.method == 'GET':
        resp = jsonify({'current_jobs_limit': current_app.config['JOBS_LIMIT']})
        resp.status_code = 201
        return resp
    else:
        data = request.get_json()
        if data is None:
            resp = jsonify({'message': 'Error: mimetype is not application/json'})
            resp.status_code = 400
            return resp
        else:
            try:
                new_jobs_limit = data['jobs_limit']
                current_app.config['JOBS_LIMIT'] = new_jobs_limit
                resp = jsonify({'new_jobs_limit': current_app.config['JOBS_LIMIT']})
                resp.status_code = 201
                return resp
            except KeyError:
                resp = jsonify({'message': 'Key is not recognized. Use \'jobs_limit\''})
                resp.status_code = 400
                return resp