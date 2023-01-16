from flask import Flask
import sqlite3
from config import DB_NAME

from config import SECRET_KEY
app = Flask(__name__)



app.config['SECRET_KEY'] = SECRET_KEY

sqlite = sqlite3.connect(DB_NAME, check_same_thread=False)





from rfidapp import routes