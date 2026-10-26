# BuildLog 개발 계획 (FastAPI + React + Supabase)

## 1. 계획의 목적

이 문서는 `spec.md`에 정한 기능을 어떤 순서로 개발할지 설명합니다.

처음 개발하는 과정에서 한 번에 너무 많은 내용을 다루지 않도록 작업을 작은 Phase로 나눕니다. 한 번의 작업에서는 Phase 하나만 진행하고, 확인 기준을 모두 통과한 뒤 다음 Phase로 넘어갑니다.

## 2. 기술 스택

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python/FastAPI (REST API with auto-generated Swagger docs)
- **Database**: 
  - Development/Test: SQLite3 (로컬 파일 기반, `database.db`)
  - Production: Supabase (PostgreSQL + Auth 포함)
- **Authentication**: JWT tokens (Supabase Auth 또는 커스텀)
- **API 문서**: Swagger UI (FastAPI 자동 생성)

## 3. 개발 원칙

- `spec.md`에 없는 기능은 추가하지 않습니다.
- Backend (FastAPI)와 Frontend (React)를 분리하여 독립적으로 개발합니다.
- 각 Phase가 끝날 때 자동 테스트와 수동 테스트를 함께 수행합니다.
- 화면에서 버튼을 숨기는 것만으로 권한을 처리하지 않습니다. 서버에서도 사용 권한을 검사합니다.
- 비밀번호와 비밀 설정값을 코드에 저장하거나 화면에 보여주지 않습니다.
- `.env`, `.venv`, 로그와 생성 파일은 Git 기록 대상에서 제외합니다.
- Git 초기화와 커밋은 별도 요청이 있기 전까지 수행하지 않습니다.

## 4. 예정된 프로젝트 구조

```
buildlog/
├─ backend/                      # FastAPI 백엔드
│  ├─ main.py                   # FastAPI 메인 앱
│  ├─ requirements.txt           # Python 의존성
│  ├─ .env.example              # 환경 변수 예시
│  ├─ .env                       # 실제 환경 변수 (Git 제외)
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ core/                  # 설정, 보안, DB
│  │  ├─ models/                # SQLAlchemy 모델
│  │  ├─ schemas/               # Pydantic 스키마
│  │  ├─ api/
│  │  │  ├─ auth.py            # 회원가입, 로그인
│  │  │  ├─ study_records.py   # 공부 기록 API
│  │  │  ├─ todos.py           # 할 일 API
│  │  │  ├─ error_records.py   # 오류 기록 API
│  │  │  ├─ comments.py        # 댓글 API
│  │  │  ├─ likes.py           # 좋아요 API
│  │  │  ├─ reports.py         # 신고 API
│  │  │  └─ public.py          # 공개 기록 API
│  │  ├─ database.py            # DB 연결
│  │  └─ utils/                 # 공통 유틸리티
│  └─ database.db               # SQLite (개발용, Git 제외)
│
├─ frontend/                      # React 프론트엔드
│  ├─ src/
│  │  ├─ main.tsx
│  │  ├─ App.tsx
│  │  ├─ index.css
│  │  ├─ components/            # 재사용 가능한 컴포넌트
│  │  ├─ pages/                 # 페이지 컴포넌트
│  │  │  ├─ LoginPage.tsx
│  │  │  ├─ SignupPage.tsx
│  │  │  ├─ HomePage.tsx
│  │  │  ├─ StudyRecordsPage.tsx
│  │  │  ├─ TodosPage.tsx
│  │  │  ├─ ErrorRecordsPage.tsx
│  │  │  ├─ PublicRecordsPage.tsx
│  │  │  └─ SettingsPage.tsx
│  │  ├─ services/              # API 호출 함수
│  │  │  └─ api.ts
│  │  ├─ hooks/                 # 커스텀 훅
│  │  ├─ context/               # React Context (인증 상태)
│  │  └─ utils/                 # 공통 유틸리티
│  ├─ package.json
│  ├─ vite.config.ts
│  └─ .env.example
│
└─ docs/
   ├─ README.md
   ├─ mvp.md
   ├─ prd.md
   ├─ spec.md
   ├─ plan.md
   └─ setup.md (필요 시)
```

## 5. 전체 개발 순서

| Phase | 영역 | 목표 | 확인 방법 |
|-------|------|------|---------|
| **0** | 환경 | 개발 환경 확인 및 구성 | Python, Node.js, pip, npm 동작 확인 |
| **1** | Backend | FastAPI 뼈대 구성 | `http://localhost:8000/docs` Swagger UI 접근 가능 |
| **2** | Backend | 데이터베이스 + 모델 설정 | SQLite3 연결, SQLAlchemy 모델 마이그레이션 |
| **3** | Backend | 회원가입/로그인/닉네임 | 인증 API 테스트 통과 |
| **4** | Frontend | React 뼈대 + 라우팅 | React 앱 실행, 페이지 네비게이션 동작 |
| **5** | Frontend | 로그인/회원가입 화면 | 폼 검증, API 호출 성공 |
| **6** | Backend | 공부 기록 CRUD API | `/api/study-records` 엔드포인트 테스트 |
| **7** | Frontend | 공부 기록 목록/상세/작성 | 화면에서 CRUD 동작 |
| **8** | Backend | 할 일 & 오류 기록 API | `/api/todos`, `/api/error-records` 테스트 |
| **9** | Frontend | 할 일 & 오류 기록 UI | 목록, 필터, 작성/수정/삭제 동작 |
| **10** | Backend | 검색 API | `/api/search` 엔드포인트 테스트 |
| **11** | Frontend | 검색 기능 | 검색 입력 및 결과 표시 동작 |
| **12** | Backend | 공개 기록 & 댓글 & 좋아요 API | 권한 검사 포함 테스트 |
| **13** | Frontend | 공개 기록 브라우징 및 상호작용 | 댓글 작성, 좋아요, 신고 동작 |
| **14** | Backend | 신고 시스템 | 신고 저장 및 중복 방지 테스트 |
| **15** | Frontend | 반응형 디자인 & 폴리싱 | 360px+ 화면에서 UI 동작 확인 |
| **16** | 전체 | 통합 테스트 & 버그 수정 | `spec.md` 완료 조건 전체 통과 |

## 6. Phase별 상세 계획

### Phase 0: 개발 환경 확인

**목표**: 개발을 시작하기 전에 필요한 모든 도구가 설치되어 있는지 확인

**작업 목록**:
- [ ] Python 3.9+ 설치 확인
- [ ] Node.js 16+ 설치 확인
- [ ] pip 및 npm 최신 버전 확인
- [ ] Git 설정 확인
- [ ] 프로젝트 폴더 구조 생성
- [ ] `.env.example` 파일 생성 (실제 `.env`는 제외)
- [ ] 기술 스택 문서화

**확인 기준**:
- Python, Node.js 모두 실행 가능
- 프로젝트 폴더 구조 완성
- 개발 시작 가능 상태

---

### Phase 1: FastAPI 뼈대 구성

**목표**: FastAPI 프로젝트 초기화 및 기본 설정

**작업 목록**:
- [ ] FastAPI 프로젝트 구조 생성
- [ ] `requirements.txt` 작성 (FastAPI, SQLAlchemy, python-multipart 등)
- [ ] 기본 `main.py` 작성
- [ ] CORS 설정 (React 개발 서버와 연결)
- [ ] SQLite3 데이터베이스 연결 설정
- [ ] Swagger UI 접근 가능한지 확인

**필요한 패키지**:
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

**확인 기준**:
- `uvicorn main:app --reload` 실행 가능
- `http://localhost:8000/docs` Swagger UI 접근 가능
- CORS 설정으로 React에서 API 호출 가능

---

### Phase 2: 데이터베이스 & 모델 설정

**목표**: SQLAlchemy 모델 정의 및 데이터베이스 마이그레이션 (또는 초기화)

**작업 목록**:
- [ ] SQLAlchemy ORM 설정
- [ ] User 모델 정의 (이메일, 비밀번호 해시, 닉네임)
- [ ] StudyRecord, TodoItem, ErrorRecord 모델 정의
- [ ] Comment, Like, Report 모델 정의
- [ ] 모델 간 관계(foreign key) 설정
- [ ] Unique 제약조건, 기본값 설정
- [ ] 데이터베이스 테이블 초기화
- [ ] 모델 테스트

**확인 기준**:
- SQLite3 데이터베이스 파일 생성
- 모든 테이블 생성 확인
- 모델 제약조건 동작 확인

---

### Phase 3: 회원가입/로그인/닉네임

**목표**: 사용자 인증 시스템 구현

**Backend 작업**:
- [ ] JWT 토큰 생성/검증 로직
- [ ] 비밀번호 해싱 (bcrypt)
- [ ] `POST /api/auth/signup` (회원가입)
- [ ] `POST /api/auth/login` (로그인)
- [ ] `POST /api/auth/logout` (로그아웃)
- [ ] `PUT /api/account/nickname` (닉네임 변경)
- [ ] `GET /api/account/info` (사용자 정보)
- [ ] 인증 미들웨어/디펜던시

**Frontend 작업**:
- [ ] React 라우팅 설정
- [ ] 로그인 페이지
- [ ] 회원가입 페이지
- [ ] 홈 페이지 (로그인 후)
- [ ] 계정 설정 페이지
- [ ] 로그인 상태 Context 설정

**확인 기준**:
- 회원가입/로그인 API 테스트 통과
- 토큰 저장 및 API 요청 시 헤더에 포함
- 무효한 토큰으로 요청 시 401 Unauthorized
- 닉네임 변경 후 새 토큰 발급

---

### Phase 4-9: 기록 기능 (공부기록, 할일, 오류기록)

각 단계에서:
- Backend: CRUD API 엔드포인트
- Frontend: 목록, 작성, 수정, 삭제 UI

**확인 기준**:
- 전체 CRUD 동작
- 권한 검사 (작성자만 수정/삭제)
- 모든 필드 검증

---

### Phase 10-14: 공개 기능 (검색, 공개 기록, 댓글, 좋아요, 신고)

**확인 기준**:
- 공개 기록만 다른 사용자에게 표시
- 댓글/좋아요 권한 검사
- 신고 중복 방지

---

### Phase 15: 반응형 디자인 & 폴리싱

**작업**:
- [ ] 360px 이상 화면에서 테스트
- [ ] 모바일 UI 개선
- [ ] 에러 메시지 개선
- [ ] 로딩 상태 표시

---

### Phase 16: 통합 테스트 & 버그 수정

**작업**:
- [ ] 전체 사용자 흐름 테스트
- [ ] Chrome, Edge, Safari 최신 버전 테스트
- [ ] 모바일 테스트
- [ ] 권한 검사 재확인
- [ ] 버그 수정 및 최적화

---

## 7. 개발 시작 전 확인사항

다음을 반드시 확인해주세요:

1. **Python 버전**: 3.9 이상?
2. **Node.js 버전**: 16 이상?
3. **개발 데이터베이스**: SQLite3로 진행?
4. **프로덕션 DB**: Supabase 계정 준비 (나중에)?
5. **추가 설정**: 특별히 필요한 것이 있나요?

모든 확인이 완료되면 **Phase 0**부터 시작하겠습니다!
