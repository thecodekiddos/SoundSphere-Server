import os
import logging

from flask import Flask
from flask_restplus import Api


def create_app():
    # Create Flask App
    app = Flask(__name__, instance_relative_config=True)

    # Set up app config
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)

    # Create Database
    from soundsphere.database.db import db
    with app.app_context():
        db.init_app(app)

    # Create Routes
    from .api.albums import api as album_api
    api = Api(app, version='1.0.0', title='SoundSphere', description='A collection of shared records.')
    api.add_namespace(album_api)

    return app
