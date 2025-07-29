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
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=3,         # SQLite도 풀링 적용
        max_overflow=5,      # 무료 서버 고려하여 작게
        pool_pre_ping=True,  # 연결 상태 확인
        pool_recycle=1800,   # 30분마다 재생성
        echo=False
    )
else:
    # PostgreSQL용 연결 풀 설정 (무료 서버에 최적화)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # 연결 상태 확인 (끊어진 연결 자동 감지)
        pool_recycle=1800,   # 30분마다 연결 재생성 (무료 DB 타임아웃 대비)
        pool_size=3,         # 기본 연결 풀 크기 (무료 서버 고려)
        max_overflow=7,      # 추가 연결 허용 (총 10개까지)
        echo=False,          # SQL 로그 비활성화 (배포환경)
        pool_timeout=30,     # 연결 대기 시간 (30초)
        pool_reset_on_return='commit'  # 연결 반환 시 커밋
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
