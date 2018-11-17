import os

from flask import Flask, jsonify, make_response

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    #db setup
    from . import db
    db.init_app(app)

    #authentication bp
    from . import auth
    app.register_blueprint(auth.bp)

    #album bp
    # from . import albums
    # app.register_blueprint(api.bp)
    # app.add_url_rule('/', endpoint='index')

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

    #API routes
    @app.route('/')
    def home():
        return 'Welcome to SoundSphere!'

    return app
    
