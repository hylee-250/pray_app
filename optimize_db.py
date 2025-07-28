#!/usr/bin/env python3
"""
PostgreSQL 데이터베이스 최적화 스크립트
배포 후 한 번 실행하여 성능을 최적화합니다.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def optimize_postgresql():
    """PostgreSQL 데이터베이스 최적화"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url or not database_url.startswith("postgresql"):
        print("PostgreSQL 데이터베이스가 아니거나 DATABASE_URL이 설정되지 않았습니다.")
        return
    
    engine = create_engine(database_url)
    
    optimization_queries = [
        # 복합 인덱스 생성 (주간 기도제목 조회 최적화)
        """
        CREATE INDEX IF NOT EXISTS idx_prayers_week_query 
        ON prayers (created_at DESC, is_private, cell_group, leader);
        """,
        
        # 관리자 페이지 조회 최적화
        """
        CREATE INDEX IF NOT EXISTS idx_prayers_admin_query 
        ON prayers (created_at DESC, cell_group, leader);
        """,
        
        # 통계 쿼리 최적화
        """
        CREATE INDEX IF NOT EXISTS idx_prayers_stats 
        ON prayers (cell_group, leader, is_private);
        """,
        
        # 파티션된 인덱스 (최근 데이터 우선)
        """
        CREATE INDEX IF NOT EXISTS idx_prayers_recent 
        ON prayers (created_at DESC) 
        WHERE created_at > NOW() - INTERVAL '30 days';
        """
    ]
    
    try:
        with engine.connect() as conn:
            print("PostgreSQL 성능 최적화를 시작합니다...")
            
            for i, query in enumerate(optimization_queries, 1):
                print(f"최적화 단계 {i}/{len(optimization_queries)} 실행 중...")
                conn.execute(text(query))
                conn.commit()
            
            # 테이블 통계 업데이트
            print("테이블 통계를 업데이트하는 중...")
            conn.execute(text("ANALYZE prayers;"))
            conn.commit()
            
            print("✅ PostgreSQL 최적화가 완료되었습니다!")
            
    except Exception as e:
        print(f"❌ 최적화 중 오류 발생: {e}")
    finally:
        engine.dispose()

def check_database_performance():
    """데이터베이스 성능 체크"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url or not database_url.startswith("postgresql"):
        return
    
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("\n📊 데이터베이스 성능 체크:")
            
            # 인덱스 사용 현황 체크
            result = conn.execute(text("""
                SELECT schemaname, tablename, attname, n_distinct, correlation
                FROM pg_stats 
                WHERE tablename = 'prayers' 
                ORDER BY n_distinct DESC;
            """))
            
            print("\n인덱스 후보 컬럼들:")
            for row in result:
                print(f"  {row.attname}: 고유값 {row.n_distinct}, 상관관계 {row.correlation}")
            
            # 테이블 크기 확인
            result = conn.execute(text("""
                SELECT 
                    pg_size_pretty(pg_total_relation_size('prayers')) as total_size,
                    pg_size_pretty(pg_relation_size('prayers')) as table_size,
                    pg_size_pretty(pg_total_relation_size('prayers') - pg_relation_size('prayers')) as index_size;
            """))
            
            row = result.fetchone()
            print(f"\n테이블 크기:")
            print(f"  전체: {row.total_size}")
            print(f"  테이블: {row.table_size}")
            print(f"  인덱스: {row.index_size}")
            
    except Exception as e:
        print(f"성능 체크 중 오류: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🚀 PostgreSQL 데이터베이스 최적화 도구")
    print("=" * 50)
    
    optimize_postgresql()
    check_database_performance()
    
    print("\n배포 후 이 스크립트를 한 번 실행하면 성능이 향상됩니다.")
    print("사용법: python optimize_db.py") 