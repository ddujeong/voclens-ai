from app.models.review import Review
from app.models.review_document import ReviewDocument
from app.services.embedding_service import EmbeddingService


def seed_review_documents(db):
    if db.query(ReviewDocument).count() > 0:
        print("리뷰 문서 데이터 이미 존재")
        return

    reviews = db.query(Review).all()

    documents = []

    for review in reviews:
        embedding = EmbeddingService.embed(review.content)

        documents.append(
            ReviewDocument(
                review_id=review.id,
                content=review.content,
                embedding=embedding,
            )
        )

    db.add_all(documents)
    db.commit()

    print(f"리뷰 문서 {len(documents)}개 생성 완료")