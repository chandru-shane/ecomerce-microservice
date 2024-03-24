from flask_restx import Namespace, Resource
from .models import User
from .extensions import db, limiter
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .api_models import user_model, token_model, update_user_parser, user_response_model
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort
ns = Namespace("api")


# Login route to generate access and refresh tokens
@ns.route('/login')
class Login(Resource):
    @ns.expect(user_model)
    @ns.response(200, 'Success', token_model)
    def post(self):
        data = ns.payload
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'message': 'Invalid username or password'}, 401

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200



@ns.route('/me')
class Protected(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            # Query the User model by username
            user = User.query.filter_by(username=current_user).first()
            return user.as_dict(),  200
           
        except Exception as e:
            abort(401, {'message': 'Unauthorized. Please provide a valid access token or something went worng'})

@ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200


@ns.route('/user')
class CreateUser(Resource):
    @ns.expect(user_model)
    @ns.response(201, 'User created successfully', user_response_model)
    def post(self):
        data = ns.payload
        username = data.get('username')
        password = data.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'User already exists'}, 409

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return new_user.as_dict(), 201
from loguru import logger
# Update user endpoint password
@ns.route('/user_update')
class UpdateUser(Resource):
    @jwt_required()
    @ns.expect(update_user_parser)
    @ns.response(200, 'User updated successfully', user_response_model)
    def put(self):
        data = update_user_parser.parse_args()
        password = data.get('password')
        user = get_jwt_identity()            
        user = User.query.get(username=user)
        logger.debug(f"{user}, {type(user)}")
        logger.debug("*"*100)
        user.password = generate_password_hash(password)
        db.session.commit()

        return user.as_dict(), 200