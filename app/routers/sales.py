from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import SaleService

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return SaleService(db).create_sale(sale)


@router.get("/", response_model=list[schemas.Sale])
def list_sales(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    return SaleService(db).get_sales_by_date_range(start_date, end_date)


@router.get("/by-product/{product_id}", response_model=list[schemas.Sale])
def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    return SaleService(db).get_sales_by_product(product_id)


@router.get("/revenue")
def get_revenue(period: str = "day", db: Session = Depends(get_db)):
    return SaleService(db).get_revenue_by_period(period)
