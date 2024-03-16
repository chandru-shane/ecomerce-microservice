from flask_restx import fields
from flask_restx import reqparse
from .extensions import api


user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Token model for response
token_model = api.model('Token', {
    'access_token': fields.String(description='Access Token'),
    'refresh_token': fields.String(description='Refresh Token')
})


user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# User model for response
user_response_model = api.model('UserResponse', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username')
})

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('password', type=str, required=True, help='Password')
