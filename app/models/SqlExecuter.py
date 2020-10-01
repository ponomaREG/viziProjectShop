from app import db


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
        cursor = db.execute(query)
        columns  = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        return {'row':row,'columns':columns}

    @staticmethod
    def getAllRowAndColumns(query):
        cursor = db.execute(query)
        columns  = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        return {'allRows':rows,'columns':columns}

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
            rowsAndColumns = SqlExecuter.getAllRowAndColumns(query)
            return SqlExecuter.prepareDataByManyRows(rowsAndColumns['allRows'],rowsAndColumns['columns'])
        except:
            return None

    @staticmethod
    def getOneRowsPacked(query):
        try:
            rowAndColumns = SqlExecuter.getOneRowAndColumns(query)
            return SqlExecuter.prepareDataByOneRow(rowAndColumns['row'],rowAndColumns['columns'])
        except:
            return None



    @staticmethod
    def executeModif(query):
        cursor = db.execute(query)
        db.commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid