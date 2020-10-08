from app import db
from app.models.SqlExecuter import connection 




class Admin:

    @staticmethod
    def __executeAndGetAllRowsAndKeys(sqlQuery):
        cursor = connection.cursor()
        cursor = db.execute(sqlQuery)
        allRows = cursor.fetchall()
        cursor.close()
        return allRows
    
    @staticmethod
    def __makeResultResponse(sqlQuery):
        res =  Admin.__executeAndGetAllRowsAndKeys(sqlQuery)
        if(len(res) == 0):
            res['status'] = 3
            res['message'] = 'Empty'
            res['data'] = []
        else:
            res['status'] = 0
            res['message'] = 'OK'
        return res


    @staticmethod
    def insertNewBook(title,author,desc,cost_sale,cost_purchase,quantity,imageName,tags):
        cursor = db.execute('insert into Товар(`title`,`author`,`desc`,`cost_sale`,`cost_purchase`,`quantity`,`imageLink`,`tags`,`rate`) \
            values("{}","{}","{}",{},{},{},"{}","{}",0.0)'.format(title,author,desc,cost_sale,cost_purchase,quantity,imageName,tags))
        db.commit()
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
        return Admin.__makeResultResponse("select Товар.title,Товар.id,sum(Забронированная_книга.count) as 'count',sum(Забронированная_книга.price) as 'total' from Забронированная_книга inner join Заказ inner join Товар where Заказ.id = order_id and product_id = Товар.id and Заказ.date >='{}' and Заказ.date <='{}'\
          GROUP by Товар.id order by sum(Забронированная_книга.count) DESC;".format(date_b,date_e))

    @staticmethod
    def getAllOrdersByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select * from Заказ where date>='{}' and date<= '{}';".format(date_b,date_e))

    @staticmethod
    def getCountOfOrderByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select count(*) as 'count' from Заказ where date>='{}' and date<= '{}';".format(date_b,date_e))

