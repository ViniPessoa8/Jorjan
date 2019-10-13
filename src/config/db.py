from pymysql import connect
from pymysql.cursors import DictCursor

def get_connection():
    return connect(host='localhost', 
                     user='root', 
                     db='Jorjan', 
                     password='root', 
                     charset='utf8mb4',
                     cursorclass=DictCursor)

    


