import os
from functools import wraps
from typing import List
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine



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
    def __init__(self, db_type: str, user: str, password: str, host: str, port: int, database: str, driver: str = None):
        self.engine: Engine = None
        self.db_type = db_type
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.driver = driver
        self.connect()


    def connect(self):
        """데이터베이스 연결 설정"""
        try:
            # 연결 문자열 생성
            connection_string = self._get_connection_string()
            self.engine = create_engine(connection_string)
            print(f"Connected to {self.db_type} database successfully.")
        except Exception as e:
            print(f"Error connecting to {self.db_type} database: {e}")
            self.engine = None
            raise e


    def _get_connection_string(self) -> str:
        """데이터베이스에 맞는 연결 문자열 생성"""
        if self.db_type == "mysql":
            driver = self.driver or "pymysql"  # 기본 드라이버
            return f"mysql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == "postgresql":
            driver = self.driver or "psycopg2"
            return f"postgresql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == "sqlite":
            # SQLite는 호스트나 포트가 필요 없음
            return f"sqlite:///{self.database}"
        elif self.db_type == "oracle":
            driver = self.driver or "cx_oracle"
            return f"oracle+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == "mssql":
            driver = self.driver or "pyodbc"
            return f"mssql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
        

    def getter(self, query: str, params: dict = None):
        """SELECT 쿼리 실행 및 튜플 형태로 반환"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return [tuple(row) for row in result]  # 각 Row를 튜플로 변환
        except Exception as e:
            print(f"Error in getter: {e}")
            raise e


    def setter(self, query: str, params: dict = None) -> None:
        """INSERT, UPDATE, DELETE 쿼리 실행"""
        try:
            with self.engine.connect() as connection:
                with connection.begin():  # 트랜잭션 처리
                    connection.execute(text(query), params or {})
        except Exception as e:
            print(f"Error in setter: {e}")
            raise e


    def close(self):
        """연결 종료"""
        try:
            if self.engine:
                self.engine.dispose()
                print("Database connection closed.")
        except Exception as e:
            print(f"Error closing database connection: {e}")



if __name__ == "__main__":
    from dotenv import load_dotenv

    # .env 파일 로드
    load_dotenv()

    # 비밀 변수 가져오기
    DB_TYPE = os.getenv("DB_TYPE")  # mysql, postgresql, sqlite, oracle, mssql
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER", None)  # 선택적

    # Database 인스턴스 생성
    db = Database(
        db_type=DB_TYPE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        driver=DB_DRIVER
    )

    # getter 예제
    select_query = "SHOW TABLES"
    try:
        data = db.getter(select_query)
        print(data)
    except Exception as e:
        print(f"Query failed: {e}")

    # 연결 종료
    db.close()
