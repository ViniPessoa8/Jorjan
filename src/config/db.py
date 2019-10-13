from pymysql import connect
from pymysql.cursors import DictCursor

def get_connection():
    return connect(host='localhost', 
                     user='root', 
                     db='Jorjan', 
                     password='root', 
                     charset='utf8mb4',
                     cursorclass=DictCursor)

def get_all_users():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuario;"
            cursor.execute(sql)
            result = cursor.fetchall()    
            print(result)
    finally:
        connection.close()

