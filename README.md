# VOCLens AI

쇼핑몰 리뷰 데이터를 분석하여 고객의 불만사항, 만족 포인트, 개선 우선순위를 도출하는 AI 기반 VOC(Voice of Customer) 분석 서비스입니다.

운영자는 대시보드를 통해 리뷰 현황을 확인하고, AI 챗봇을 통해 고객 의견을 자연어로 분석할 수 있습니다.

---

## 프로젝트 목표

* 사용자 리뷰 데이터 수집
* 리뷰 통계 시각화
* VOC 분석
* 리뷰 기반 RAG 검색
* AI 운영자 챗봇 구현

---

## 주요 기능

### 사용자

* 상품 목록 조회
* 상품 상세 조회
* 리뷰 작성

### 관리자

* KPI 대시보드

  * 전체 리뷰 수
  * 긍정/부정/중립 리뷰 수
  * 감성 비율 분석

* VOC 분석

  * 리뷰 감성 분류
  * 고객 불만 키워드 분석

* 리뷰 검색

  * 키워드 기반 리뷰 검색
  * 관련 리뷰 탐색

### AI

* 리뷰 기반 RAG 검색
* 운영자 챗봇
* 고객 불만 원인 분석
* 개선 우선순위 제안

---

## 시스템 아키텍처

```text
Frontend (Next.js)
        ↓
Backend (FastAPI)
        ↓
PostgreSQL
        ↓
Review Storage
```

### RAG Pipeline

```text
리뷰 작성
        ↓
Embedding 생성
        ↓
pgvector 저장

운영자 질문
        ↓
Embedding 생성
        ↓
Vector Similarity Search
        ↓
Top-K Review Retrieval
        ↓
Gemini
        ↓
VOC 분석 답변 생성
```

---

## 기술 스택

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* React Markdown

### Backend

* FastAPI
* SQLAlchemy
* Pydantic

### Database

* PostgreSQL
* pgvector

### AI

* Gemini 3.1 Flash Lite
* Sentence Transformers
* paraphrase-multilingual-MiniLM-L12-v2
* RAG (Retrieval-Augmented Generation)

---

## 개발 순서

* [x] 프로젝트 초기 설정
* [x] FastAPI 서버 구성
* [x] PostgreSQL 구성
* [x] Product 모델
* [x] Review 모델
* [x] Seed 데이터
* [x] 상품 API
* [x] 리뷰 API
* [x] 관리자 대시보드
* [x] 리뷰 검색
* [x] pgvector 연동
* [x] 리뷰 임베딩 저장
* [x] Vector Similarity Search
* [x] 리뷰 기반 RAG
* [x] AI 챗봇

---

## 향후 개선 계획

* 리뷰 데이터 1000건 이상 확장
* 하이브리드 검색(BM25 + Vector Search) 적용
* 감성 분석 모델 고도화
* 상품별 VOC 자동 리포트 생성
* 실시간 리뷰 수집 파이프라인 구축
* 관리자 AI Agent 기능 확장
