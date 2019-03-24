import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from rest_api.security import authenticate, identity
from rest_api.resources.user import UserRegister, UserDelete
from rest_api.resources.item import Item, ItemList
from rest_api.resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'mys3cr3tk3y'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['JWT_AUTH_URL_RULE'] = '/login'
# JWT will expire after half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /login endpoint


@jwt.auth_response_handler
def custom_auth_reponse_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def custom_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserDelete, '/remove/<string:username>')

