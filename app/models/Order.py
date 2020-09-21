from app import db
from app.models.Cart import Cart
from app.models.Address import Address


class Order:
    #TODO  ADDRESSES!!!!!!!




    @staticmethod
    def addNewOrder(userID,district,flat,porch='',house,floor,street):
        result = {}
        cursor = db.execute('select * from Покупатель where id = {};'.format(userID))
        user = cursor.fetchone()
        if(user[3] is None):
            result['status'] = 10
            result['message'] = 'Empty address'
            cursor.close()
            return result
        cursor.close()
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
                    Cart.countTotalCostOfUser(userID)),
                    lastrowidAddress).lastrowid
            db.commit()
        except:
            result['status'] = 4
            result['message'] = 'SQL runtime error'
            result['data'] = []
            cursor.close()
            return result
        
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
        result['data'] = []
        cursor.close()
        return result
        