from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경변수에서 DATABASE_URL을 가져오고, 없으면 SQLite 사용
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prayers.db")

# Render에서 PostgreSQL URL이 postgres://로 시작하면 postgresql://로 변경
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite인 경우 connect_args 추가, PostgreSQL인 경우 asyncpg 사용
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL인 경우 asyncpg 드라이버 사용
    if "postgresql://" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
