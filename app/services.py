from typing import List, Optional

from fastapi import HTTPException, status
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


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_inventory(self, inventory: schemas.InventoryCreate) -> models.Inventory:
        existing = (
            self.db.query(models.Inventory)
            .filter(models.Inventory.product_id == inventory.product_id)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Inventory already exists for product_id {inventory.product_id}",
            )

        db_inventory = models.Inventory(**inventory.model_dump())
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def get_inventory(self, product_id: int) -> Optional[models.Inventory]:
        return (
            self.db.query(models.Inventory)
            .filter(models.Inventory.product_id == product_id)
            .first()
        )

    def get_all_inventory(self) -> List[models.Inventory]:
        return self.db.query(models.Inventory).all()

    def get_low_stock(self, threshold: int = 10) -> List[models.Inventory]:
        return (
            self.db.query(models.Inventory)
            .filter(models.Inventory.stock < threshold)
            .all()
        )

    def update_inventory_stock(
        self, product_id: int, stock: int
    ) -> Optional[models.Inventory]:
        inventory = self.get_inventory(product_id)
        if inventory:
            inventory.stock = stock
            self.db.commit()
            self.db.refresh(inventory)
        return inventory
