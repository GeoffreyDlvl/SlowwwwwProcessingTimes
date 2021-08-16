import os, hashlib
from flask import (
    current_app, jsonify, request, Response
)

def archive_exists(filename):
    return filename in os.listdir(current_app.config['UPLOAD_FOLDER'])

def create_response(json_body, status_code):
    resp = jsonify(json_body)
    resp.status_code = status_code
    return resp

def compute_checksum(filename):
    hash_md5 = hashlib.md5()
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_filename_in(request):
    if not request.is_json:
        return create_response({'message': 'Error: mimetype is not application/json'}, 400)

    data = request.get_json()
    try:
        data['filename']
        return Response()
    except KeyError:
        return create_response({'message': 'Key is not recognized. Use \'filename\''}, 400)

def is_response_empty(response):
    return response.content_length is None

def get_filename_from(request):
    return request.get_json()['filename']