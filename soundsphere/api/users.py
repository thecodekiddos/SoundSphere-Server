from flask import Flask, current_app, request, Response, json, session, url_for, flash, redirect
from flask_restplus import Namespace, Resource
from flask_login import current_user, login_user, login_required, logout_user
from ..database.db import User, get_user_by_username, add_user, db, login
from marshmallow import Schema, fields, ValidationError


api = Namespace('users', description='Operations related to users')


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(require=True)
    password2 = fields.Str(required=True)


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
        password = data['password']
        password2 = data['password2']
        if password != password2:
            return Response(response="Passwords don't match", status=400,
                            headers={'Access-Control-Allow-Origin': '*'})
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
            return url_for("/")
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        user = get_user_by_username(username)
        if not user or not user.check_password(password):
            return Response(response={'Invalid username or password'}, status=400, headers={'Access-Control-Allow-Origin': '*'})
        login_user(user)
        return Response('Login successful', status=204, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})


@api.route('/logout')
@api.header('Access-Control-Allow-Origin')
# @login_required
class UsersLogout(Resource):
    def post(self):
        logout_user()
        return Response('Logout successful', status=204, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})


@api.route('/<id>')
@api.doc(params={'id': 'A user ID'})
@api.response(404, 'User not found')
@api.header('Access-Control-Allow-Origin')
class User(Resource):
    def get(self):
        return ''

#
# @api.route('/login')
# def login():
#     return discogs.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))
#

# @api.route('/oauth-authorized')
# @discogs.authorized_handler
# def oauth_authorized(resp):
#     next_url = request.args.get('next') or url_for('index')
#     if resp is None:
#         flash(u'You denied the request to sign in.')
#         return redirect(next_url)
#
#     session['discogs_token'] = (
#         resp['oauth_token'],
#         resp['oauth_token_secret']
#     )
#     session['discogs_user'] = resp['user_name']
#
#     flash('You were signed in as %s' % resp['user_name'])
#     return redirect(next_url)
