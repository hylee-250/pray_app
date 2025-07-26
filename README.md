# 기도제목 관리 앱

FastAPI로 만든 기도제목 관리 웹 애플리케이션입니다.

## 기능

- 📝 기도제목 등록 (이름, 다락방, 순장, 기도제목)
- 📊 다락방/순장별 기도제목 조회
- 📅 일요일~토요일 주간 단위 필터링
- 📥 엑셀 다운로드 기능
- 🔄 다락방 선택 시 해당 순장 자동 필터링

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택사항)

#### 로컬 개발 (SQLite 사용)
```bash
# 기본값으로 SQLite 사용 (별도 설정 불필요)
```

#### PostgreSQL 사용 (권장)
```bash
# 환경변수 설정
export DATABASE_URL="postgresql://username:password@localhost:5432/prayers_db"
```

#### Render 배포 시
1. Render 대시보드에서 환경변수 설정
2. `DATABASE_URL`에 PostgreSQL 연결 문자열 입력
3. 예: `postgresql://user:password@host:port/database`

### 3. 애플리케이션 실행
```bash
uvicorn main:app --reload
```

## 데이터베이스 설정

### SQLite (기본값)
- 로컬 개발용
- 파일 기반 데이터베이스
- 별도 설정 불필요

### PostgreSQL (권장)
- 프로덕션 환경용
- Render 무료 티어 지원
- 데이터 영속성 보장

## API 엔드포인트

- `GET /`: 기도제목 등록 폼
- `POST /submit`: 기도제목 제출
- `GET /admin`: 관리자 페이지 (조회/필터링)
- `GET /export-excel`: 엑셀 다운로드

## 다락방 및 순장 설정

현재 설정된 다락방과 순장:
- 은혜다락방: 고영은, 김다빈, 송은설, 오지은, 이호영, 용민기, 최다열, 이용식
- 하품다락방: 하품1~8
- 오지다락방: 오지1~8
- 소금다락방: 소금1~8

## 배포 (Render)

1. GitHub 저장소 연결
2. 환경변수 설정:
   - `DATABASE_URL`: PostgreSQL 연결 문자열
3. 빌드 명령어: `pip install -r requirements.txt`
4. 시작 명령어: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 주의사항

⚠️ **중요**: SQLite를 사용할 경우 Render에서 앱이 재시작될 때마다 데이터가 초기화될 수 있습니다. 40명이 실제로 사용할 예정이라면 반드시 PostgreSQL을 사용하세요. 