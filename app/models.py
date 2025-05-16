from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", uselist=False, back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)

    product = relationship("Product", back_populates="sales")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    stock = Column(Integer, nullable=False)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="inventory")
