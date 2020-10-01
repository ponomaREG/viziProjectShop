from app import db
from utils import imageHelper
from app.models.SqlExecuter import SqlExecuter

class Cart:


    @staticmethod
    def getQuantityOfProductInCart(userID,productID):
        result = {}
        row = SqlExecuter.getOneRow('select count from Корзина where user_id = {} and product_id = {};'
        .format(userID,productID))
        if(row is None):
            result['status'] = 2
            result['message'] = 'Product doesnt exist in cart'
            result['data'] = {'count':0}
            return result
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = {'count':row[0]}
        return result




    @staticmethod #TODO: REFACTOR
    def countTotalCostOfUser(userID):
        row = SqlExecuter.getOneRowsPacked('select SUM(cart.count*pr.cost_sale) as "totalCost" \
                as "Total" from Товар as pr \
                inner join Корзина as cart on pr.id == product_id \
                and user_id = {};'.format(userID))
        return float(row['totalCost'])

    @staticmethod
    def removeItemInCartOfUser(userID,productID):
        result = {}
        try:
            row = SqlExecuter.getOneRowsPacked(
                'select * from Корзина where product_id = {} and user_id = {};'.format(productID,userID)
            )
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            return result
        if(row is not None):
            if(row['count']>1):
                try:
                    SqlExecuter.executeModif('update Корзина set count = count - 1 where \
                    product_id = {} and user_id = {};'.format(productID,userID))
                except:
                    result['status'] = 1
                    result['message'] = 'SQL Runtime error'
                    return result
                result['status'] = 0
                result['message'] = 'OK'
                return result
            try:
                SqlExecuter.executeModif('delete from Корзина where \
                    product_id = {} and user_id = {};'.format(productID,userID))
            except:
                result['status'] = 1
                result['message'] = 'SQL Runtime error'
                return result
            result['status'] = 0
            result['message'] = 'OK'
            return result
        result['status'] = 2
        result['message'] = 'Not found item'
        return result


    @staticmethod
    def addItemInCartOfUser(userID,productID):
        result = {}
        
        row = SqlExecuter.getOneRowsPacked(
            'select * from Товар where id = {};'.format(productID)
        )
        
        if(row is None):
            result['status'] = 2
            result['message'] = 'No such product'
            return result
        if(row['quantity'] == 0):
            result['status'] = 4
            result['message'] = 'Zero quantity of called product'
            return result
        quantityOfProduct = row['quantity']
        try:
            row = SqlExecuter.getOneRowsPacked(
                'select * from Корзина where product_id = {} and user_id = {};'.format(productID,userID)
            )
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            return result

        if(row is not None):
            if(row['count'] >= quantityOfProduct):
                result['status'] = 5
                result['message'] = 'Not enough products'
                return result
            try:
                SqlExecuter.executeModif(
                    'update Корзина set count = count + 1 \
                    where product_id = {} and user_id = {}'.format(productID,userID))
            except:
                result['status'] = 1
                result['message'] = 'SQL Runtime error'
                return result
            result['status'] = 0
            result['message'] = 'Inc count'
            return result
        
        try:
            SqlExecuter.executeModif('insert into Корзина values({},{},1)'.format(userID,productID))
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            return result
        result['status'] = 0
        result['message'] = 'Add new values'
        return result
        

    @staticmethod
    def getCountOfItemsInCart(userID):
        result = {}
        try:
            row = SqlExecuter.getOneRowsPacked(
                'select SUM(count) as "count" from Корзина where user_id = {};'.format(userID))
            if(row is None):
                result['status'] = 2
                result['message'] = 'Empty cart'
                result['data'] = [0]
                return result
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = [row['count']]
            return result
        except:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            return result


    @staticmethod
    def getCartOfUser(userID):
        result = {}
        try:
            data = SqlExecuter.getAllRowsPacked('select (pr.title || " - " || pr.author) as "title",pr.cost_sale as "cost",cart.count,cart.count*pr.cost_sale as "total",pr.id,pr.imageLink,pr.author from Товар as pr inner join Корзина as cart on pr.id == product_id and user_id = {};'.format(userID))
        except:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            return result
        if(len(data) == 0):
            result['status'] = 2
            result['message'] = 'Empty cart'
            result['data'] = []
            return result
        result['data'] = []
        result['count'] = len(data)
        result['status'] = 0
        result['message'] = 'OK'
        result['totalCost'] = SqlExecuter.prepareDataByOneRow("select SUM(cart.count*pr.cost_sale) as 'totalCost' from Товар as pr inner join Корзина as cart on pr.id == product_id and user_id = {};".format(userID))['totalCost']
        return result