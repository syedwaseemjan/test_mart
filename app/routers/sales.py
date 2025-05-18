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
def list_sales(
    product_id: int = None,
    category: str = None,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    return SaleService(db).get_filtered_sales(
        product_id=product_id,
        category=category,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/revenue")
def get_revenue(period: str = "day", db: Session = Depends(get_db)):
    return SaleService(db).get_revenue_by_period(period)


@router.get("/revenue/comparison")
def compare_revenue(
    period: str = "month",
    category: str = None,
    compare_periods: int = 2,  # Compare last 2 periods by default
    db: Session = Depends(get_db)
):
    return SaleService(db).get_revenue_comparison(
        period=period,
        category=category,
        compare_periods=compare_periods
    )
