from flask_login import UserMixin
from app import db
from utils import md5helper


class User(UserMixin):
    userID = -1
    email = None
    password_hash = None

    def __init__(self,userID,email,password_hash):
        self.userID = userID
        self.email = email
        self.password_hash = password_hash
    

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.userID)


    @staticmethod
    def registerUser(email,password,last_name,first_name,birthdate):
        result = {}
        cursor = db.execute('select * from Покупатель where email="{}";'.format(email))
        if(cursor.fetchone() is not None):
            result['status'] = 1
            result['message'] = 'User with same email already exists'
            cursor.close()
            return result
        cursor.close()
        cursor = db.execute(
            'insert into Покупатель("email","last_name","first_name","birthdate","password_hash") \
                values("{}","{}","{}","{}","{}")'.format(
                    email,last_name,first_name,birthdate,md5helper.ecnrypt(password))
                )
        db.commit()
        result["status"] = 0
        result["message"] = "OK"
        result["userID"] = cursor.lastrowid
        cursor.close()
        return result
        
    
    @staticmethod
    def getInfo(value,column='id'):
        cursor = db.execute('select * from Покупатель where {} = {};'.format(column,value))
        result = {}
        allRows = cursor.fetchall()
        if(len(allRows) == 0):
            result['data'] = {}
            result['status'] = 1
            result['message'] = 'User not found'
            return result
        row = allRows[0]
        result['data'] = {
            'id':row[0],'last_name':row[1],
            'first_name':row[2],'address':row[3],
            'email':row[4],'birthdate':row[5],
            'password_hash':row[6]}
        result['status'] = 0
        result['message'] = 'OK'
        cursor.close()
        return result

    @staticmethod
    def addUser(data):
        result = {}
        try:
            last_name = data['last_name']
            first_name = data['first_name']
            password = data['password']
            birthdate = data['birthdate']
            email = data['email']
        except KeyError:
            result['status'] = 1
            result['message'] = 'Required field is missing'
            return result
        try:
            db.execute(
                'insert into shop values("{}","{}",NULL,"{}","{}","{}");'.format(
                    last_name,first_name,
                    email,birthdate,
                    md5helper.ecnrypt(password)
                )
            )
            db.commit()
        except Exception:
            result['status'] = 2
            result['message'] = 'SQL runtime error'
            return result
        result['status'] = 0
        result['message'] = 'OK'
        return result
    
    @staticmethod
    def validateUser(email,password):
        cursor = db.execute(
            'select * from Покупатель where email \
             = "{}" and password_hash = "{}"'.format(email,md5helper.ecnrypt(password))
            )
        allRows = cursor.fetchall()
        if(len(allRows) == 0):
            return False
        else:
            return True

    @staticmethod
    def validateUserAndReturnUserID(email,password):
        cursor = db.execute(
            'select * from Покупатель where email \
             = "{}" and password_hash = "{}"'.format(email,md5helper.ecnrypt(password))
            )
        allRows = cursor.fetchall()
        if(len(allRows) == 0):
            return -1
        else:
            return allRows[0][0]