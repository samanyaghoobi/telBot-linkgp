from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import MYSQL_CONFIG

url = (
    f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
    f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
)
engine = create_engine(url, echo=False)
SessionLocal = sessionmaker(bind=engine)
