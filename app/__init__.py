from flask import Flask
from config import BaseConfig
import sqlite3

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = sqlite3.connect(app.config.get('DB_SHOP'),check_same_thread=False)

from app import views