from app import db
from utils import sqlQueryHelper
from utils import imageHelper
from utils import tagsHelper
from app.models.SqlExecuter import SqlExecuter


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
    def __preparePackedProducts(allRows):
        result = {}
        if(allRows is None or len(allRows) == 0):
            result['status'] = 2
            result['message'] = "Empty data"
            result['data'] = []
            return result
        for row in allRows:
            row['imageLink'] = imageHelper.makeFullPathToImage(row['imageLink'])
        result['data'] = allRows
        result['status'] = 0
        result['message'] = 'OK'
        return result

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
                'title':rw[9]+' - '+rw[1],'desc':rw[2],
                'rate':rw[7],'cost':rw[4],
                'quantity':rw[5],'tags':rw[6],
                'id':rw[0],'imageLink':imageHelper.makeFullPathToImage(rw[8]),
                'author':rw[9],'bookTitle':rw[1]
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
            row = SqlExecuter.getOneRowsPacked(query)
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        if(row is not None):
            result['status'] = 0
            result['message'] = 'OK'
            result['count'] = row['count']
        else:
            result['status'] = 2
            result['message'] = 'Not founded'
            result['count'] = 0
        return result

    @staticmethod
    def getAllProfuctsFilteredById(page,offset):
        result = {}
        try:
            
            allRows = SqlExecuter.getAllRowsPacked(
                'select *,cost_sale as "cost",title as "bookTitle",(title || " - " || author) as "title" from Товар order by id DESC LIMIT {} OFFSET {};'
                .format(offset,offset*(page-1)))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        return Product.__preparePackedProducts(allRows)

    @staticmethod
    def getAllProfuctsFilteredByQuery(query,page=-1,offset=-1):
        result = {}
        try:
            allRows = SqlExecuter.getAllRowsPacked(
                'select *,cost_sale as "cost",title as "bookTitle",(title || " - " || author) as "title" from Товар where title like "%{0}%" or author like "%{0}%" order by id DESC LIMIT {1} OFFSET {2};'
                .format(query,offset,offset*(page-1)))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        return Product.__preparePackedProducts(allRows)

    @staticmethod
    def getAllProductsFilteredByTags(tags,page,offset):
        result = {}
        try:
            allRows = SqlExecuter.getAllRowsPacked(sqlQueryHelper.buildSqlQueryByTagsAndPage('select *,cost_sale as "cost",title as "bookTitle",(title || " - " || author) as "title" from Товар',tags,page,offset))
        except:
            result['status'] = 1
            result['message'] = "Runtime error while executing sql query"
            result['data'] = []
            return result
        return Product.__preparePackedProducts(allRows)

    @staticmethod
    def getAvailableTags():
        result = {}
        allRows = SqlExecuter.getAllRowsPacked('select tags from Товар;')
        if(allRows is None or len(allRows) == 0):
            result['status'] = 2
            result['message'] = 'Empty data'
            result['data'] = []
            return result
        tagsArrUNIQUE = []
        for row in allRows:
            tags = row['tags']
            tagsArr = tagsHelper.makeTagsStrToArray(tags)
            tagsArrUNIQUE = list(set(tagsArrUNIQUE + tagsArr))
        result['status'] = 0
        result['message'] = 'OK'
        result['data'] = tagsArrUNIQUE
        return result


    @staticmethod
    def addNewRate(userID,productID,mark):
        result = {}
        row = SqlExecuter.getOneRowsPacked('select * from Рейтинг where user_id = {} and product_id = {};'.format(userID,productID))
        if(row is not None):
            result['status'] = 9
            result['message'] = 'User already set mark'
            result['data'] = []
            return result
        lastrowid = SqlExecuter.executeModif('insert into Рейтинг values({},{},{});'.format(productID,userID,mark))
        if(lastrowid != -1):
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = lastrowid
        else:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            result['data'] = []
        return result


    @staticmethod
    def getRateOfProduct(productID):
        row = SqlExecuter.getOneRowsPacked('select round(coalesce(avg(mark),0),2) as "count" from Рейтинг where product_id == {};'.format(productID))
        return float(row['count'])


    @staticmethod
    def getDetailsOfProduct(productID):
        result = {}
        try:
            row = SqlExecuter.getOneRowsPacked('select *,cost_sale as "cost",title as "bookTitle",(title || " - " || author) as "title",round(avg(rate.mark),2) as "rate" from Товар inner join Рейтинг as rate where id = {};'.format(productID))
        except:
            result['status'] = 1
            result['message'] = 'SQL Runtime error'
            result['data'] = []
            return result
        if(row is None):
            result['status'] = 2
            result['message'] = 'Empty data'
            result['data'] = []
            return result
        else:
            row['imageLink'] = imageHelper.makeFullPathToImage(row['imageLink'])
            result['status'] = 0
            result['message'] = 'OK'
            result['data'] = [row]
            return result
