# 🚀 Render + Neon PostgreSQL 배포 가이드

## 1. Neon PostgreSQL 설정

### 1.1 Neon 계정 생성 및 데이터베이스 생성

1. [Neon Console](https://console.neon.tech/) 접속
2. 새 프로젝트 생성
3. 데이터베이스 연결 정보 복사 (CONNECTION_STRING)

### 1.2 연결 문자열 예시

```
postgresql://username:password@host.neon.tech/database?sslmode=require
```

## 2. Render 배포 설정

### 2.1 필수 환경변수 (Render Environment Variables에 설정)

```bash
# 필수 - 관리자 비밀번호
ADMIN_PASSWORD=your_very_secure_admin_password

# 필수 - 환경 설정
ENVIRONMENT=production

# 필수 - Neon PostgreSQL 연결 문자열
DATABASE_URL=postgresql://username:password@host.neon.tech/database?sslmode=require

# 다락방별 순장 설정 (실제 이름으로 변경)
LEADERS_EUNHYE=실제순장1,실제순장2,실제순장3,실제순장4,실제순장5
LEADERS_HAPOOM=실제순장1,실제순장2,실제순장3,실제순장4,실제순장5
LEADERS_OJI=실제순장1,실제순장2,실제순장3,실제순장4,실제순장5
LEADERS_SOGEUM=실제순장1,실제순장2,실제순장3,실제순장4,실제순장5
LEADERS_NEW=실제순장1,실제순장2,실제순장3,실제순장4,실제순장5
```

### 2.2 Render 배포 순서

1. GitHub 리포지토리에 코드 푸시
2. Render 대시보드에서 "New Web Service" 선택
3. GitHub 리포지토리 연결
4. 환경변수 설정 (위의 필수 환경변수들)
5. 배포 시작

## 3. 첫 배포 후 확인사항

### 3.1 데이터베이스 테이블 생성 확인

- FastAPI가 시작되면 자동으로 테이블이 생성됩니다
- Neon Console에서 `prayers` 테이블 생성 확인

### 3.2 기능 테스트

1. 기도제목 등록 테스트
2. 관리자 로그인 테스트 (`/admin`)
3. 비공개 기도제목 기능 테스트
4. 엑셀 다운로드 기능 테스트

## 4. 보안 설정 확인

✅ HTTPS 자동 적용 (Render)
✅ 쿠키 Secure 플래그 자동 설정
✅ 관리자 인증 시스템
✅ 비공개 기도제목 접근 제어

## 5. 모니터링

### 5.1 Render 로그 모니터링

- Render 대시보드에서 실시간 로그 확인
- 오류 발생 시 이메일 알림 설정 가능

### 5.2 Neon 데이터베이스 모니터링

- Neon Console에서 연결 상태 및 사용량 확인
- 자동 백업 기능 활용

## 6. 문제 해결

### 6.1 데이터베이스 연결 오류

- `DATABASE_URL` 환경변수 확인
- Neon 데이터베이스 상태 확인
- 연결 문자열 형식 확인 (`postgresql://` 시작)

### 6.2 관리자 로그인 실패

- `ADMIN_PASSWORD` 환경변수 설정 확인
- 대소문자 및 특수문자 정확히 입력

### 6.3 순장 목록이 나오지 않음

- `LEADERS_*` 환경변수들 설정 확인
- 쉼표로 구분된 형식 확인
