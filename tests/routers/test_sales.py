from datetime import date

import pytest

from app.models import Inventory, Product


class TestSales:
    @pytest.fixture(autouse=True)
    def setup(self, client, test_db):
        self.client = client
        self.db = test_db

        self.PRICE = 100.00
        product = Product(name="Test Product", category="Test", price=self.PRICE)
        self.db.add(product)
        self.db.commit()

        inventory = Inventory(product_id=product.id, stock=50)
        self.db.add(inventory)
        self.db.commit()

        self.sale_data = {
            "product_id": product.id,
            "quantity": 2,
            "sale_date": str(date.today()),
            "total_amount": self.PRICE * 2,
        }

    def test_create_sale(self):
        response = self.client.post("/api/sales/", json=self.sale_data)
        assert response.status_code == 200
        assert float(response.json()["total_amount"]) == self.PRICE * 2

    def test_create_sale_invalid_product(self):
        invalid_data = self.sale_data.copy()
        invalid_data["product_id"] = 999
        response = self.client.post("/api/sales/", json=invalid_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Product with id 999 does not exist"
