# 기도제목 관리 시스템 🙏

40명이 사용하는 기도제목 등록 및 관리 시스템입니다.

## 🚀 주요 기능

- **기도제목 등록**: 이름, 다락방, 순장, 기도제목 입력
- **관리자 페이지**: 기도제목 조회, 필터링, 수정, 삭제
- **엑셀 내보내기**: 필터링된 결과를 엑셀 파일로 다운로드
- **주차별 관리**: 일요일~토요일 기준으로 주차별 조회
- **다락방별 분류**: 다락방 > 순장 > 순원 순서로 계층적 표시

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택사항)

#### 로컬 개발 (SQLite 사용)
```bash
# 기본값으로 SQLite 사용
python main.py
```

#### PostgreSQL 사용
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
python main.py
```

#### Render 배포 시
```bash
# Render 대시보드에서 환경변수 설정
DATABASE_URL=postgresql://username:password@host:5432/dbname
```

### 3. 애플리케이션 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🗄️ 데이터베이스 설정

### SQLite (기본값)
- 파일 기반 데이터베이스
- 개발 및 테스트용으로 적합
- **주의**: Render에서 SQLite 사용 시 데이터가 초기화될 수 있음

### PostgreSQL (권장)
- 프로덕션 환경에 적합
- 데이터 영속성 보장
- Render에서 안정적으로 동작

## 🔧 API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 기도제목 등록 페이지 |
| POST | `/submit` | 기도제목 등록 |
| GET | `/admin` | 관리자 페이지 |
| GET | `/export-excel` | 엑셀 다운로드 |
| DELETE | `/prayer/{id}` | 기도제목 삭제 |
| PUT | `/prayer/{id}` | 기도제목 수정 |

## 🏠 다락방/순장 설정

시스템에서 사용하는 다락방과 순장 정보는 `main.py`의 `CELL_GROUP_LEADERS` 딕셔너리에서 관리됩니다:

```python
CELL_GROUP_LEADERS = {
    "다락방1": ["순장1", "순장2", "순장3"],
    "다락방2": ["순장4", "순장5", "순장6"],
    # ... 추가 다락방들
}
```

## 🚀 Render 배포

### 1. Render 대시보드에서 새 Web Service 생성

### 2. GitHub 저장소 연결

### 3. 환경변수 설정
```
DATABASE_URL=postgresql://username:password@host:5432/dbname
```

### 4. 빌드 명령어
```bash
chmod +x build.sh
./build.sh
```

또는 Render 대시보드에서 빌드 명령어를 `./build.sh`로 설정

### 5. 시작 명령어
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## ⚠️ 주의사항

### SQLAlchemy 버전 문제 해결
Render 배포 시 다음과 같은 오류가 발생할 수 있습니다:
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes {'__static_attributes__', '__firstlineno__'}.
```

**해결 방법:**
1. `requirements.txt`에서 SQLAlchemy 버전을 2.0.19로 고정
2. `typing-extensions==4.8.0` 추가
3. `runtime.txt`에 Python 3.11.7 명시

### 데이터베이스 선택
- **개발/테스트**: SQLite 사용 (간편함)
- **프로덕션**: PostgreSQL 사용 (안정성)

## 📁 프로젝트 구조

```
pray_app/
├── main.py              # FastAPI 애플리케이션
├── models.py            # SQLAlchemy 모델
├── database.py          # 데이터베이스 설정
├── requirements.txt     # Python 의존성
├── runtime.txt         # Python 버전
├── templates/          # HTML 템플릿
│   ├── form.html       # 기도제목 등록 페이지
│   └── admin.html      # 관리자 페이지
└── static/            # 정적 파일 (Excel 다운로드)
```

## 🎨 UI/UX 특징

- **현대적인 디자인**: 그라데이션 배경과 카드형 레이아웃
- **반응형 웹**: 모바일과 데스크톱 모두 지원
- **직관적인 인터페이스**: 사용자 친화적인 폼과 버튼
- **동적 필터링**: 다락방 선택 시 해당 순장만 표시
- **실시간 업데이트**: 수정/삭제 시 페이지 자동 새로고침

## 🔄 업데이트 내역

- ✅ 기도제목 등록 기능
- ✅ 관리자 페이지 (조회, 필터링)
- ✅ 엑셀 내보내기 기능
- ✅ 주차별 관리 기능
- ✅ 수정/삭제 기능
- ✅ PostgreSQL 지원
- ✅ 현대적인 UI/UX 디자인
- ✅ SQLAlchemy 버전 호환성 문제 해결 