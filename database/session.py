from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import MYSQL_CONFIG

url = (
    f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
    f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
)
engine = create_engine(
    url,
    echo=False,
    pool_size=20,           # تعداد کانکشن‌های فعال همزمان
    max_overflow=10,        # تعداد کانکشن‌های اضافی در مواقع نیاز
    pool_timeout=30,        # زمان انتظار برای دریافت کانکشن (ثانیه)
    pool_recycle=1800,      # زمان بازیابی کانکشن (ثانیه)، برای جلوگیری از قطع شدن کانکشن‌های قدیمی
    pool_pre_ping=True      # بررسی سلامت کانکشن قبل از استفاده
)
SessionLocal = sessionmaker(bind=engine)
