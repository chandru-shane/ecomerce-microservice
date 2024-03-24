from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest
import os
from .config import DevelopmentConfig, TestingConfig
from .extensions import api, db, migrate
from .resources import ns
from datetime import timedelta
from loguru import logger

def create_app(testing=False):
    app = Flask(__name__)
    
    if not testing:
        app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
    else:
        app.config.from_object(os.environ.get('APP_SETTINGS', TestingConfig))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize Prometheus metrics
    # metrics = PrometheusMetrics(app)
    @app.route('/metrics')
    def metrics():
        return generate_latest()
    

    logger.add("logs/product.log", backtrace=True, level="DEBUG")
    
    api.init_app(app)
    db.init_app(app)
    api.add_namespace(ns)
    migrate.init_app(app, db)

    @app.before_request
    def log_request_info():
        logger.info(
            f"Request: {request.method} {request.url} | IP: {request.remote_addr} | Data: {request.data}"
        )
        
    @app.after_request
    def log_response_info(response):
        logger.info(
            f"Response: {response.status_code}"
        )
        return response

    with app.app_context():
        db.create_all()

    return app

