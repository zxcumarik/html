from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
from .routes import initialize_routes
api = Api(app)
initialize_routes(api)

