from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, DB_NAME

db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

from app import routes
