#!/usr/bin/env python3
"""
네온 PostgreSQL 데이터베이스 마이그레이션 스크립트
is_private 컬럼을 안전하게 추가합니다.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    """데이터베이스에 is_private 컬럼 추가"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL이 설정되지 않았습니다.")
        return False
    
    # PostgreSQL URL 변환
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"🔍 네온 DB 연결 중...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # 먼저 테이블 존재 확인
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'prayers';
            """))
            
            if not result.fetchone():
                print("❌ prayers 테이블이 존재하지 않습니다.")
                return False
            
            # is_private 컬럼이 이미 존재하는지 확인
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'prayers' AND column_name = 'is_private';
            """))
            
            if result.fetchone():
                print("✅ is_private 컬럼이 이미 존재합니다.")
                return True
            
            print("🔧 is_private 컬럼을 추가하는 중...")
            
            # is_private 컬럼 추가 (기본값: false)
            conn.execute(text("""
                ALTER TABLE prayers 
                ADD COLUMN is_private BOOLEAN DEFAULT FALSE NOT NULL;
            """))
            
            # 인덱스 추가
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_prayers_is_private 
                ON prayers (is_private);
            """))
            
            conn.commit()
            
            # 컬럼 추가 확인
            result = conn.execute(text("""
                SELECT COUNT(*) as total FROM prayers;
            """))
            total_count = result.fetchone().total
            
            print(f"✅ is_private 컬럼이 성공적으로 추가되었습니다!")
            print(f"📊 기존 기도제목 {total_count}개가 모두 공개로 설정되었습니다.")
            
            return True
            
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        return False
    
    finally:
        engine.dispose()

def verify_migration():
    """마이그레이션 검증"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        return False
    
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # 테이블 구조 확인
            result = conn.execute(text("""
                SELECT column_name, data_type, column_default, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'prayers' 
                ORDER BY ordinal_position;
            """))
            
            print("\n📋 현재 prayers 테이블 구조:")
            print("-" * 60)
            for row in result:
                nullable = "NULL" if row.is_nullable == "YES" else "NOT NULL"
                default = f"DEFAULT {row.column_default}" if row.column_default else ""
                print(f"  {row.column_name:<12} {row.data_type:<20} {nullable} {default}")
            
            # 샘플 데이터 조회
            result = conn.execute(text("""
                SELECT name, is_private, created_at 
                FROM prayers 
                ORDER BY created_at DESC 
                LIMIT 3;
            """))
            
            print("\n📊 샘플 데이터:")
            print("-" * 60)
            for row in result:
                privacy = "🔒 비공개" if row.is_private else "🌐 공개"
                print(f"  {row.name}: {privacy}")
            
            return True
            
    except Exception as e:
        print(f"❌ 검증 중 오류: {e}")
        return False
    
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🚀 네온 PostgreSQL 데이터베이스 마이그레이션")
    print("=" * 50)
    
    if migrate_database():
        print("\n🔍 마이그레이션 검증 중...")
        verify_migration()
        print("\n✅ 마이그레이션이 성공적으로 완료되었습니다!")
        print("이제 애플리케이션이 정상적으로 작동할 것입니다.")
    else:
        print("\n❌ 마이그레이션에 실패했습니다.")
        print("네온 DB 연결 상태를 확인해주세요.") 