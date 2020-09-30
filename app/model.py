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
    user = User(userID = row[0],email = row[4],
    password_hash = row[6],last_name=row[1],
    first_name =row[2] ,birthdate = row[5])
    if(checkIfUserAdmin(userID)):
        user.set_admin(True)
    return user



def checkIfUserAdmin(userID):
    cursor = db.execute('select * from Админ where user_id == {};'.format(userID))
    user = cursor.fetchone()
    return user is not None
