from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, DB_NAME
# from app.modelsdels import User, AuthorizedUsers, UserLogs


db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

from app import routes

# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)

# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)