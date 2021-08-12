import os
from flask import Flask

from slow_processing_times.entities.archive_info_entity import ArchiveInfo
from slow_processing_times.enums.state_enum import State

from . import db
from .blueprints import crack
from .blueprints import archive

def load_archives_dict(app):
    for row in db.get_db().execute("SELECT * FROM cracked_password"):
        filename = row['filename']
        password = row['password']
        crack.archives[filename] = ArchiveInfo(state=State.CRACKED, is_cracked=True, password=password)
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename not in crack.archives:
            crack.archives[filename] = ArchiveInfo(state=State.UPLOADED)

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

    db.init_app(app)

    app.register_blueprint(crack.bp)

    app.register_blueprint(archive.bp)

    with app.app_context():
        load_archives_dict(app)

    return app