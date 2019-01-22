from flask import abort, Response, json, request
from flask_restplus import Resource, reqparse, Namespace
from marshmallow import ValidationError, Schema, fields
from ..database.db import get_album, add_album, get_all_albums, update_album, delete_album, get_album_by_title
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


def must_be_defined(data):
    if not data:
        raise ValidationError('No data provided.')


# Resource fields - uses marshal with for data validation
class AlbumSchema(Schema):
    title = fields.Str(required=True, error_messages={"required": "Title is required"}, validate=must_be_defined)
    artist = fields.Str(required=True, error_messages={"required": "Artist is required"}, validate=must_be_defined)
    year = fields.Integer()
    barcode = fields.Str()
    catno = fields.Str(required=True, error_messages={"required": "Catalogue number is required"},
                       validate=must_be_defined)
    notes = fields.Str()


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)


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
                404: 'Resource not found',
                500: 'Internal Server Error'
             })
    def get(self):
        albums = get_all_albums()
        if albums is None:
            return abort(404, message="No albums exist in this collection")
        js = json.dumps(albums)
        resp = Response(js, status=200, headers={'Access-Control-Allow-Origin': '*'})
        return resp

    @api.doc('post_albums',
             resonses={
                 200: 'Success',
                 400: 'Bad Request',
                 500: 'Internal Server Error'
             })
    def post(self):
        if not request.is_json:
            return Response(response={'Not valid json'}, status=400)
        json_data = request.get_json()
        if not json_data:
            return Response(response={'Missing valid data'}, status=400,
                            headers={'Access-Control-Allow-Origin': '*'}, mimetype='application/json')
        try:
            data = album_schema.load(json_data)
        except ValidationError as err:
            response = "Required field missing:" + str(err.messages)
            return Response(response=response, status=400,
                            headers={'Access-Control-Allow-Origin': '*'}, mimetype='application/json')
        title = data['title']
        album = get_album_by_title(title)
        if album is None:
            album_to_add = add_album(data)
            js = json.dumps(album_to_add)
            resp = Response(js, status=201, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})
            return resp
        else:
            return Response(response={"Album with title: '" + title + "' already exists"}, status=400)


# Specifies a list of all albums
@api.route('/<id>')
@api.doc(params={'id': 'An album ID'})
@api.response(404, 'Album not found')
@api.header('Access-Control-Allow-Origin')
class Album(Resource):
    @api.doc('get_album_by_id',
             responses={
                 201: 'Success'
             })
    def get(self, id):
        abort_if_album_doesnt_exist(id)
        album_from_db = get_album(id)
        author_result = album_schema.dumps(album_from_db)
        resp = Response(author_result, status=201, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})
        return resp

    @api.doc('delete_album_by_id',
             responses={
                 204: "Success"
             })
    def delete(self, id):
        delete_album(id)
        return '', 204

    @api.doc('put_album_by_id',
             responses={
                 201: "Success"
             })
    # @api.marshal_with(album)
    def put(self, id):
        args = parser.parse_args()
        update = copy.copy(args)
        for k, v in args.items():
            if v is None:
                del update[k]
        album_to_update = update_album(update, id)
        js = json.dumps(album_to_update)
        resp = Response(js, status=201, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})
        return resp
