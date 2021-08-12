import os, time
from flask import (
    Blueprint, request, current_app
)
from werkzeug.exceptions import Unauthorized

from .. import utils
from ..enums.state_enum import State
from slow_processing_times.db import get_db

bp = Blueprint('crack', __name__, url_prefix='/crack')

# Global
job_count = 0
archive_cracks = {}

@bp.route('/<filename>', methods=['GET'])
def crack(filename):
    if not utils.archive_exists(filename):
        return utils.createResponse({'file': filename, 'message': 'File not found'}, 400)
    
    global job_count
    if job_count < current_app.config['JOBS_LIMIT']:
        job_count += 1
        db = get_db()
        for row in db.execute("SELECT * FROM cracked_password"):
            if row['filename'] == filename: #TODO: use checksum
                return utils.createResponse(
                {
                    'message': 'Archive has already been cracked', 
                    'archive_info': archive_cracks[filename].serialize()
                }
                , 201)
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
        except db.IntegrityError:
            return utils.createResponse(
                {
                    'message': 'Crack successful but there was an error updating the database. Duplicate checksum?', 
                    'password': password
                }
                , 400)
        else:
            archive_cracks[filename].state = State.CRACKED
            archive_cracks[filename].is_cracked = True
            archive_cracks[filename].password = password
            return utils.createResponse({'file': filename, 'message': 'Crack successful!', 'password': password}, 201)
    else:
        return utils.createResponse({'message': 'Jobs limit reached'}, 201)

@bp.route('/jobs', methods=['GET','POST'])
def jobs():
    if request.method == 'GET':
        return utils.createResponse({'current_jobs_limit': current_app.config['JOBS_LIMIT']}, 201)
    else:
        data = request.get_json()
        if data is None:
            return utils.createResponse({'message': 'Error: mimetype is not application/json'}, 400)
        else:
            try:
                new_jobs_limit = data['jobs_limit']
                current_app.config['JOBS_LIMIT'] = new_jobs_limit
            except KeyError:
                return utils.createResponse({'message': 'Key is not recognized. Use \'jobs_limit\''}, 400)
            else:
                return utils.createResponse({'new_jobs_limit': current_app.config['JOBS_LIMIT']}, 400)