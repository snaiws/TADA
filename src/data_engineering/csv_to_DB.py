import pandas as pd
from sqlalchemy import create_engine



def migrate(path_csv, table_name, configs_db):
    server = f"mysql+pymysql://{configs_db['user']}:{configs_db['password']}@{configs_db['host']}:{configs_db['port']}/{configs_db['database']}?charset=utf8mb4"
    db = create_engine(server)
    df = pd.read_csv(path_csv)
    df.to_sql(table_name, db, if_exists = 'replace', index=False)
    return



if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    configs_db = {
        "host":os.getenv("DB_HOST"),
        "port":int(os.getenv("DB_PORT")),
        "user":os.getenv("DB_USER"),
        "password":os.getenv("DB_PASSWORD"),
        "database":os.getenv("DB_NAME"),
    }
    
    example_path = "/workspace/Projects/tada/base/TADA/src/example"
    example_paths = [os.path.join(example_path, x) for x in os.listdir(example_path)]
    
    for path in example_paths:
        migrate(path, os.path.basename(path).split('.')[0], configs_db)