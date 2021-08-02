import asyncio
from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}/{settings.DB_NAME}?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

session_lock = asyncio.Lock()
