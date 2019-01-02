import os

from flask import Flask
from flask_restful import Api
#Gross change this
from .api.api import Landing, Albums, Album


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    # db setup
    # from . import db
    # db.init_app(app)

    # setup REST_api
    api.add_resource(Landing, '/')
    api.add_resource(Albums, '/api/albums', endpoint="albums")
    api.add_resource(Album, '/api/album/<string:album_id>', endpoint='album_id')

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
