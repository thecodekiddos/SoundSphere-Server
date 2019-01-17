from flask import abort, Response, json, request
from flask_restplus import Resource, reqparse, fields, Namespace, marshal
from ..database.db import Album, db, get_album, add_album, get_all_albums, update_album, delete_album
import copy

api = Namespace('albums', description='Operations related to albums in collection')


# Argument Parser - Data validation
parser = reqparse.RequestParser()
parser.add_argument('title', help="Album title")
parser.add_argument('artist', help="Artist of the album")
parser.add_argument('year', help="Release of the album")
parser.add_argument('barcode', help="Release of the album")
parser.add_argument('catno', help="Release of the album")
parser.add_argument('notes', help="Release of the album")

# Resource fields - uses marshal with for data validation
# album = api.model('Albums', {
#     'title': fields.String,
#     'artist': fields.String,
#     # update below to be DateTime
#     'release': fields.String
# })


# Error handling
def abort_if_album_doesnt_exist(id):
    if get_album(id) is None:
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
        album_to_add = add_album(data)
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
    def delete(self, id):
        delete_album(id)
        return '', 204

    @api.doc('put_album_by_id')
    # @api.marshal_with(album)
    def put(self, id):
        args = parser.parse_args()
        update = copy.copy(args)
        for k, v in args.items():
            if v is None:
                del update[k]
        album_to_update = update_album(update, id)
        js = json.dumps(album_to_update)
        resp = Response(js, status=201, mimetype='application/json')
        return resp
