import time
from flask import (
    Blueprint, request, current_app
)

from .. import utils
from ..enums.state_enum import State
from ..blueprints.crack import archives

bp = Blueprint('processing', __name__, url_prefix='/processing')

def some_processing():
    print('PROCESSING...')
    time.sleep(10)
    print('DONE.')

@bp.route('some_processing', methods=['POST'])
def append_some_processing():
    response = utils.check_filename_in(request)
    if not utils.is_response_empty(response):
        return response
    filename = utils.get_filename_from(request)
        
    if not utils.archive_exists(filename):
        return utils.create_response({'file': filename, 'message': 'File not found'}, 400)

    archive = archives[filename]
    archive.append_processing(some_processing)

    if archive.state is not State.PROCESSING:
        archive.start_processing()
        return utils.create_response({'message': 'All processing completed'}, 201)
    else:
        return utils.create_response({'message': 'Processing has been appended to the queue'}, 201)

    

    