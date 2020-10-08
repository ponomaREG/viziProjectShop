import pymysql
from pymysql.cursors import DictCursor


connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Huyhuyhuy123',
    db = 'shop',
    charset='utf8',
    cursorclass = DictCursor
)

cursor = connection.cursor()
cursor.execute('select * from Товар;')
print(cursor.fetchall())
cursor.close()
connection.close()