from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, DB_NAME


db = SQLAlchemy()
app = Flask(__name__)

# sqlite = sqlite3.connect(DB_NAME, check_same_thread=False)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
# def create_app():
#     app = Flask(__name__)

#     app.config['SECRET_KEY'] = '12345'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

#     db.init_app(app)

#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app


