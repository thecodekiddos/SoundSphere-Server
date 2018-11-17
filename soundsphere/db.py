#!flask/bin/python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key = True)
    title = Column(String)
    artist = Column(String)

    def __repr__(self):
        return "<Album( title='%s', artist='%s')"


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
