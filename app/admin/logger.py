
from app.models.SqlExecuter import connection
import json

class AdminLogger:



    @staticmethod
    def log(adminID,operation):
        dumpsOperation = json.dumps(operation,ensure_ascii = False)
        cursor = connection.cursor()
        cursor.execute('insert into логи(`admin_id`,`operation`) values({},"{}");'.format(adminID,dumpsOperation[1:len(dumpsOperation)-2]))
        cursor.close()
        connection.commit()