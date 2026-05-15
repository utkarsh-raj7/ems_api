 import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.common.config.config import settings

encoded_password = urllib.parse.quote_plus(settings.db_password)
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.db_user}:{encoded_password}@{settings.db_host}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=settings.db_pool_size)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()