#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

albums_list = list

def init_app(app):
    db.init_app(app)


def from_sql(row):
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# Shared helper table for user to albums
collection = db.Table('collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True)
)


class Album(db.Model):
    '''
    This class defines how albums will be stored in the SQLite DB
    '''
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(80))
    catno = db.Column(db.String(80), nullable=False, unique=True)
    notes = db.Column(db.Text)
    user = db.relationship("User", secondary=collection, backref=db.backref("albums"))


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


def get_album(id):
    result = Album.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    album = Album(**data)
    db.session.add(album)
    db.session.commit()
    return from_sql(album)


def get_all_albums():
    query = (Album.query.order_by(Album.title))
    albums = albums_list(map(from_sql, query.all()))
    return albums


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
