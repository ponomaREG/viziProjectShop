from app import db
from app.models.SqlExecuter import connection 




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
    def setNewValueBook(productID,column,value):
        result = {}
        cursor = connection.cursor()
        try:
            print(column)
            print(type(column))
            if(type(value) is int or type(value) is float):
                cursor.execute('update Товар set {}={} where id = {};'.format(column,value,productID))
            else:
                print('update Товар set {}="{}" where id = {};'.format(column,value,productID))
                cursor.execute('update Товар set {}="{}" where id = {};'.format(column,value,productID))
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
    def incQuantityOfBook(productID,quantity):
        result = {}
        if(quantity<0):
            result['status'] = 130
            result['message'] = 'ADMIN:incorrect input data'
            return result
        cursor = connection.cursor()
        cursor.execute('update Товар set quantity=quantity+{} where id = {};'.format(quantity,productID))
        lastrowid = cursor.lastrowid
        cursor.close()
        connection.commit()
        result['status'] = 0
        result['message'] = 'OK'
        result['lastrowid'] = lastrowid
        return result

    @staticmethod
    def getInfoOfBookBy(columnName,value):
        return Admin.__makeResultResponse('select * from Товар where {} like "%{}%";'.format(columnName,value))


    @staticmethod
    def getColumnsOfTable(tableName):
        return Admin.__makeResultResponse('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`="{}";'.format(tableName))

    @staticmethod
    def insertNewBook(title,author,desc,cost_sale,cost_purchase,quantity,imageName,tags):
        cursor = connection.cursor()
        cursor.execute('insert into Товар(`book_title`,`author`,`description`,`cost_sale`,`cost_purchase`,`quantity`,`imageLink`,`tags`) \
            values("{}","{}","{}",{},{},{},"{}","{}")'.format(title,author,desc,cost_sale,cost_purchase,quantity,imageName,tags))
        connection.commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        result = {}
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
    def getAllIncomeByPeriod(date_b,date_e):
        return Admin.__makeResultResponse('select sum(total) as "total" from Заказ where date>="{}" and date<= "{}";'.format(date_b,date_e))



    @staticmethod
    def getRatingPopularityOfBooksByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select Товар.book_title,Товар.id,sum(Забронированная_книга.count) as 'count',sum(Забронированная_книга.price) as 'total' from Забронированная_книга inner join Заказ inner join Товар where Заказ.id = order_id and product_id = Товар.id and Заказ.date >='{}' and Заказ.date <='{}'\
          GROUP by Товар.id order by sum(Забронированная_книга.count) DESC;".format(date_b,date_e))

    @staticmethod
    def getAllOrdersByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select * from Заказ as ord inner join Адрес as addr inner join Покупатель as usr where date>='{}' and date<= '{}' and ord.address_id = addr.id and usr.id = ord.user_id;".format(date_b,date_e))

    @staticmethod
    def getCountOfOrderByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select count(*) as 'count' from Заказ where date>='{}' and date<= '{}';".format(date_b,date_e))

