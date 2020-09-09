from app import db
from utils import sqlQueryHelper


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