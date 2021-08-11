from flask import (
    Blueprint, g, request, jsonify
)

from slow_processing_times.db import get_db

bp = Blueprint('crack_archive', __name__, url_prefix='/crack')