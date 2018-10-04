#!flask/bin/python
from app import app

albums = [
    {
        'id': 1,
        'title': u'Kind of Blue',
        'artist': u'Miles Davis',
        'release': 1958
    },
    {
        'id': 2,
        'title': u'Voodoo',
        'artist': u'D\'Angelo',
        'release': 1999
    }
]

def get_albums_db():
    return albums
