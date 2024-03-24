from flask import Flask ,request
import os
from prometheus_flask_exporter import PrometheusMetrics
from loguru import logger
from .config import DevelopmentConfig, TestingConfig
from .extensions import api, db, jwt, migrate, limiter
from .resources import ns
from datetime import timedelta

def create_app(testing=False):

    app = Flask(__name__)

    if not testing:
        app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
    else:
        # this will be applied for testing config
        app.config.from_object(os.environ.get('APP_SETTINGS', TestingConfig))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your secret key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set access token expiration time
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    metrics = PrometheusMetrics(app)
    logger.add("logs/users.log", backtrace=True, level="DEBUG")
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    api.add_namespace(ns)

    
    with app.app_context():
        db.create_all()
    
    return app