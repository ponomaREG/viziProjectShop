
from app.models.Cart import Cart
from app.models.Address import Address
from app.models.Product import Product
from app.models.SqlExecuter import SqlExecuter
from utils import imageHelper
from utils import emailSender
from utils import addressBuilder


class Order:

    @staticmethod
    def getOrdersOfUser(userID):
        result = {}
        allRows = SqlExecuter.getAllRowsPacked('select ord.*,addr.district,addr.street,addr.flat,addr.floor,\
        addr.porch,addr.house,address_id as "address" \
        from Заказ as ord inner join Адрес as addr\
         where ord.address_id = addr.id and user_id = {} order by id DESC;'.format(userID))
        if(allRows is None or len(allRows) == 0):
            result['status'] = 2
            result['message'] = 'Empty response'
            result['data'] = []
            return result
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = allRows
        return result

    @staticmethod
    def cancelOrder(userID,orderID):
        result = {}
        if(not Order.checkIfUserHaveOrderWith(userID,orderID)):
            result['status'] = 3
            result['message'] = 'Why are you so curious?'
            result['data'] = []
            return result
        if(not Order.checkIfOrderExists(orderID)):
            result['status'] = 40
            result['message'] = 'Not founded'
            result['data'] = []
            return result
        query = 'update Заказ set status = 4 where id = {};'.format(orderID)
        SqlExecuter.executeModif(query)
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = []
        return result

    @staticmethod
    def getDetailsOfOrder(userID,orderID):
        result = {}
        if(not Order.checkIfUserHaveOrderWith(userID,orderID)):
            result['status'] = 3
            result['message'] = 'Why are you so curious?'
            result['data'] = []
            return result
        if(not Order.checkIfOrderExists(orderID)):
            result['status'] = 40
            result['message'] = 'Not founded'
            result['data'] = []
            return result

        data = SqlExecuter.getAllRowsPacked("select pr.id,pr.imageLink,pr.book_title,bk.count,pr.cost_sale*bk.count as 'total' from Забронированная_книга as bk inner join Товар as pr on bk.order_id = {} and pr.id = bk.product_id;".format(orderID))
        for row in data:
            row['imageLink'] = imageHelper.makeFullPathToImage(row['imageLink'])
        rowAddressPacked = SqlExecuter.getOneRowsPacked(
            "select ord.id as 'orderID',addr.*,ord.date,ord.status,ord.total,concat(addr.district,' district,',addr.street,', ',addr.house) as 'address' from Заказ as ord  inner join Адрес as addr \
            where ord.address_id = addr.id and ord.id = {};".format(orderID))
        result['address'] = rowAddressPacked
        result['info'] = {'orderID':rowAddressPacked['orderID'],'date':rowAddressPacked['date'],'status':rowAddressPacked['status'],
                            'total':rowAddressPacked['total']}
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = data
        return result




    @staticmethod
    def addNewOrder(userID,district,flat,house,floor,street,porch='',email='',desc = '',phone=''):
        result = {}
        try:
            quantityInCart = Cart.getCountOfItemsInCart(userID)
            if(quantityInCart['status'] == 2):
                result['status'] = 2
                result['message'] = 'Empty cart'
                result['data'] = []
                return result
        except IndexError:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            return result
        cartOfUser = Cart.getCartOfUser(userID)['data']
        isError = False
        for row in cartOfUser:
            product = SqlExecuter.getOneRowsPacked('select * from Товар where id = {};'.format(row['id']))
            if(product['quantity'] < row['count']):
                isError = True
                SqlExecuter.executeModif('delete from Корзина where product_id = {} and user_id = {};'.format(row['id'],userID))
        if(isError):
                result['status'] = 10 
                result['message'] = 'Attempt to order product with incorrect quantity'
                return result
        try:
            lastrowidAddress = Address.addNewAddress(district,house,floor,flat,porch,street)
        except IndexError:
                result['status'] = 1
                result['message'] = 'SQL runtime error'
                result['data'] = []
                return result 
        
        try:
            lastrowid = SqlExecuter.executeModif('insert into Заказ(`user_id`,`status`,`total`,`address_id`,`description`,`email`,`phone`) values({},{},{},{},"{}","{}","{}");'.format(
                    userID,
                    0,
                    Cart.countTotalCostOfUser(userID),
                    lastrowidAddress,
                    desc,
                    email,
                    phone))
        except IndexError:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            result['data'] = []
            return result
        data = {'id':lastrowid,"data":cartOfUser}
        for row in cartOfUser:
            try:
                SqlExecuter.executeModif('insert into Забронированная_книга \
                    values({},{},{},{})'.format(row['id'],row['count'],lastrowid,row['cost']))
                SqlExecuter.executeModif('delete from Корзина where \
                    user_id = {} and product_id = {};'.format(userID,row['id']))
                SqlExecuter.executeModif('update Товар set quantity = quantity - {} where id = {};'.format(row['count'],row['id']))

            except IndexError:
                result['status'] = 1
                result['message'] = 'SQL runtime error'
                result['data'] = []
                return result
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = data
        # if(email is not None):
        #     emailSender.EmailSender.sendEmailTo([email],orderDetails=result['data'])
        return result

    @staticmethod
    def checkIfUserHaveOrderWith(userID,orderID):
        return SqlExecuter.getOneRowsPacked('select * from Заказ where user_id = {} and id = {};'.format(userID,orderID)) is not None

    @staticmethod
    def checkIfOrderExists(orderID):
        return SqlExecuter.getOneRowsPacked('select * from Заказ where id = {} and status != 4 and status != 5;'.format(orderID)) is not None
        
