from app import db
from utils import sqlQueryHelper
from utils import imageHelper
from utils import tagsHelper


class Product:
    id = -1
    title = None
    cost_sale = -1.0
    quantity = -1
    def __init__(self,title,cost_sale,quantity,id):
        self.id = id
        self.title = title
        self.cost_sale = cost_sale
        self.quantity = quantity

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
                'quantity':rw[5],'tags':rw[6],
                'id':rw[0],'imageLink':imageHelper.makeFullPathToImage(rw[8])
                }
            result['data'].append(rowDict)
        result['status'] = 0
        result['count'] = len(allRows)
        result['message'] = "OK"
        cursor.close()
        return result


    @staticmethod
    def getQuantityOfRowsInTable(query):
        result = {}
        try:
            cursor = db.execute(
                query
                )
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            cursor.close()
            return result
        result['status'] = 0
        result['message'] = 'OK'
        result['count'] = len(cursor.fetchall())
        cursor.close()
        return result

    @staticmethod
    def getAllProfuctsFilteredByRate(page,offset):
        result = {}
        try:
            cursor = db.execute(
                'select * from Товар order by rate DESC LIMIT {} OFFSET {};'
                .format(offset,offset*(page-1)))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            cursor.close()
            return result
        return Product.__prepareProducts(cursor)

    @staticmethod
    def getAllProfuctsFilteredByQuery(query,page=-1,offset=-1):
        result = {}
        try:
            cursor = db.execute(
                'select * from Товар where title like "%{0}%" or author like "%{0}%" order by rate DESC LIMIT {1} OFFSET {2};'
                .format(query,offset,offset*(page-1)))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            cursor.close()
            return result
        return Product.__prepareProducts(cursor)

    @staticmethod
    def getAllProductsFilteredByTags(tags,page,offset):
        result = {}
        try:
            print(sqlQueryHelper.buildSqlQueryByTagsAndPage('select * from Товар',tags,page,offset))
            cursor = db.execute(sqlQueryHelper.buildSqlQueryByTagsAndPage('select * from Товар',tags,page,offset))
        except:
            result['status'] = 3
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        return Product.__prepareProducts(cursor)

    @staticmethod
    def getAvailableTags():
        result = {}
        cursor = db.execute('select tags from Товар;')
        allRows = cursor.fetchall()
        cursor.close()
        if(len(allRows) == 0):
            result['status'] = 2
            result['message'] = 'Empty data'
            return result
        tagsArrUNIQUE = []
        for row in allRows:
            tags = row[0]
            tagsArr = tagsHelper.makeTagsStrToArray(tags)
            tagsArrUNIQUE = list(set(tagsArrUNIQUE + tagsArr))
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = tagsArrUNIQUE
        return result


    @staticmethod
    def getDetailsOfProduct(productID):
        result = {}
        try:
            cursor = db.execute('select * from Товар where id = {};'.format(productID))
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            result['data'] = []
            cursor.close()
            return result
        rw = cursor.fetchone()
        cursor.close()
        if(rw is None):
            result['status'] = 2
            result['message'] = 'Empty data'
            result['data'] = []
            cursor.close()
            return result
        else:
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = [{'id':rw[0],'title':rw[1],
            'desc':rw[2],'cost':rw[4],'quantity':rw[5],
            'tags':rw[6],'rate':rw[7],'imageLink':imageHelper.makeFullPathToImage(rw[8])}]
            return result
