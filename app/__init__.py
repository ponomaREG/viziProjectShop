from flask import Flask
from config import BaseConfig
from flask_login import LoginManager
import sqlite3


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = sqlite3.connect(app.config.get('DB_SHOP'),check_same_thread=False)
login_manager = LoginManager()
login_manager.init_app(app)
from app import views,API