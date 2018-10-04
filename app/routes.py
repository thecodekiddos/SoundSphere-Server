#!flask/bin/python
from app.utils.db import get_albums_db
from app import app
from flask import jsonify

@app.route('/')
def home():
    return 'Welcome to SoundSphere!'

@app.route('/api/albums', methods=['GET'])
def get_albums():
    return jsonify({'albums': get_albums_db()})

@app.route('/api/album/<int:album_id>', methods=['GET'])
def get_album_by_id(album_id):
    album = [album for album in albums if album['id'] == album_id]
    if len(album) == 0:
        abort(404)
    return jsonify({'album': album[0]})

@app.route('/api/albums/', methods=['POST'])
def add_album():
    if not request.json or not ('title' or 'artist') in request.json:
        abort(404)
    album = {
        'id': albums[-1]['id'] + 1,
        'title': request.json['title'],
        'artist': request.json['artist'],
        'release': request.json.get('release', "")

    }
    albums.append(album)
    return jsonify({'album': album}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    SoundSphere.run(debug=True)
