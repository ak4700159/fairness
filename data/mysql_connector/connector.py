import pymysql
from fair_setup import connect_mysql_database as connect_dastabase_server

class DatabaseConnector:
    def __init__(self):
        self.connection = connect_dastabase_server(config_path=r"C:\Users\ksm\Desktop\fairness\config.yaml")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    # SQL문 실행
    def executeSQL(self, sql_query, values):
        if not self.connection:
            print("데이터베이스 연결이 없습니다")
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, *values)
        except pymysql.MySQLError as e:
            print(f"❌ SQL 실행 실패 {e}")
        self.connection.commit()
        cursor.close()