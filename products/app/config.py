import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    host = os.environ.get("DB_HOST", "postgres_db")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}/flask_products"
    
    orders_api = f"http://{os.environ.get('USERS_SERVICE', 'users')}/api/"
    LOGFILE = "log.log"
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'


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
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    host = os.environ.get("DB_HOST", "localhost:5432")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}/flask_orders"