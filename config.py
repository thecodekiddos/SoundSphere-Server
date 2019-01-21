import os

dirname = os.path.dirname(__file__)
db_filename = os.path.join(dirname, 'test_db.db')

if(os.environ.get('APP_SETTINGS') == 'dev'):
    DEBUG = True
    ENV = 'development'
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_filename
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
else:
    DEBUG = False
    ENV = 'production'
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_filename
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


