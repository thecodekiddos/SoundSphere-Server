import os

dirname = os.path.dirname(__file__)
db_filename = os.path.join(dirname, 'test_db.db')


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'HV\xb7\xe1\x9f3/\x9c\xa3\xc2TY\xe7\x1b\x10\xd55\x1a\x8aL\x92*\x9a\xb2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_filename
    DISCOGS_KEY = os.environ['DISCOGS_KEY']
    DISCOGS_SECRET = os.environ['DISCOGS_SECRET']


class Development(BaseConfig):
    DEBUG = True
    ENV = 'development'
    FLASK_ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class Production(BaseConfig):
    DEBUG = False
    ENV = 'production'
    FLASK_ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

