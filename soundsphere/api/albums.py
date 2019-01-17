from flask import abort, Response, json, request, jsonify
from flask_restplus import Resource, reqparse, fields, Namespace, marshal
from ..database.db import Album, db, get_album, create, get_all_albums

api = Namespace('albums', description='Operations related to albums in collection')


# Argument Parser - Data validation
parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help="Album title")
parser.add_argument('artist', required=True, help="Artist of the album")
parser.add_argument('release', help="Release of the album")

# Resource fields - uses marshal with for data validation
album = api.model('Albums', {
    'title': fields.String,
    'artist': fields.String,
    # update below to be DateTime
    'release': fields.String
})


# Error handling
def abort_if_album_doesnt_exist(id):
    if album not in get_album(id):
        api.abort(404, message="Album " + id + " doesn't exist")


@api.route('/')
@api.response(404, 'Albums not found')
@api.header('Access-Control-Allow-Origin')
class Albums(Resource):
    @api.doc('get_albums',
             responses={
                200: 'Success',
                500: 'Internal Server Error'
             })
    def get(self):
        albums = get_all_albums()
        if albums is None:
            return abort(404, message="No albums exist in this collection")
        js = json.dumps(albums)
        resp = Response(js, status=200)
        return resp

    @api.doc('post_albums')
    def post(self):
        data = request.form.to_dict(flat=True)
        album_to_add = create(data)
        js = json.dumps(album_to_add)
        resp = Response(js, status=201, mimetype='application/json')
        return resp


# Specifies a list of all albums
@api.route('/<id>')
@api.param('id', 'album identifier')
@api.response(404, 'Album not found')
@api.header('Access-Control-Allow-Origin')
class Album(Resource):
    @api.doc('get_album_by_id')
    def get(self, id):
        album_from_db = get_album(id)
        js = json.dumps(album_from_db)
        resp = Response(js, status=201, mimetype='application/json')
        return resp

    @api.doc('delete_album_by_id')
    def delete(self, album_id):
        if ALBUMS[album_id] is None:
            return 204
        del ALBUMS[album_id]
        return '', 204

    @api.doc('put_album_by_id')
    @api.marshal_with(album)
    def put(self, album_id):
        abort_if_album_doesnt_exist(album_id)
        args = parser.parse_args()
        album_updated = {'title': args['title'],
                         'artist': args['artist'],
                         'release': args['release'],
                        }
        ALBUMS[album_id] = album_updated
        js = json.dumps(album_updated)
        resp = Response(js, status=201, mimetype='application/json')
        return resp
