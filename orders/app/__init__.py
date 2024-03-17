from flask import Flask 
import os
from .config import DevelopmentConfig
from .extensions import api, db, migrate
from .resources import ns

def create_app():

    app = Flask(__name__)

    app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api.init_app(app)
    db.init_app(app)
    
    migrate.init_app(app, db)
    api.add_namespace(ns)

    return app