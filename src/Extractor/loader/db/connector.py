import os  
from functools import wraps  
from typing import List

import pymysql


def singleton(cls):  
    instances = {}  
    
    @wraps(cls)  
    def get_instance(*args, **kwargs):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kwargs)  
        return instances[cls]  
    
    return get_instance  


@singleton  
class Database:  
    def __init__(self, host: str, port: int, user: str, password: str, database: str):  
        """데이터베이스 연결 초기화"""  
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

        self.connection = None
        self.cursor = None
        self.connect()  # 초기 연결 설정


    def connect(self):
        """데이터베이스 연결 설정"""
        if self.connection is None or not self._is_connected():
            try:
                self.connection = pymysql.connect(
                    host=self.__host,
                    port=self.__port,
                    user=self.__user,
                    password=self.__password,
                    database=self.__database,
                    cursorclass=pymysql.cursors.DictCursor  # 결과를 dict 형태로 반환
                )
                self.cursor = self.connection.cursor()
                print("Database connected successfully.")
            except Exception as e:
                self.connection = None
                self.cursor = None
                raise e

    def _is_connected(self):
        """연결 상태 확인"""
        try:
            if self.connection:
                self.connection.ping(reconnect=True)
                return True
        except Exception:
            return False
        return False

    def getter(self, query: str, params: tuple = ()) -> List[dict]:
        """SELECT 쿼리 실행 및 결과 반환"""
        try:
            if not self._is_connected():
                self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def setter(self, query: str, params: tuple = ()) -> None:
        """INSERT, UPDATE, DELETE 쿼리 실행"""
        try:
            if not self._is_connected():
                self.connect()
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def close(self):  
        """연결 종료"""  
        if self.cursor:  
            self.cursor.close()  
        if self.connection:  
            self.connection.close()  
            print("Database connection closed.")


if __name__ == "__main__":
    from dotenv import load_dotenv  

    # .env 파일 로드
    load_dotenv()

    # 비밀변수 가져오기
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT'))
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    # Database 인스턴스 생성
    db = Database(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # getter 예제
    select_query = "SELECT * FROM oil_prices"
    data = db.getter(select_query)
    print(data)

    # 연결 종료
    db.close()