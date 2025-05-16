from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: schemas.ProductCreate) -> models.Product:
        db_product = models.Product(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_product(self, product_id: int) -> Optional[models.Product]:
        return (
            self.db.query(models.Product)
            .filter(models.Product.id == product_id)
            .first()
        )

    def get_products(self, skip: int = 0, limit: int = 100) -> List[models.Product]:
        return self.db.query(models.Product).offset(skip).limit(limit).all()
