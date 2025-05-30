from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import desc, extract, func
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

    def get_products(self, skip: int = 0, limit: int = 100) -> list[models.Product]:
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

        log = models.InventoryLog(product_id=inventory.product_id, change=inventory.stock, reason="initial stock")
        self.db.add(log)

        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def get_inventory(self, product_id: int) -> Optional[models.Inventory]:
        return self.db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

    def get_all_inventory(self) -> list[models.Inventory]:
        return self.db.query(models.Inventory).all()

    def get_low_stock(self, threshold: int = 10) -> list[models.Inventory]:
        return self.db.query(models.Inventory).filter(models.Inventory.stock < threshold).all()

    def update_inventory_stock(self, product_id: int, stock: int) -> Optional[models.Inventory]:
        inventory = self.get_inventory(product_id)
        if inventory:
            change = stock - inventory.stock
            inventory.stock = stock

            log = models.InventoryLog(product_id=product_id, change=change, reason="manual adjustment")
            self.db.add(log)
            self.db.commit()
            self.db.refresh(inventory)
        return inventory

    def get_logs(self, product_id: int, skip: int = 0, limit: int = 100) -> list[models.InventoryLog]:
        product = ProductService(self.db).get_product(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")

        return (
            self.db.query(models.InventoryLog)
            .filter(models.InventoryLog.product_id == product_id)
            .order_by(models.InventoryLog.changed_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


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
            db_sale = models.Sale()
            db_sale.product_id = sale.product_id
            db_sale.quantity = sale.quantity
            db_sale.sale_date = sale.sale_date
            db_sale.total_amount = total_amount
            self.db.add(db_sale)

            inventory.stock -= sale.quantity

            log = models.InventoryLog(
                product_id=sale.product_id, change=-sale.quantity, reason="sale"  # Negative for deduction
            )
            self.db.add(log)

            self.db.commit()
            self.db.refresh(db_sale)
            return db_sale
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error during sale transaction")

    def get_filtered_sales(
        self,
        product_id: Optional[int] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> list[models.Sale]:
        query = self.db.query(models.Sale)

        if product_id:
            query = query.filter(models.Sale.product_id == product_id)

        if category:
            query = query.join(models.Product).filter(models.Product.category == category)

        if start_date:
            query = query.filter(models.Sale.sale_date >= start_date)

        if end_date:
            query = query.filter(models.Sale.sale_date <= end_date)

        return query.order_by(models.Sale.sale_date.desc()).all()

    def get_revenue_by_period(self, period: str = "day") -> list[dict]:
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
                .all()  # type: ignore
            )
            return [{"year": int(r[0]), "month": int(r[1]), "total_amount": float(r[2])} for r in results]

        elif period == "year":
            results = (
                self.db.query(extract("year", sale_date).label("year"), total).group_by("year").all()  # type: ignore
            )
            return [{"year": int(r[0]), "total_amount": float(r[1])} for r in results]

        return []

    def get_revenue_comparison(
        self,
        period: str = "month",
        category: Optional[str] = None,
        compare_periods: int = 2
    ) -> list[dict]:
        query = self.db.query(
            extract("year", models.Sale.sale_date).label("year"),
            func.sum(models.Sale.total_amount).label("total_amount")
        )

        if category:
            query = query.join(models.Product).filter(models.Product.category == category)

        # Add grouping based on period
        if period == "day":
            query = query.add_columns(
                extract("month", models.Sale.sale_date).label("month"),
                extract("day", models.Sale.sale_date).label("day")
            ).group_by(
                "year", "month", "day"
            ).order_by(
                desc("year"), desc("month"), desc("day")
            )  # type: ignore
        elif period == "week":
            query = query.add_columns(
                extract("week", models.Sale.sale_date).label("week")
            ).group_by(
                "year", "week"
            ).order_by(
                desc("year"), desc("week")
            )  # type: ignore
        elif period == "month":
            query = query.add_columns(
                extract("month", models.Sale.sale_date).label("month")
            ).group_by(
                "year", "month"
            ).order_by(
                desc("year"), desc("month")
            )  # type: ignore
        else:  # year
            query = query.group_by(
                "year"
            ).order_by(
                desc("year")
            )

        results = query.limit(compare_periods).all()

        # Format results based on period type
        formatted_results = []
        for r in results:
            result = {
                "total_amount": float(r.total_amount),
                "category": category if category else "all"
            }

            if period == "day":
                result["period"] = f"{int(r.year)}-{int(r.month):02d}-{int(r.day):02d}"
            elif period == "week":
                result["period"] = f"{int(r.year)}-W{int(r.week):02d}"
            elif period == "month":
                result["period"] = f"{int(r.year)}-{int(r.month):02d}"
            else:  # year
                result["period"] = f"{int(r.year)}"

            formatted_results.append(result)

        return formatted_results
