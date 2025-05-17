import pytest

from app.models import Product


class TestInventory:
    @pytest.fixture(autouse=True)
    def setup(self, client, test_db):
        self.client = client
        self.db = test_db
        self.product = Product(name="Test Product", category="Test", price=100.00)
        self.db.add(self.product)
        self.db.commit()

    def test_create_inventory(self):
        inventory_data = {"product_id": self.product.id, "stock": 50}
        response = self.client.post("/api/inventory/", json=inventory_data)

        assert response.status_code == 200
        assert response.json()["stock"] == inventory_data["stock"]

    def test_create_inventory_duplicate_product(self):
        inventory_data = {"product_id": self.product.id, "stock": 50}
        self.client.post("/api/inventory/", json=inventory_data)
        response = self.client.post("/api/inventory/", json=inventory_data)

        assert response.status_code in [400, 409]
