from datetime import timedelta
from flask import Flask 
from prometheus_flask_exporter import PrometheusMetrics

import os
from loguru import logger
from .config import DevelopmentConfig, TestingConfig
from .extensions import api, db, migrate
from .resources import ns

def create_app(testing=False):

    app = Flask(__name__)
    if not testing:
        app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
    else:
        app.config.from_object(os.environ.get('APP_SETTINGS', TestingConfig))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    metrics = PrometheusMetrics(app)
    logger.add("logs/product.log", backtrace=True, level="DEBUG")

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    return app