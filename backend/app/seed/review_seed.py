from app.models.review import Review


def seed_reviews(db):
    reviews = [
        Review(product_id=1, rating=5, content="흡입력이 강하고 먼지 제거가 잘 됩니다.", sentiment="positive"),
        Review(product_id=1, rating=2, content="배터리가 너무 빨리 닳아서 불편합니다.", sentiment="negative"),
        Review(product_id=1, rating=3, content="성능은 괜찮지만 무게가 조금 무겁습니다.", sentiment="neutral"),

        Review(product_id=2, rating=5, content="디자인이 예쁘고 소음이 적어서 만족합니다.", sentiment="positive"),
        Review(product_id=2, rating=2, content="가격이 비싸고 AS 응대가 아쉬웠습니다.", sentiment="negative"),
        Review(product_id=2, rating=4, content="청소 성능은 좋지만 충전 시간이 깁니다.", sentiment="positive"),

        Review(product_id=3, rating=5, content="흡입력이 정말 좋고 카펫 청소에 강합니다.", sentiment="positive"),
        Review(product_id=3, rating=2, content="소음이 크고 무게가 부담됩니다.", sentiment="negative"),
        Review(product_id=3, rating=3, content="성능은 좋은데 가격이 너무 높습니다.", sentiment="neutral"),

        Review(product_id=4, rating=4, content="가격 대비 성능이 좋습니다.", sentiment="positive"),
        Review(product_id=4, rating=2, content="내구성이 약한 것 같고 배터리 성능이 아쉽습니다.", sentiment="negative"),
        Review(product_id=4, rating=3, content="가볍지만 흡입력은 평범합니다.", sentiment="neutral"),

        Review(product_id=5, rating=5, content="무게가 가볍고 사용하기 편합니다.", sentiment="positive"),
        Review(product_id=5, rating=2, content="배송이 늦고 포장이 훼손되어 왔습니다.", sentiment="negative"),
        Review(product_id=5, rating=3, content="소음은 적지만 흡입력이 조금 약합니다.", sentiment="neutral"),
    ]

    db.add_all(reviews)
    db.commit()