from app import db

class Cart:


    @staticmethod
    def countTotalCostOfUser(userID):
        cursor = db.execute('select pr.cost_sale,cart.count,cart.count*pr.cost_sale,pr.id \
                as "Total" from Товар as pr \
                inner join Корзина as cart on pr.id == product_id \
                and user_id = {};'.format(userID))
        allRows = cursor.fetchall()
        total = 0.0
        for row in allRows:
            total += row[2]
        cursor.close()
        return total

    @staticmethod
    def removeItemInCartOfUser(userID,productID):
        result = {}
        try:
            cursor = db.execute(
                'select * from Корзина where product_id = {} and user_id = {};'.format(productID,userID)
            )
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            return result
        allRows = cursor.fetchall()
        if(len(allRows)>0):
            if(allRows[0][2]>1):
                try:
                    db.execute('update Корзина set count = count - 1 where \
                    product_id = {} and user_id = {};'.format(productID,userID))
                    db.commit()
                    cursor.close()
                except:
                    result['status'] = 2
                    result['message'] = 'SQL Runtime error'
                    return result
                result['status'] = 0
                result['message'] = 'OK'
                return result
            try:
                db.execute('delete from Корзина where \
                    product_id = {} and user_id = {};'.format(productID,userID))
                db.commit()
                cursor.close()
            except:
                result['status'] = 3
                result['message'] = 'SQL Runtime error'
                return result
            result['status'] = 0
            result['message'] = 'OK'
            return result
        result['status'] = 4
        result['message'] = 'Not found item'
        return result


    @staticmethod
    def addItemInCartOfUser(userID,productID):
        result = {}
        
        cursor = db.execute(
            'select * from Товар where id = {};'.format(productID)
        )
        row = cursor.fetchone()
        if(row is None):
            result['status'] = 7
            result['message'] = 'No such product'
            return result
        if(row[5] == 0):
            result['status'] = 8
            result['message'] = 'Zero quantity of called product'
            return result
        quantityOfProduct = row[5]
        try:
            cursor = db.execute(
                'select * from Корзина where product_id = {} and user_id = {};'.format(productID,userID)
            )
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            return result
        row = cursor.fetchone()
        if(row is not None):
            if(row[2] >= quantityOfProduct):
                result['status'] = 6
                result['message'] = 'Not enough products'
                return result
            try:
                db.execute(
                    'update Корзина set count = count + 1 \
                    where product_id = {} and user_id = {}'.format(productID,userID))
                db.commit()
                cursor.close()
            except:
                result['status'] = 2
                result['message'] = 'SQL Runtime error'
                return result
            result['status'] = 0
            result['message'] = 'Inc count'
            return result
        try:
            db.execute('insert into Корзина values({},{},1)'.format(userID,productID))
            db.commit()
            cursor.close()
        except:
            result['status'] = 3
            result['message'] = 'SQL Runtime error'
            return result
        result['status'] = 0
        result['message'] = 'Add new values'
        return result
        


    @staticmethod
    def getCartOfUser(userID):
        result = {}
        try:
            cursor = db.execute(
                'select pr.title,pr.cost_sale,cart.count,cart.count*pr.cost_sale,pr.id \
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
        totalCost = 0.0
        for row in allRows:
            result['data'].append(
                {
                    'total':row[3],'count':row[2],
                    'cost':row[1],'title':row[0]
                }
            )
            totalCost += row[3]
        result['status'] = 0
        result['message'] = 'OK'
        result['totalCost'] = totalCost
        return result