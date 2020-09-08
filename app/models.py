from app import db
from utils import md5helper, sqlQueryHelper
from app import login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(userID):
    cursor = db.execute('select * from Покупатель where id = {};'.format(userID))
    allRows = cursor.fetchall()
    if(len(allRows) == 0):
        return None
    row = allRows[0]
    return User(row[0],row[4],row[6])

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
    

class Product:

    @staticmethod
    def __prepareProducts(cursor):
        allRows = cursor.fetchall()
        result = {}
        if(len(allRows) == 0):
            result['status'] = 2
            result['message'] = "Empty data"
            result['data'] = []
            cursor.close()
            return result
        result['data'] = []
        for rw in allRows:
            rowDict = {
                'title':rw[1],'desc':rw[2],
                'rate':rw[7],'cost':rw[4],
                'quantity':rw[5],'tags':rw[6]
                }
            result['data'].append(rowDict)
        result['status'] = 0
        result['count'] = len(allRows)
        result['message'] = "OK"
        cursor.close()
        return result

    @staticmethod
    def getAllProfuctsFilteredByRate(page):
        result = {}
        try:
            cursor = db.execute('select * from Товар order by rate DESC LIMIT 5 OFFSET {};'.format(5*page))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            cursor.close()
            return result
        return Product.__prepareProducts(cursor)

    @staticmethod
    def getAllProductsFilteredByTags(tags):
        result = {}
        try:
            cursor = db.execute(sqlQueryHelper.buildSqlQueryByTags('select * from Товар',tags))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        return Product.__prepareProducts(cursor)


class Cart:


    @staticmethod
    def getCartOfUser(userID):
        result = {}
        try:
            cursor = db.execute(
                'select pr.title,pr.cost_sale,cart.count,cart.count*pr.cost_sale \
                as "Total" from Товар as pr \
                inner join Корзина as cart on pr.id == product_id \
                and user_id = {};'.format(userID))
            allRows = cursor.fetchall()
        except:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            cursor.close()
            return result
        if(len(allRows) == 0):
            result['status'] = 2
            result['message'] = 'Empty cart'
            result['data'] = []
            cursor.close()
            return result
        result['data'] = []
        result['count'] = len(allRows)
        for row in allRows:
            result['data'].append(
                {
                    'total':row[3],'count':row[2],
                    'cost':row[1],'title':row[0]
                }
            )
        result['status'] = 0
        result['message'] = 'OK'
        return result

# class Cart:
#     pass

        