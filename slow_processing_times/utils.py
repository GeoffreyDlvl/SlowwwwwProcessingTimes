import os
from flask import current_app, jsonify

def archive_exists(filename):
    return filename in os.listdir(current_app.config['UPLOAD_FOLDER'])

def createResponse(json_body, status_code):
    resp = jsonify(json_body)
    resp.status_code = status_code
    return resp