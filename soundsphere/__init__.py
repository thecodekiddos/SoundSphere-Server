import os

from flask import Flask
from flask_restplus import Api
from .api.albums import api as album_api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app, version='1.0.0', title='SoundSphere', description='A collection of shared records.')
    api.add_namespace(album_api)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    # db setup
    # from . import db
    # db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
