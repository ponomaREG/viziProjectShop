from app import db
from utils import md5helper, sqlQueryHelper, dateHelper
from app import login_manager
from flask_login import UserMixin
from app.models.User import *



@login_manager.user_loader
def load_user(userID):
    row = SqlExecuter.getOneRowsPacked('select * from Покупатель where id = {};'.format(userID))
    if(row is None):
        return None
    user = User(userID = row['id'],email = row['email'],
    password_hash = row['password_hash'],last_name=row['last_name'],
    first_name =row['first_name'] ,birthdate = row['birthdate'])
    if(checkIfUserAdmin(userID)):
        user.set_admin(True)
    return user



def checkIfUserAdmin(userID):
    return SqlExecuter.getOneRowsPacked('select * from Админ where user_id = {};'.format(userID)) is not None
