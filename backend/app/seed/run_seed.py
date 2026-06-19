from app.core.database import SessionLocal
from app.seed.product_seed import seed_products
from app.seed.review_seed import seed_reviews

db = SessionLocal()

try:
    seed_products(db)
    seed_reviews(db)
    print("시드 데이터 생성 완료")
finally:
    db.close()