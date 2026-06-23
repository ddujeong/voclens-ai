import os, json

from dotenv import load_dotenv
from google import genai


load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite"

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

        self.client = genai.Client(api_key=api_key)

    def generate_admin_answer(
        self,
        question: str,
        top_keyword: str,
        count: int,
        related_reviews: list[str],
    ) -> str:
        review_text = "\n".join(
            [f"- {review}" for review in related_reviews[:5]]
        )

        prompt = f"""
당신은 쇼핑몰 운영자를 돕는 VOC 분석 AI 에이전트입니다.

운영자의 질문:
{question}

분석 결과:
- 주요 불만 키워드: {top_keyword}
- 언급 횟수: {count}건

관련 리뷰:
{review_text}

답변 규칙:
1. 운영자가 바로 이해할 수 있게 요약합니다.
2. 고객 불만의 핵심 원인을 설명합니다.
3. 개선 우선순위를 제안합니다.
4. 과장하지 말고 제공된 리뷰 근거 안에서만 답변합니다.
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text
    
    def generate_rag_answer(
        self,
        question: str,
        related_reviews: list[str],
    ) -> str:

        review_text = "\n".join(
            [f"- {review}" for review in related_reviews]
        )

        prompt = f"""
    당신은 쇼핑몰 운영자를 위한 VOC 분석 AI 에이전트입니다.

    운영자 질문:
    {question}

    검색된 관련 리뷰:
    {review_text}

    답변 규칙:
    1. 리뷰를 근거로만 답변합니다.
    2. 핵심 불만 또는 만족 포인트를 요약합니다.
    3. 개선 우선순위를 제안합니다.
    4. 리뷰에 없는 내용은 추측하지 않습니다.
    """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text
    
    def analyze_review_sentiment(
        self,
        content: str,
    ) -> str:
        prompt = f"""
    다음 쇼핑몰 리뷰의 감성을 분류하세요.

    리뷰:
    {content}

    분류 기준:
    - positive: 만족, 장점, 긍정 평가
    - negative: 불만, 문제점, 개선 필요
    - neutral: 긍정과 부정이 섞이거나 판단이 애매함

    반드시 아래 셋 중 하나만 출력하세요.
    positive
    negative
    neutral
    """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        sentiment = response.text.strip().lower()

        if sentiment not in ["positive", "negative", "neutral"]:
            return "neutral"

        return sentiment
    
    def analyze_review_metadata(
        self,
        content: str,
    ) -> dict:
        prompt = f"""
다음 쇼핑몰 리뷰를 분석하세요.

리뷰:
{content}

분석 항목:
1. sentiment: positive, negative, neutral 중 하나
2. tags: 리뷰 핵심 키워드 1~3개

태그 예시:
배터리, 충전, 가격, 가성비, 배송, 포장, AS, 소음, 무게, 흡입력, 내구성, 디자인, 사용성

반드시 JSON만 출력하세요.

예시:
{{
"sentiment": "negative",
"tags": ["배터리", "충전"]
}}
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        try:
            raw_text = response.text.strip()

            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

            result = json.loads(raw_text)

            sentiment = result.get("sentiment", "neutral")
            tags = result.get("tags", [])

            if sentiment not in ["positive", "negative", "neutral"]:
                sentiment = "neutral"

            if not isinstance(tags, list):
                tags = []

            tags = [
                str(tag).strip()
                for tag in tags
                if str(tag).strip()
            ][:3]

            return {
                "sentiment": sentiment,
                "tags": tags,
            }

        except Exception:
            return {
                "sentiment": "neutral",
                "tags": [],
            }
    def generate_voc_report(
        self,
        question: str,
        reviews: str,
    ) -> str:
        prompt = f"""
        당신은 쇼핑몰 운영자를 위한 VOC 분석 전문가입니다.

        운영자 질문:
        {question}

        검색된 관련 리뷰:
        {reviews}

        아래 형식으로 답변하세요.

        ## 핵심 요약
        - 검색된 리뷰에서 공통적으로 확인되는 내용만 1~2문장으로 요약하세요.

        ## 주요 VOC
        - 여러 리뷰에서 반복 확인된 의견과 일부 리뷰에서만 확인된 의견을 구분하세요.
        - "공통 의견"이라는 표현은 모든 리뷰에 해당될 때만 사용하세요.
        - 일반적으로는 "반복 확인된 의견", "일부 의견"으로 표현하세요.

        ## 고객 영향
        - 리뷰 원문에 직접 드러난 착용 불편, 사용 빈도 저하, 만족도 저하만 작성하세요.
        - 반품, 교환, 재구매 저하, 브랜드 신뢰도 하락은 리뷰에 직접 언급된 경우에만 작성하세요.

        ## 개선 제안
        - 운영자가 바로 실행할 수 있는 개선안을 작성하세요.
        - 단, 리뷰에 없는 원인을 임의로 만들지 마세요.

        ## 근거 리뷰
        - 사용한 리뷰 원문을 3개 이내로 그대로 인용하세요.

        답변 규칙:
        1. 반드시 검색된 리뷰 내용만 근거로 답변하세요.
        2. 리뷰에 없는 내용은 추측하지 마세요.
        3. "대부분", "많음", "주요 원인" 같은 표현은 여러 리뷰에서 반복 확인될 때만 사용하세요.
        4. 한두 개 리뷰에서만 보이는 내용은 "일부 의견"으로 표현하세요.
        5. 질문의 의도와 다른 리뷰는 근거로 사용하지 마세요.
        6. 고객 영향은 리뷰 원문에 직접 드러난 행동이나 불편만 작성하세요.
        재구매, 반품, 교환, 브랜드 신뢰도 같은 표현은 리뷰에 직접 언급된 경우에만 사용하세요.
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text
    
    def generate_voc_comparison_report(
        self,
        question: str,
        positive_reviews: list[str],
        negative_reviews: list[str],
    ) -> str:
        positive_text = "\n".join(
            f"- {review}"
            for review in positive_reviews
        )

        negative_text = "\n".join(
            f"- {review}"
            for review in negative_reviews
        )

        prompt = f"""
당신은 쇼핑몰 운영자를 위한 VOC 분석 전문가입니다.

운영자 질문:
{question}

긍정 리뷰:
{positive_text}

부정 리뷰:
{negative_text}

아래 형식으로 답변하세요.

## 긍정 의견
- 긍정 리뷰에서 반복 확인되는 만족 포인트를 요약하세요.

## 부정 의견
- 부정 리뷰에서 반복 확인되는 불만 포인트를 요약하세요.

## 종합 분석
- 긍정과 부정 의견을 비교하여 운영자가 봐야 할 핵심 인사이트를 정리하세요.

## 개선 제안
- 부정 의견을 줄이고 긍정 의견을 강화할 수 있는 실행 방안을 제안하세요.

## 근거 리뷰
- 긍정 리뷰 2개, 부정 리뷰 2개 이내로 원문을 그대로 인용하세요.

답변 규칙:
1. 반드시 제공된 리뷰 내용만 근거로 답변하세요.
2. 리뷰에 없는 내용은 추측하지 마세요.
3. "대부분", "많음", "주요 원인" 같은 표현은 여러 리뷰에서 반복 확인될 때만 사용하세요.
4. 긍정 리뷰와 부정 리뷰를 섞어서 판단하지 말고 구분해서 분석하세요.
5. 리뷰가 없는 영역은 "제공된 리뷰에서는 확인되지 않습니다"라고 작성하세요.
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text