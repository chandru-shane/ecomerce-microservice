from flask_sqlalchemy import SQLAlchemy 
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(get_remote_address, default_limits=["20 per second"],)
