import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestProduct:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)
        self.product_data = {"name": "Test Product", "category": "Electronics", "price": 999.99}

    def test_create_product(self):
        response = self.client.post("/api/products/", json=self.product_data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == self.product_data["name"]
        assert "id" in response_data

    def test_create_product_invalid_data(self):
        invalid_data = self.product_data.copy()
        invalid_data["price"] = -10  # Invalid price
        response = self.client.post("/api/products/", json=invalid_data)
        assert response.status_code == 422  # Unprocessable Entity
