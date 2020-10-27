from app import db
from app.models.SqlExecuter import connection 
from app.admin.logger import AdminLogger as Logger




class Admin:

    @staticmethod
    def __executeAndGetAllRowsAndKeys(sqlQuery):
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        allRows = cursor.fetchall()
        columns_names = [i[0] for i in cursor.description]
        cursor.close()
        return {'data':allRows,'keys':columns_names}
    
    @staticmethod
    def __makeResultResponse(sqlQuery):
        res =  Admin.__executeAndGetAllRowsAndKeys(sqlQuery)
        if(len(res['data']) == 0):
            res['status'] = 3
            res['message'] = 'Empty'
            res['data'] = []
        else:
            res['status'] = 0
            res['message'] = 'OK'
        return res

    @staticmethod
    def getSuppliers():
        return Admin.__makeResultResponse('select * from Поставщик;')

    @staticmethod
    def addNewSupplier(supplierName,adminID):
        cursor = connection.cursor()
        query = 'insert into Поставщик(`company_name`) values("{}");'.format(supplierName)
        cursor.execute(query)
        lastrowid = cursor.lastrowid
        cursor.close()
        Logger.log(adminID,query)
        connection.commit()
        result = {}
        result['keys'] = ['new id']
        if(lastrowid > 0):
            result['data'] = [lastrowid]
            result['message'] = 'OK'
            result['status'] = 0
        else:
            result['data'] = []
            result['message'] = 'Not > 0'
            result['status'] = 125
        return result



    @staticmethod
    def setNewValueBook(productID,column,value,adminID):
        result = {}
        cursor = connection.cursor()
        try:
            if(type(value) is int or type(value) is float):
                query = 'update Товар set {}={} where id = {};'.format(column,value,productID)
            else:
                query = 'update Товар set {}="{}" where id = {};'.format(column,value,productID)
            cursor.execute(query)
            Logger.log(adminID,query)
        except:
            result['status'] = 130
            result['message'] = 'ADMIN: sql error because admin entered incorrect input data'
            return result
        lastrowid = cursor.lastrowid
        cursor.close()
        connection.commit()
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = [lastrowid]
        result['keys'] = ['updated id']
        return result



    @staticmethod
    def incQuantityOfBook(productID,quantity,adminID):
        result = {}
        if(quantity<0):
            result['status'] = 130
            result['message'] = 'ADMIN:incorrect input data'
            return result
        cursor = connection.cursor()
        query = 'update Товар set quantity=quantity+{} where id = {};'.format(quantity,productID)
        cursor.execute(query)
        Logger.log(adminID,query)
        lastrowid = cursor.lastrowid
        cursor.close()
        connection.commit()
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = [lastrowid]
        result['keys'] = ['updated id']
        return result

    @staticmethod
    def getInfoOfBookBy(columnName,value,adminID):
        query = 'select * from Товар where {} like "%{}%";'.format(columnName,value)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def addNewDeliveryOfProducts(productID,quantity,cost_purhase,supplier_id,adminID):
        query = 'insert into Закупки(`quantity`,`cost_purchase`,`supplier_id`,`product_id`) values({},{},{},{})'.format(quantity,cost_purhase,supplier_id,productID)
        cursor = connection.cursor()
        cursor.execute(query)
        Logger.log(adminID,query)
        return Admin.incQuantityOfBook(productID,quantity,adminID)



    @staticmethod
    def getColumnsOfTable(tableName):
        return Admin.__makeResultResponse('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`="{}";'.format(tableName))

    @staticmethod
    def insertNewBook(title,author,desc,cost_sale,cost_purchase,quantity,imageName,tags,adminID):
        cursor = connection.cursor()
        query = 'insert into Товар(`book_title`,`author`,`description`,`cost_sale`,`quantity`,`imageLink`,`tags`) \
            values("{}","{}","{}",{},{},"{}","{}")'.format(title,author,desc,cost_sale,quantity,imageName,tags)
        cursor.execute(query)
        Logger.log(adminID,query)
        lastrowid = cursor.lastrowid
        query = 'insert into Закупки(`product_id`,`cost_purchase`,`quantity`) values({},{},{});'.format(lastrowid,cost_purchase,quantity)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        result = {}
        result['keys'] = ['new id']
        if(lastrowid>0):
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = [lastrowid,]
        else:
            result['status'] = 125
            result['message'] = 'Not > 0'
            result['data'] = []
        return result


    @staticmethod
    def getAllIncomeByPeriod(date_b,date_e,adminID):
        query = 'select sum(total) as "total" from Заказ where date>="{}" and date<= "{}";'.format(date_b,date_e)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)



    @staticmethod
    def getRatingPopularityOfBooksByPeriod(date_b,date_e,adminID):
        query = "select Товар.book_title,Товар.id,sum(Забронированная_книга.count) as 'count',sum(Забронированная_книга.price) as 'total' from Забронированная_книга inner join Заказ inner join Товар where Заказ.id = order_id and product_id = Товар.id and Заказ.date >='{}' and Заказ.date <='{}'\
          GROUP by Товар.id order by sum(Забронированная_книга.count) DESC;".format(date_b,date_e)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def getAllOrdersByPeriod(date_b,date_e,adminID):
        query = "select * from Заказ as ord inner join Адрес as addr inner join Покупатель as usr where date>='{}' and date<= '{}' and ord.address_id = addr.id and usr.id = ord.user_id;".format(date_b,date_e)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def getCountOfOrderByPeriod(date_b,date_e,adminID):
        query = "select count(*) as 'count' from Заказ where date>='{}' and date<= '{}';".format(date_b,date_e)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def getInfoOfOrderBy(orderID,adminID):
        query = 'select * from Заказ as ord inner join Адрес as addr where ord.id = {} and address_id = addr.id;'.format(orderID)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def getOrdersByStatus(status,adminID):
        query = 'select * from Заказ where status = {};'.format(status)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse('select * from Заказ where status = {};'.format(status))
        
    @staticmethod
    def __unbookedBooksBy(orderID,adminID):
        query = 'select * from Забронированная_книга where order_id = {};'.format(orderID)
        Logger.log(adminID,query)
        bookedBooks = Admin.__executeAndGetAllRowsAndKeys(query)
        cursor = connection.cursor()
        query = 'delete from Забронированная_книга where order_id = {};'.format(orderID)
        cursor.execute(query)
        Logger.log(adminID,query)
        for row in bookedBooks['data']:
            query = 'update Товар set quantity=quantity+{} where id = {};'.format(row['count'],row['product_id'])
            Logger.log(adminID,query)
            cursor.execute(query)
        cursor.close()    
        connection.commit()

    @staticmethod
    def setNewStatusOfOrder(newStatus,orderID,adminID):
        cursor = connection.cursor()
        query = 'update Заказ set status = {} where id = {};'.format(newStatus,orderID)
        Logger.log(adminID,query)
        cursor.execute(query)
        lastrowid = cursor.lastrowid
        cursor.close()
        if(newStatus == 4 or newStatus == 5):
            Admin.__unbookedBooksBy(orderID,adminID)
        result = {}
        result['keys'] = ['updated id']
        if(lastrowid>0):
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = [lastrowid,]
        else:
            result['status'] = 125
            result['message'] = 'Not > 0'
            result['data'] = []
        return result

    @staticmethod
    def getBookedBooksBy(orderID,adminID):
        query = 'select * from Заброннированная_книга where order_id = {};'.format(orderID)
        Logger.log(adminID,query)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def is_admin_can_write(adminID):
        query = 'select * from Админ where user_id = {};'.format(adminID)
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        return row['level_of_access']> 0
