from app import db
from utils import md5helper




class User:
    
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
        