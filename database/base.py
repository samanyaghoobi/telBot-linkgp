from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import MYSQL_CONFIG
import pymysql

Base = declarative_base()

def ensure_database():
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            port=MYSQL_CONFIG["port"]
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        conn.close()
    except Exception as e:
        print(f"Database creation failed: {e}")

ensure_database()

url = (
    f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
    f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
)
engine = create_engine(url, echo=False)
SessionLocal = sessionmaker(bind=engine)
