import os
from slow_processing_times.utils import archive_exists
from flask import Flask

from slow_processing_times.entities.archive_info_entity import ArchiveInfo
from slow_processing_times.enums.state_enum import State

# Application Factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        ), 'uploads')
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'slow-processing-times.sqlite'),
        JOBS_LIMIT=2,
        UPLOAD_FOLDER=UPLOAD_FOLDER
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from .blueprints import crack
    app.register_blueprint(crack.bp)

    from .blueprints import archive
    app.register_blueprint(archive.bp)

    with app.app_context():
        for row in db.get_db().execute("SELECT * FROM cracked_password"):
            filename = row['filename']
            password = row['password']
            crack.archive_cracks[filename] = ArchiveInfo(state=State.CRACKED, is_cracked=True, password=password)

    return app