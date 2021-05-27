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


def select(query):
    # 전역에 선언되어 있는 connection 객체 참조
    global dbconn
    # 커서 취득
    cursor = dbconn.cursor()
    # 쿼리 실행
    cursor.execute(query)
    # 실행된 결과 RETURN - cursor가 결과의 위치를 갖고 있음.
    # fetch 함수 이용해서 일부분을 리턴하거나 리스트 형태로 리턴도 가능하다.
    # 이 경우에는 용량이 많으면 느려지게 된다.(단점)
    return cursor # 커서 객체를 리턴함.


# DML 처리 함수 : INSERT, UPDATE, DELETE 처리
## execute() 사용
## commit 필요함 -> commit 처리 후에 에러가 발생하면 예외처리 후에 rollback 처리
## 사용자에게 쿼리와 쿼리에 사용될 값을 분리해 받아서 처리

def execute_dml(query, values):
    # 전역에 선언되어 있는 connection 객체 참조
    global dbconn
    try:
        # 커서 취득
        cursor = dbconn.cursor()
        # 쿼리 실행
        # execute 함수는 내부에서 문자열 포맷팅으로 설정된 값에 실제 값을 매칭시켜줌.
        cursor.execute(query, values)
        dbconn.commit()

    except Exception as e:
        dbconn.rollback()

# DML 이외의 쿼리를 실행하는 함수 (CREATE ALTER DROP)
## commit 필요함 -> commit 처리 후에 에러가 발생하면 예외처리 후에 rollback 처리

def execute_ddl(query):
    # connection 객체 가져오기
    global dbconn
    try:
        # 커서 취득
        cursor = dbconn.cursor()
        # 쿼리 실행
        cursor.execute(query)
        # 쿼리 커밋
        dbconn.commit()
    except Exception as e:
        print(e)
        dbconn.rollback()