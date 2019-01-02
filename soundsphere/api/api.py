from flask import app, jsonify, request, abort, make_response, Response, json
from soundsphere.db import get_albums_db
from flask_restful import Resource, reqparse, fields, marshal_with

# ALBUM TEST DATA
ALBUMS = get_albums_db()

# Argument Parser - Data validation
parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help="Album title")
parser.add_argument('artist', required=True, help="Artist of the album")
parser.add_argument('release', help="Release of the album")

# Resource fields - uses marshal with for data validation
resource_fields = {
    'title': fields.String,
    'artist': fields.String,
    # update below to be DateTime
    'release': fields.String,
    #'uri': fields.Url('album_id')
}


# def abort_if_album_doesnt_exist(album_id):
#     if album_id not in ALBUMS:
#         abort(404, message="Album {} doesn't exist")



class Landing(Resource):
    def get(self):
        return "Welcome to SoundSphere"


class Albums(Resource):
    def get(self):
        if ALBUMS is None:
            return abort(404, message="No albums exist in this collection")
        js = json.dumps(ALBUMS)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self):
        args = parser.parse_args()
        album_id = int(max(ALBUMS.keys()).lstrip('album')) + 1
        album_id = 'album%i' % album_id
        ALBUMS[album_id] = {'title': args['title'],
                            'artist': args['artist'],
                            'release': args['release'],
                            }
        js = json.dumps(ALBUMS[album_id])
        resp = Response(js, status=201, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


# Specifies a list of all albums
class Album(Resource):
    @marshal_with(resource_fields)
    def get(self, album_id):
        js = json.dumps(ALBUMS[album_id])
        resp = Response(js, status=201, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def delete(self, album_id):
        if ALBUMS[album_id] is None:
            return 204
        del ALBUMS[album_id]
        resp = Response('', status=201)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return '', 204

    @marshal_with(resource_fields)
    def put(self, album_id):
        args = parser.parse_args()
        album = {'title': args['title'],
                 'artist': args['artist'],
                 'release': args['release'],
                 }
        ALBUMS[album_id] = album
        js = json.dumps(album)
        resp = Response(js, status=201, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return album