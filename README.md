# VOCLens AI

쇼핑몰 리뷰 데이터를 분석하여 고객의 불만사항, 만족 포인트, 개선 우선순위를 도출하는 AI 기반 VOC(Voice of Customer) 분석 서비스입니다.

운영자는 대시보드를 통해 리뷰 현황을 확인하고, AI 챗봇을 이용해 자연어로 고객 의견을 분석하고 상품별 VOC를 탐색할 수 있습니다.

AI 기반 리뷰 감성 분석과 태그 추출을 통해 리뷰를 자동 분류하고, 운영자의 질문을 의도·카테고리·태그로 해석한 뒤 Vector Search(RAG)를 활용하여 관련 VOC를 검색하고 분석 결과를 제공합니다.

---

## 프로젝트 목표

* 사용자 리뷰 수집 및 관리
* 리뷰 기반 VOC 자동 분석
* 관리자 대시보드 제공
* AI 기반 자연어 VOC 검색
* 상품별 VOC 분석 및 개선 인사이트 제공

---

## 주요 기능

### 사용자

* 상품 목록 조회
* 상품 상세 조회
* 리뷰 작성
* AI 감성 분석이 적용된 리뷰 저장

### 관리자

#### KPI Dashboard

* 전체 리뷰 수
* 긍정 / 부정 / 중립 비율
* VOC TOP 키워드 시각화
* 감성 분포 차트
* 부정 리뷰 TOP 상품

#### VOC Search

* 키워드 기반 리뷰 검색
* 카테고리별 VOC 분석
* 상품별 VOC 분석
* 위험 상품 추천

### AI

* 리뷰 감성 분석
* 리뷰 태그 추출
* Vector Search 기반 RAG
* 운영자 AI 챗봇
* VOC 요약
* 개선 우선순위 제안

---

## 시스템 아키텍처

```text
Frontend (Next.js)
        ↓
Backend (FastAPI)
        ↓
──────────────────────────
│ Dashboard Service      │
│ Review Service         │
│ AI Chat Service        │
│ RAG Service            │
──────────────────────────
        ↓
PostgreSQL + pgvector
        ↓
Review / Embedding Storage
```

---

## RAG Pipeline

```text
리뷰 작성
        ↓
감성 분석 + 태그 추출
        ↓
Embedding 생성
        ↓
PostgreSQL(pgvector) 저장

운영자 질문
        ↓
질문 의도 분석
        ↓
카테고리 / 태그 추론
        ↓
Vector Search
        ↓
관련 리뷰 검색
        ↓
Gemini
        ↓
VOC 분석 리포트 생성
```

---

## 기술 스택

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Recharts
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
* Vector Search
* RAG
* TF-IDF
* Logistic Regression
* ABSA

---

## 개발 순서

* [x] 상품/리뷰 API
* [x] 리뷰 작성
* [x] 리뷰 감성 분석
* [x] 리뷰 태그 추출
* [x] 관리자 대시보드
* [x] KPI 시각화
* [x] VOC 키워드 분석
* [x] 감성 분포 차트
* [x] 부정 리뷰 TOP 상품
* [x] 리뷰 검색
* [x] pgvector 연동
* [x] 리뷰 임베딩 저장
* [x] Vector Search
* [x] RAG 기반 VOC 검색
* [x] 운영자 AI 챗봇
* [x] 상품별 VOC 분석
* [x] 위험 상품 추천

---

## 향후 개선 계획

* Hybrid Search(BM25 + Vector Search)
* 기간별 VOC 트렌드 분석
* 관리자 리포트 PDF 생성
* AI 개선 우선순위 자동 산출
* 상품별 VOC 리포트 자동 생성
* 실시간 리뷰 스트리밍
* AI Agent 기반 운영 자동화
