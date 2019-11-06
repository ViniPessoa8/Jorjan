from pymysql import connect, converters, FIELD_TYPE
from pymysql.cursors import DictCursor

orig_conv = converters.conversions
orig_conv[FIELD_TYPE.BIT] = lambda data: data == '\x01'

def get_connection():
    return connect(host='localhost', 
                    user='root', 
                    db='Jorjan', 
                    password='root', 
                    charset='utf8mb4',
                    cursorclass=DictCursor,
                    conv=orig_conv)

    


