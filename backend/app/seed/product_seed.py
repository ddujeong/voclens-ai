from sqlalchemy.orm import Session

from app.models.product import Product


def seed_products(db: Session):

    products = [
        Product(
            name="LG 코드제로 A9",
            brand="LG",
            category="무선청소기",
            price=890000,
        ),
        Product(
            name="삼성 비스포크 제트",
            brand="삼성",
            category="무선청소기",
            price=950000,
        ),
        Product(
            name="다이슨 V15",
            brand="Dyson",
            category="무선청소기",
            price=1190000,
        ),
        Product(
            name="샤오미 G10",
            brand="Xiaomi",
            category="무선청소기",
            price=420000,
        ),
        Product(
            name="일렉트로룩스 UltimateHome",
            brand="Electrolux",
            category="무선청소기",
            price=590000,
        ),
    ]

    db.add_all(products)
    db.commit()