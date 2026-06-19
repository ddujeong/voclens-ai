# VOCLens AI

쇼핑몰 리뷰 데이터를 분석하여 고객의 불만사항, 만족 포인트, 개선 우선순위를 도출하는 AI 기반 VOC 분석 서비스

## 프로젝트 목표

- 사용자 리뷰 데이터 수집
- 리뷰 통계 시각화
- VOC 분석
- 리뷰 기반 RAG 검색
- AI 운영자 챗봇 구현

## MVP

### 사용자

- 상품 목록 조회
- 상품 상세 조회
- 리뷰 작성

### 관리자

- KPI 대시보드
- VOC 분석
- 리뷰 검색

### AI

- 리뷰 기반 RAG
- 운영자 챗봇

## 기술 스택

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Shadcn UI

### Backend

- FastAPI
- SQLAlchemy
- Pydantic

### Database

- PostgreSQL
- pgvector

### AI

- Gemini
- Embedding
- RAG

## 개발 순서

- [x] 프로젝트 초기 설정
- [x] FastAPI 서버 구성
- [ ] PostgreSQL 구성
- [ ] Product 모델
- [ ] Review 모델
- [ ] Seed 데이터
- [ ] 상품 API
- [ ] 리뷰 API
- [ ] 관리자 대시보드
- [ ] RAG
- [ ] AI 챗봇