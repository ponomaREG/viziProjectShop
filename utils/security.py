
from app.models.SqlExecuter import connection


class Security:



    @staticmethod
    def escape_sql(s):
        return connection.escape_string(s)


    

