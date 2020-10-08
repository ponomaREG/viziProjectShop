from app import db
import pymysql
from pymysql.cursors import DictCursor


connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Huyhuyhuy123',
    db = 'shop',
    charset = 'utf8',
    use_unicode = True,
    cursorclass = DictCursor
)


class SqlExecuter:


    @staticmethod
    def getOneRow(query):
        cursor = db.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row


    @staticmethod
    def getAllRows(query):
        cursor = db.execute(query)
        allRows = cursor.fetchall()
        cursor.close()
        return allRows

    @staticmethod
    def getOneRowAndColumns(query):
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    @staticmethod
    def getAllRowAndColumns(query):
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        print(rows)
        return rows

    @staticmethod
    def prepareDataByOneRow(row,columns):
        if(row is None or len(row) == 0):
            return None
        keyword = {}
        for i in range(len(columns)):
            keyword[columns[i]] = row[i]
        return keyword 

    @staticmethod
    def prepareDataByManyRows(allRows,columns):
        if(allRows is None or len(allRows) == 0):
            return None
        data = []
        for row in allRows:
            data.append(SqlExecuter.prepareDataByOneRow(row,columns))
        return data

    @staticmethod
    def getAllRowsPacked(query):
        try:
            return SqlExecuter.getAllRowAndColumns(query)
        except:
            return None

    @staticmethod
    def getOneRowsPacked(query):
        try:
            return SqlExecuter.getOneRowAndColumns(query)
        except:
            return None



    @staticmethod
    def executeModif(query):
        cursor = connection.cursor()
        cursor.execute(query)
        lastrowid = cursor.lastrowid
        connection.commit()
        cursor.close()
        return lastrowid