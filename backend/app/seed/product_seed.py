from sqlalchemy.orm import Session

from app.models.product import Product


def seed_products(db: Session):

    products = [
        Product(
            name="여성 루즈핏 니트",
            brand="MUSINSA",
            category="여성의류",
            price=39900,
        ),
        Product(
            name="플라워 롱 원피스",
            brand="MUSINSA",
            category="여성의류",
            price=59900,
        ),
        Product(
            name="남성 베이직 반팔티",
            brand="TOPTEN",
            category="남성의류",
            price=19900,
        ),
        Product(
            name="러닝 운동화",
            brand="NIKE",
            category="패션슈즈",
            price=129000,
        ),
        Product(
            name="데일리 숄더백",
            brand="STAND OIL",
            category="잡화",
            price=89000,
        ),
    ]

    db.add_all(products)
    db.commit()