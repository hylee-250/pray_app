from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경변수에서 DATABASE_URL을 가져오고, 없으면 SQLite 사용
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prayers.db")

# Render에서 PostgreSQL URL이 postgres://로 시작하면 postgresql://로 변경
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite인 경우 connect_args 추가, PostgreSQL인 경우 연결 풀 설정
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL용 연결 풀 설정 (Neon에 최적화)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # 연결 상태 확인
        pool_recycle=3600,   # 1시간마다 연결 재생성
        pool_size=5,         # 기본 연결 풀 크기
        max_overflow=10,     # 추가 연결 허용
        echo=False           # SQL 로그 비활성화 (배포환경)
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
