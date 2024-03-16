import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    user = os.environ.get("user", "postgres")
    password = os.environ.get("password", "")
    host = os.environ.get("host", "")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}/flask_products"
    user_api = "http://127.0.0.1:8000/api/"
    orders_api = "http://127.0.0.1:8088/api/"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True