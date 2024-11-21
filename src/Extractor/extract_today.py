from loader.db.connector import Database
from loader.db.query import query_creat_table_oil, query_update_oilprice



def get_oilprice_now(dbinfo): 


    return 



if __name__ == "__main__":
    import os

    from dotenv import load_dotenv  

    # .env 파일 로드
    load_dotenv()
    
    dbinfo = {
        "host":os.getenv('DB_HOST'),
        "port":int(os.getenv('DB_PORT')),
        "user":os.getenv('DB_USER'),
        "password":os.getenv('DB_PASSWORD'),
        "database":os.getenv('DB_NAME')
    }
    get_oilprice_now(dbinfo)