from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from soundsphere.db import get_db

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    db = get_db()
    albums = db.execute('SELECT p.id, title, body, created, album_id, username'
        ' FROM post p JOIN user u ON p.album_id = u.id'
        ' ORDER BY created DESC'
    ).fetchal()
    return albums

''' @bp.route('/albums', methods=['GET'])
def get_albums():
    return jsonify({'albums': get_albums_db()})

@bp.route('/album/<int:album_id>', methods=['GET'])
def get_album_by_id(album_id):
    album = [album for album in albums if album['id'] == album_id]
    if len(album) == 0:
        abort(404)
    return jsonify({'album': album[0]})

@bp.route('/albums/', methods=['POST'])
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

@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
     '''