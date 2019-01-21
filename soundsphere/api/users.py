from flask import Flask
from flask_restplus import Namespace, Resource

api = Namespace('users', description='Operations related to users in collection')


@api.route('/')
class Users(Resource):

    def get(self):
        return ''

    def put(self):
        return ''


@api.route('/<id>')
class User(Resource):

    def get(self):
        return ''




