import os
from flask import Flask

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

    return app