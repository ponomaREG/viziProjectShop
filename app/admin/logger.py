
from app.models.SqlExecuter import connection
import json

class AdminLogger:



    @staticmethod
    def log(adminID,operation):
        print('insert into логи(`admin_id`,`operation`) values({},"{}");'.format(adminID,json.dumps(operation, ensure_ascii=False)[1:len(operation)-2]))
        print(json.dumps(operation, ensure_ascii=False)[1:len(operation)-2])
        cursor = connection.cursor()
        cursor.execute('insert into логи(`admin_id`,`operation`) values({},"{}");'.format(adminID,json.dumps(operation, ensure_ascii=False)[1:len(operation)-2]))
        cursor.close()
        connection.commit()