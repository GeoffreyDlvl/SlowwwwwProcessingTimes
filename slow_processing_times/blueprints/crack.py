import time
from flask import (
    Blueprint, request, current_app
)

from .. import utils
from ..enums.state_enum import State
from slow_processing_times.db import get_db

bp = Blueprint('crack', __name__, url_prefix='/crack')

# Global
job_count = 0
archives = {}

@bp.route('/', methods=['POST'])
def crack():
    response = utils.check_filename_in(request)
    if not utils.is_response_empty(response):
        return response
    filename = utils.get_filename_from(request)
        
    if not utils.archive_exists(filename):
        return utils.create_response({'file': filename, 'message': 'File not found'}, 400)
    
    global job_count
    if job_count < current_app.config['JOBS_LIMIT']:
        job_count += 1
        db = get_db()
        for row in db.execute("SELECT * FROM cracked_password"):
            if row['md5_checksum'] == utils.compute_checksum(filename):
                return utils.create_response(
                {
                    'message': 'Archive has already been cracked', 
                    'archive_info': archives[row['filename']].serialize()
                }
                , 201)
        archives[filename].state = State.CRACKING
        time.sleep(10)
        job_count -= 1
        password = 'the-password'
        try:
            db.execute(
                "INSERT INTO cracked_password (md5_checksum, filename, password) VALUES (?, ?, ?)",
                (utils.compute_checksum(filename), filename, password),
            )
            db.commit()
        except db.IntegrityError:
            return utils.create_response(
                {
                    'message': 'Crack successful but there was an error updating the database.', 
                    'password': password
                }
                , 400)
        else:
            archives[filename].state = State.CRACKED
            archives[filename].is_cracked = True
            archives[filename].password = password
            return utils.create_response({'file': filename, 'message': 'Crack successful!', 'password': password}, 201)
    else:
        return utils.create_response({'message': 'Jobs limit reached'}, 201)

@bp.route('/jobs', methods=['GET','POST'])
def jobs():
    if request.method == 'GET':
        return utils.create_response({'current_jobs_limit': current_app.config['JOBS_LIMIT']}, 201)
    else:
        data = request.get_json()
        if data is None:
            return utils.create_response({'message': 'Error: mimetype is not application/json'}, 400)
        else:
            try:
                new_jobs_limit = data['jobs_limit']
                current_app.config['JOBS_LIMIT'] = new_jobs_limit
            except KeyError:
                return utils.create_response({'message': 'Key is not recognized. Use \'jobs_limit\''}, 400)
            else:
                return utils.create_response({'new_jobs_limit': current_app.config['JOBS_LIMIT']}, 400)