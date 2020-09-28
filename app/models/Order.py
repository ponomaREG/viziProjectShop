from app import db
from app.models.Cart import Cart
from app.models.Address import Address
from app.models.Product import Product
from utils import imageHelper
from utils import emailSender
from utils import addressBuilder


class Order:

    @staticmethod
    def getOrdersOfUser(userID):
        result = {}
        cursor = db.execute('select * from Заказ as ord inner join Адрес as addr where ord.address_id == addr.id and user_id = {};'.format(userID))
        allRows = cursor.fetchall()
        cursor.close()
        data = []
        if(len(allRows) == 0):
            result['status'] = 2
            result['message'] = 'Empty'
            result['data'] = []
            return result
        for row in allRows:
            data.append({'id':row[0],'date':row[2],
            'status':row[3],'total':row[4],'address':row[5]})
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = data
        return result

    @staticmethod
    def getDetailsOfOrder(orderID):
        result = {}
        cursor = db.execute("select pr.id,pr.imageLink,pr.title,bk.count,pr.cost_sale*bk.count as 'total' from Забронированная_книга as bk inner join Товар as pr on bk.order_id == {} and pr.id == bk.product_id;".format(orderID))
        data = []
        for row in cursor.fetchall():
            data.append({'id':row[0],'imageLink':imageHelper.makeFullPathToImage(row[1]),
            'title':row[2],'count':row[3],'total':row[4]})
        cursor.close()
        cursor = db.execute(
            'select ord.id,addr.*,ord.date,ord.status,ord.total from Заказ as ord  inner join Адрес as addr \
            where ord.address_id == addr.id and ord.id = {};'.format(orderID))
        address = cursor.fetchone()
        result['address'] = {'district':address[2],
                            'street':address[3],'flat':address[4],'floor':address[5],
                            'porch':address[6],'house':address[7],'address':addressBuilder.buildAddress(
                                address[2],address[3],address[4],address[5],
                                address[6],address[7]
                            )}
        result['info'] = {'orderID':address[0],'date':address[8],'status':address[9],
                            'total':address[10]}
        cursor.close()
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = data
        return result




    @staticmethod
    def addNewOrder(userID,district,flat,house,floor,street,porch='',email=''):
        result = {}
        try:
            cursor = db.execute('select pr.title,pr.cost_sale,cart.count,cart.count*pr.cost_sale,pr.id \
                as "Total" from Товар as pr \
                inner join Корзина as cart on pr.id == product_id \
                and user_id = {};'.format(userID))
            allRows = cursor.fetchall()
            if(len(allRows) == 0):
                result['status'] = 2
                result['message'] = 'Empty cart'
                result['data'] = []
                cursor.close()
                return result
        except:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            return result

        try:
            lastrowidAddress = Address.addNewAddress(district,house,floor,flat,porch,street)
        except:
                result['status'] = 3
                result['message'] = 'SQL runtime error'
                result['data'] = []
                cursor.close()
                return result 
        
        try:
            lastrowid = db.execute('insert into Заказ("user_id","status","total","address_id") values({},{},{},{});'.format(
                    userID,
                    0,
                    Cart.countTotalCostOfUser(userID),
                    lastrowidAddress)).lastrowid
            db.commit()
        except:
            result['status'] = 4
            result['message'] = 'SQL runtime error'
            result['data'] = []
            cursor.close()
            return result
        data = {'id':lastrowid,"data":Cart.getCartOfUser(userID)['data']}
        for row in allRows:
            try:
                db.execute('insert into Забронированная_книга \
                    values({},{},{})'.format(row[4],row[2],lastrowid))
                #db.commit()
                db.execute('delete from Корзина where \
                    user_id = {} and product_id = {};'.format(userID,row[4]))
                db.commit()
            except:
                result['status'] = 3
                result['message'] = 'SQL runtime error'
                result['data'] = []
                cursor.close()
                return result
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = data
        cursor.close()
        # if(email is not None):
        #     emailSender.EmailSender.sendEmailTo([email],orderDetails=result['data'])
        return result
        
