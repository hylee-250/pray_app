#!/usr/bin/env python3
"""
네온 PostgreSQL 데이터베이스의 기도제목 데이터 확인 스크립트
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

load_dotenv()

def check_neon_data():
    """네온 DB의 기도제목 데이터 확인"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL이 설정되지 않았습니다.")
        print("네온 DB URL을 .env 파일에 추가해주세요.")
        return
    
    # PostgreSQL URL 변환
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"🔍 연결 중: {database_url[:50]}...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # 테이블 존재 확인
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'prayers';
            """))
            
            if not result.fetchone():
                print("❌ prayers 테이블이 존재하지 않습니다.")
                return
            
            # 전체 기도제목 수
            result = conn.execute(text("SELECT COUNT(*) as total FROM prayers;"))
            total_count = result.fetchone().total
            print(f"📊 전체 기도제목 수: {total_count}개")
            
            if total_count == 0:
                print("❗ 기도제목이 없습니다. 새로 등록해주세요.")
                return
            
            # 최근 기도제목들 (최근 10개)
            result = conn.execute(text("""
                SELECT id, name, leader, cell_group, 
                       LEFT(content, 50) as content_preview, 
                       created_at, is_private
                FROM prayers 
                ORDER BY created_at DESC 
                LIMIT 10;
            """))
            
            print("\n📋 최근 기도제목들 (최근 10개):")
            print("-" * 80)
            
            KST = pytz.timezone('Asia/Seoul')
            for row in result:
                # UTC를 KST로 변환
                if row.created_at.tzinfo is None:
                    # 타임존 정보가 없으면 UTC로 가정
                    created_kst = pytz.UTC.localize(row.created_at).astimezone(KST)
                else:
                    created_kst = row.created_at.astimezone(KST)
                
                privacy = "🔒" if row.is_private else "🌐"
                print(f"{privacy} [{row.id}] {row.name} ({row.leader}/{row.cell_group})")
                print(f"    {row.content_preview}...")
                print(f"    등록: {created_kst.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
            
            # 다락방별 통계
            result = conn.execute(text("""
                SELECT cell_group, COUNT(*) as count
                FROM prayers 
                GROUP BY cell_group 
                ORDER BY count DESC;
            """))
            
            print("\n📈 다락방별 기도제목 수:")
            for row in result:
                print(f"  {row.cell_group}: {row.count}개")
            
            # 순장별 통계
            result = conn.execute(text("""
                SELECT leader, COUNT(*) as count
                FROM prayers 
                GROUP BY leader 
                ORDER BY count DESC;
            """))
            
            print("\n👥 순장별 기도제목 수:")
            for row in result:
                print(f"  {row.leader}: {row.count}개")
            
            # 비공개/공개 비율
            result = conn.execute(text("""
                SELECT 
                    is_private,
                    COUNT(*) as count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM prayers), 1) as percentage
                FROM prayers 
                GROUP BY is_private;
            """))
            
            print("\n🔒 공개/비공개 비율:")
            for row in result:
                status = "비공개" if row.is_private else "공개"
                print(f"  {status}: {row.count}개 ({row.percentage}%)")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("1. 네온 DB URL이 올바른지 확인")
        print("2. 네트워크 연결 상태 확인")
        print("3. 네온 DB가 활성화되어 있는지 확인")
    
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🔍 네온 PostgreSQL 데이터 확인 도구")
    print("=" * 50)
    check_neon_data() 