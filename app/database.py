from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_CONFIG
import logging
logger = logging.getLogger("uvicorn")

sqlalchemy_url_format = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
SQLALCHEMY_DATABASE_URL = sqlalchemy_url_format.format(**DATABASE_CONFIG)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size = 50,
    max_overflow = 50,
    pool_recycle = 3600,
    pool_timeout = 3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_mysql_database_if_not_exists(url = SQLALCHEMY_DATABASE_URL):
    url_no_db = "/".join(url.split('/')[:-1])
    db_name = url.split('/')[-1]
    engine_no_db = create_engine(url_no_db)
    with engine_no_db.connect() as conn:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    logger.info("Create database success.")
    
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

