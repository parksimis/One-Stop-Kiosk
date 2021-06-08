import pymysql

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '0000',
    'database': 'mydb',
    'charset': 'utf8'
}

dbconn = pymysql.connect(**config)


def select(query, values=None):
    global dbconn
    cursor = dbconn.cursor()
    cursor.execute(query, values)
    return cursor


def execute_dml(query, values):
    global dbconn
    try:
        cursor = dbconn.cursor()
        cursor.execute(query, values)
        dbconn.commit()
    except Exception as e:
        dbconn.rollback()


def execute_ddl(query):
    global dbconn
    try:
        cursor = dbconn.cursor()
        cursor.execute(query)
        dbconn.commit()
    except Exception as e:
        print(e)
        dbconn.rollback()