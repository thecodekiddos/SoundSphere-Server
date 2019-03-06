import os
from flask import Flask, redirect, url_for, flash, render_template
from flask_restplus import Api
from flask_login import logout_user, login_required


def create_app(debug=False, testing=False, create_db=False):
    # Create Flask App
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.debug = debug
    app.testing = testing

    # Create Database
    from soundsphere.database.db import db, migrate, login
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)

    if create_db:
        with app.app_context():
            db.create_all()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create Routes
    from .api.albums import api as album_api
    from .api.users import api as user_api
    # from .api.discogs import api as discogs_api
    api = Api(app, version='1.0.0', title='SoundSphere', description='A collection of shared records.')
    api.add_namespace(album_api)
    api.add_namespace(user_api)
    # api.add_namespace(discogs_api)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have logged out")
        return redirect(url_for("index"))

    @app.route("/home")
    def index():
        return render_template("home.html")

    return app
