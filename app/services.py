from datetime import date
from typing import Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import extract, func
from sqlalchemy.exc import SQLAlchemyError
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
        return self.db.query(models.Product).filter(models.Product.id == product_id).first()

    def get_products(self, skip: int = 0, limit: int = 100) -> List[models.Product]:
        return self.db.query(models.Product).offset(skip).limit(limit).all()


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_inventory(self, inventory: schemas.InventoryCreate) -> models.Inventory:
        # Check if inventory already exists
        existing = self.db.query(models.Inventory).filter(models.Inventory.product_id == inventory.product_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Inventory already exists for product_id {inventory.product_id}",
            )

        # Check if the referenced product exists
        product = self.db.query(models.Product).filter(models.Product.id == inventory.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {inventory.product_id} does not exist",
            )

        db_inventory = models.Inventory(**inventory.model_dump())
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def get_inventory(self, product_id: int) -> Optional[models.Inventory]:
        return self.db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

    def get_all_inventory(self) -> List[models.Inventory]:
        return self.db.query(models.Inventory).all()

    def get_low_stock(self, threshold: int = 10) -> List[models.Inventory]:
        return self.db.query(models.Inventory).filter(models.Inventory.stock < threshold).all()

    def update_inventory_stock(self, product_id: int, stock: int) -> Optional[models.Inventory]:
        inventory = self.get_inventory(product_id)
        if inventory:
            inventory.stock = stock
            self.db.commit()
            self.db.refresh(inventory)
        return inventory


class SaleService:
    def __init__(self, db: Session):
        self.db = db

    def create_sale(self, sale: schemas.SaleCreate) -> models.Sale:
        try:
            product = self.db.query(models.Product).filter(models.Product.id == sale.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with id {sale.product_id} does not exist")

            inventory = self.db.query(models.Inventory).filter(models.Inventory.product_id == sale.product_id).first()
            if not inventory:
                raise HTTPException(status_code=404, detail="Inventory not found")

            if inventory.stock < sale.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock. Available: {inventory.stock}, Requested: {sale.quantity}",
                )

            total_amount = product.price * sale.quantity
            db_sale = models.Sale(
                product_id=sale.product_id, quantity=sale.quantity, sale_date=sale.sale_date, total_amount=total_amount
            )
            self.db.add(db_sale)

            inventory.stock -= sale.quantity

            self.db.commit()
            self.db.refresh(db_sale)
            return db_sale
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error during sale transaction")

    def get_sales_by_date_range(self, start_date: date, end_date: date) -> List[models.Sale]:
        return (
            self.db.query(models.Sale)
            .filter(models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date)
            .all()
        )

    def get_sales_by_product(self, product_id: int) -> List[models.Sale]:
        return self.db.query(models.Sale).filter(models.Sale.product_id == product_id).all()

    def get_revenue_by_period(self, period: str = "day") -> List[Dict]:
        sale_date = models.Sale.sale_date
        total = func.sum(models.Sale.total_amount)

        if period == "day":
            results = self.db.query(sale_date, total).group_by(sale_date).all()
            return [{"date": r[0], "total_amount": float(r[1])} for r in results]

        elif period == "month":
            results = (
                self.db.query(
                    extract("year", sale_date).label("year"), extract("month", sale_date).label("month"), total
                )
                .group_by("year", "month")
                .all()
            )
            return [{"year": int(r[0]), "month": int(r[1]), "total_amount": float(r[2])} for r in results]

        elif period == "year":
            results = self.db.query(extract("year", sale_date).label("year"), total).group_by("year").all()
            return [{"year": int(r[0]), "total_amount": float(r[1])} for r in results]

        return []
