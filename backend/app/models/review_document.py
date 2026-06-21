from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
)

from pgvector.sqlalchemy import Vector

from app.core.database import Base


class ReviewDocument(Base):
    __tablename__ = "review_documents"

    id = Column(Integer, primary_key=True)

    review_id = Column(
        Integer,
        ForeignKey("reviews.id"),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(384),
        nullable=False,
    )