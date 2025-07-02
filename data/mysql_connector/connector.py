
import pymysql
import json

class CustomMySQLConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            print("Connection successful")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def insert_articles_from_json(self, json_file_path):
        if not self.connection:
            print("⚠️ 연결이 없습니다.")
            return

        cursor = self.connection.cursor()

        with open(json_file_path, 'r', encoding='utf-8') as file:
            articles = json.load(file)

        insert_sql = """
            INSERT INTO article (url, content, title, created_time, publisher)
            VALUES (%s, %s, %s, %s, %s)
        """

        success_count = 0
        for a in articles:
            try:
                cursor.execute(insert_sql, (
                    a.get("URL", "추출 실패"),
                    a.get("본문", "추출 실패"),
                    a.get("기사제목", "추출 실패"),
                    a.get("작성일자", "추출 실패"),
                    a.get("신문사", "추출 실패")
                ))
                success_count += 1
            except pymysql.MySQLError as e:
                print(f"❌ 삽입 실패: {e} | 제목: {a.get('기사제목')}")
        
        self.connection.commit()
        print(f"✅ 삽입 완료: {success_count}건")

        cursor.close()