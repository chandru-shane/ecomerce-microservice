from flask import Flask 
import os
from .config import DevelopmentConfig
from .extensions import api, db, jwt, migrate
from .resources import ns
from datetime import timedelta

def create_app():

    app = Flask(__name__)

    app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your secret key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set access token expiration time
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api.add_namespace(ns)
    return app