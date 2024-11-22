import mysql.connector  
from datetime import datetime  
from typing import List  
import os  
from dotenv import load_dotenv  

class DatabaseLoader:  
    def __init__(self):  
        """데이터베이스 연결 초기화"""  
        load_dotenv()  
        
        self.connection = mysql.connector.connect(  
            host=os.getenv('DB_HOST'),  
            port=int(os.getenv('DB_PORT', '50007')),  # 기본값으로 50007 설정
            user=os.getenv('DB_USER'),  
            password=os.getenv('DB_PASSWORD'),  
            database=os.getenv('DB_NAME')  
        )  
        self.cursor = self.connection.cursor()  
        self._initialized = False  
        self.initialize_table()  

    def initialize_table(self):  
        """테이블 초기화"""  
        if self._initialized:  
            print("이미 초기화되어 있습니다.")  
            return  
    
        print("테이블 초기화 시작...")  
    
        try:  
            # 테이블 존재 여부 확인  
            self.cursor.execute("""  
                SELECT COUNT(*)  
                FROM information_schema.tables  
                WHERE table_schema = %s  
                AND table_name = 'oil_prices'  
            """, (os.getenv('DB_NAME'),))  
            
            table_exists = self.cursor.fetchone()[0] > 0  
            print(f"테이블 존재 여부: {'있음' if table_exists else '없음'}")  
    
            # 테이블 생성  
            create_table_query = """  
            CREATE TABLE IF NOT EXISTS oil_prices (  
                id INT AUTO_INCREMENT PRIMARY KEY,  
                date DATE NOT NULL,  
                product VARCHAR(20) NOT NULL,  
                price DECIMAL(10, 2),  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
                UNIQUE KEY date_product_idx (date, product)  
            )  
            """  
            print("테이블 생성 쿼리 실행 시작...")  
            self.cursor.execute(create_table_query)  
            self.connection.commit()  
            print("테이블 생성 완료 및 커밋됨")  
    
            # 테이블이 실제로 생성되었는지 다시 확인  
            self.cursor.execute("""  
                SELECT COUNT(*)  
                FROM information_schema.tables  
                WHERE table_schema = %s  
                AND table_name = 'oil_prices'  
            """, (os.getenv('DB_NAME'),))  
            
            if self.cursor.fetchone()[0] > 0:  
                print("테이블이 성공적으로 생성되었습니다.")  
            else:  
                print("경고: 테이블이 생성되지 않았습니다!")  
    
        except Exception as e:  
            print(f"테이블 초기화 중 오류 발생: {str(e)}")  
            raise  
        
        self._initialized = True  
        print("초기화 프로세스 완료")

    def insert_oil_price_data(self, data: List[List[str]], headers: List[str]):  
        """유가 데이터 삽입 또는 업데이트"""  
        # 제품 리스트 정의  
        products = ["고급휘발유", "보통휘발유", "실내등유", "선박용경유", "자동차용경유",   
                   "벙커C유", "용제", "아스팔트"]  

        for row in data:  
            date_str = row[0].strip()  
        
            try:  
                # '월' 제거 및 년도 처리  
                if '월' in date_str:  
                    if '년' not in date_str:  
                        month = date_str.replace('월', '').strip()  
                        for prev_row in data:  
                            if '년' in prev_row[0]:  
                                year = prev_row[0].split('년')[0].strip()  
                                if len(year) == 2:  
                                    year = '20' + year  
                                break  
                        date_str = f"{year}-{month.zfill(2)}-01"  
                    else:  
                        year = date_str.split('년')[0].strip()  
                        if len(year) == 2:  
                            year = '20' + year  
                        month = date_str.split('년')[1].replace('월', '').strip()  
                        date_str = f"{year}-{month.zfill(2)}-01"  
                
                date = datetime.strptime(date_str, '%Y-%m-%d').date()  
            
                # 첫 번째 컬럼(날짜)을 제외한 가격 데이터 처리  
                price_data = row[1:]  # 두 번째 컬럼부터 가격 데이터  
            
                for product_idx, product in enumerate(products):  
                    if product_idx >= len(price_data):  
                        continue  
                    
                    price_str = price_data[product_idx].strip().replace(',', '')  
                
                    # 유효하지 않은 가격 데이터 처리  
                    if price_str in ['-', '', 'None', 'NULL', 'nan', 'NaN']:  
                        continue  
                
                    try:  
                        price = float(price_str)  
                        if price <= 0:  # 0이나 음수 가격은 제외  
                            continue  
                        
                        query = """  
                        INSERT INTO oil_prices (date, product, price)  
                        VALUES (%s, %s, %s)  
                        ON DUPLICATE KEY UPDATE  
                        price = IF(ABS(price - VALUES(price)) > 0.01, VALUES(price), price)  
                        """  
                    
                        self.cursor.execute(query, (date, product, price))  

                    except (ValueError, TypeError) as e:  
                        print(f"가격 변환 오류 무시 (날짜: {date}, 제품: {product}, 값: {price_str})")  
                        continue  

            except ValueError as e:  
                print(f"날짜 형식 오류 ({date_str}): {str(e)}")  
                continue  

        self.connection.commit()  

    def close_connection(self):  
        """데이터베이스 연결 종료"""  
        if hasattr(self, 'cursor') and self.cursor:  
            self.cursor.close()  
        if hasattr(self, 'connection') and self.connection:  
            self.connection.close()  
            self._initialized = False