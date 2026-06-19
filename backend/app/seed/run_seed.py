from app.core.database import SessionLocal
from app.seed.product_seed import seed_products

db = SessionLocal()

try:
    seed_products(db)
    print("상품 시드 데이터 생성 완료")
finally:
    db.close()