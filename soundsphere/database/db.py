#!flask/bin/python
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

login.login_view = 'discogs.login'

albums_list = list


def init_app(app):
    db.init_app(app)


def from_sql(row):
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


'''
Models/Tables
'''
# Shared helper table for user to albums
collection = db.Table('collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True)
)


class Album(db.Model):
    '''
    This class defines how albums will be stored in the SQLite3 DB
    '''
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    barcode = db.Column(db.String(80))
    catno = db.Column(db.String(80), nullable=False, unique=True)
    notes = db.Column(db.Text)
    user = db.relationship("User", secondary=collection, backref=db.backref("albums"))


class User(UserMixin, db.Model):
    '''
    Defines the user class
    '''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# class OAuth(OAuthConsumerMixin, db.Model):
#     provider_user_id = db.Column(db.String(256), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id))
#     user = db.relationship(User)
#


'''
Album Query Methods
'''


def get_all_albums():
    query = (Album.query.order_by(Album.title))
    albums = albums_list(map(from_sql, query.all()))
    return albums


def get_album(id):
    result = Album.query.get(id)
    if not result:
        return None
    return from_sql(result)


def get_album_by_title(title):
    result = Album.query.filter_by(title=title).first()
    if not result:
        return None
    return from_sql(result)


def add_album(data):
    album = Album(**data)
    try:
        db.session.add(album)
        db.session.commit()
        return from_sql(album)
    except IntegrityError as err:
        return err


def delete_album(id):
    Album.query.filter_by(id=id).delete()
    db.session.commit()


def update_album(data, id):
    album = Album.query.get(id)
    for k, v in data.items():
        setattr(album, k, v)
    db.session.commit()
    return from_sql(album)


'''
User Query Methods
'''


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_user_by_username(username):
    result = User.query.filter_by(username=username).first()
    if result is None:
        return None
    return result


def add_user(data):
    user = User(username=data['username'], email=data['email'])
    try:
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return from_sql(user)
    except IntegrityError as err:
        return err
'''
Build database as a single script
'''


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")

def _drop_database():
    """
    If this script is run directly, drop all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    init_app(app)
    with app.app_context():
        db.drop_all()
    print("All tables dropped")



#
# if __name__ == '__main__':
#     _create_database()
