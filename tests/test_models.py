from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Inventory, Product, Sale


class TestProductModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        yield
        self.session.rollback()
        self.session.close()
        self.engine.dispose()

    def test_product_creation(self):
        product = Product(name="Laptop", category="Electronics", price=1299.99)
        self.session.add(product)
        self.session.commit()

        assert product.id is not None
        assert product.name == "Laptop"
        assert product.category == "Electronics"
        assert float(product.price) == 1299.99

    def test_product_required_fields(self):
        """Test non-nullable constraints"""
        with pytest.raises(Exception):
            product = Product(name=None, category=None, price=None)
            self.session.add(product)
            self.session.commit()


class TestSaleModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.product = Product(name="Test Product", category="Test", price=100.00)
        self.session.add(self.product)
        self.session.commit()
        yield
        self.session.rollback()
        self.session.close()
        self.engine.dispose()

    def test_sale_creation(self):
        sale = Sale(
            product_id=self.product.id,
            quantity=2,
            sale_date=date(2023, 1, 1),
            total_amount=200.00,
        )
        self.session.add(sale)
        self.session.commit()

        assert sale.id is not None
        assert sale.product == self.product
        assert len(self.product.sales) == 1

    def test_sale_amount_calculation(self):
        sale = Sale(
            product=self.product,
            quantity=3,
            sale_date=date.today(),
            total_amount=float(self.product.price) * 3,
        )
        assert float(sale.total_amount) == 300.00


class TestInventoryModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.product = Product(name="Inventory Product", category="Test", price=50.00)
        self.session.add(self.product)
        self.session.commit()
        yield
        self.session.rollback()
        self.session.close()
        self.engine.dispose()

    def test_inventory_relationship(self):
        inventory = Inventory(product=self.product, stock=100)
        self.session.add(inventory)
        self.session.commit()

        assert inventory.id is not None
        assert self.product.inventory == inventory
        assert inventory.last_updated is not None

    def test_stock_update(self):
        inventory = Inventory(product=self.product, stock=50)
        self.session.add(inventory)
        self.session.commit()

        inventory.stock = 30
        self.session.commit()
        assert self.product.inventory.stock == 30
