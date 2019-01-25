from flask import Flask, current_app, request, Response, json
from flask_login import current_user, login_user
from flask_restplus import Namespace, Resource
from ..database.db import User, get_user_by_username, add_user
from marshmallow import Schema, fields, ValidationError

api = Namespace('users', description='Operations related to users')


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(require=True)
    email = fields.Str(required=True)


user_schema = UserSchema()


@api.route('/')
@api.response(404, 'User not found')
@api.header('Access-Control-Allow-Origin')
class Users(Resource):
    def post(self):
        if not request.is_json:
            return Response(response={'Not valid json'},
                            headers={'Access-Control-Allow-Origin': '*'}, status=400)
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            response = "Required field missing:" + str(err.messages)
            return Response(response=response, status=400,
                            headers={'Access-Control-Allow-Origin': '*'}, mimetype='application/json')
        username = data['username']
        user = get_user_by_username(username)
        if user is None:
            user_to_add = add_user(data)
            js = json.dumps(user_to_add)
            resp = Response(js, status=201, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})
            return resp
        else:
            return Response(response={"User with username: '" + username + "' already exists"}, status=400)

@api.route('/login')
@api.header('Access-Control-Allow-Origin')
class UsersLogin(Resource):
    def post(self):
        if current_user.is_authenticated:
            return "redirect to home"
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        user = get_user_by_username(username)
        if not user or not user.check_password(password):
            return Response(response={'Invalid username or password'}, status=400)
        login_user(user)
        return 'Login successful'


@api.route('/<id>')
@api.doc(params={'id': 'A user ID'})
@api.response(404, 'User not found')
@api.header('Access-Control-Allow-Origin')
class User(Resource):

    def get(self):
        return ''




