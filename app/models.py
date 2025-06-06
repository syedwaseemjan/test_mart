from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (  # Keep these for column types
    DECIMAL,
    TIMESTAMP,
    Date,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True, default="")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    sales: Mapped[list["Sale"]] = relationship(back_populates="product")
    inventory: Mapped[Optional["Inventory"]] = relationship(back_populates="product", uselist=False)

    inventory_logs: Mapped[list["InventoryLog"]] = relationship(
        back_populates="product", order_by="desc(InventoryLog.changed_at)", cascade="all, delete-orphan"
    )


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    product: Mapped["Product"] = relationship(back_populates="inventory")


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="sales")


class InventoryLog(Base):
    __tablename__ = "inventory_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    change: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="inventory_logs")
