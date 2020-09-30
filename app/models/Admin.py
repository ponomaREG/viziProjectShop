from app import db





class Admin:

    @staticmethod
    def __executeAndGetAllRowsAndKeys(sqlQuery):
        cursor = db.execute(sqlQuery)
        allRows = cursor.fetchall()
        columns  = [description[0] for description in cursor.description]
        cursor.close()
        return {'data':allRows,'keys':columns}
    
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
    def getAllIncomeByPeriod(date_b,date_e):
        return Admin.__makeResultResponse('select sum(total) as "total" from Заказ where date>="{}" and date<= "{}";'.format(date_b,date_e))

    @staticmethod
    def getRatingPopularityOfBooksByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select Товар.title,Товар.id,sum(Забронированная_книга.count) as 'count',sum(Забронированная_книга.price) as 'total' from Забронированная_книга inner join Заказ inner join Товар where Заказ.id == order_id and product_id == Товар.id and Заказ.date >='{}' and Заказ.date <='{}'\
          GROUP by Товар.id order by sum(Забронированная_книга.count) DESC;".format(date_b,date_e))

    @staticmethod
    def getAllOrdersByPeriod(date_b,date_e):
        return Admin.__makeResultResponse("select * from Заказ where date>='{}' and date<= '{}';".format(date_b,date_e))
