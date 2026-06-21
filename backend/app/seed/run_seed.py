from app.core.database import SessionLocal
from app.seed.product_seed import seed_products
from app.seed.review_seed import seed_reviews
from app.seed.review_document_seed import seed_review_documents

db = SessionLocal()

try:
    seed_products(db)
    seed_reviews(db)
    seed_review_documents(db)
    print("시드 데이터 생성 완료")
finally:
    db.close()