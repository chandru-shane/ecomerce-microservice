from flask_sqlalchemy import SQLAlchemy 
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
