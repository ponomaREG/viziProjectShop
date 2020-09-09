from app import db
from utils import md5helper, sqlQueryHelper, dateHelper
from app import login_manager
from flask_login import UserMixin
from app.models.User import *



@login_manager.user_loader
def load_user(userID):
    cursor = db.execute('select * from Покупатель where id = {};'.format(userID))
    allRows = cursor.fetchall()
    if(len(allRows) == 0):
        return None
    row = allRows[0]
    return User(row[0],row[4],row[6])
