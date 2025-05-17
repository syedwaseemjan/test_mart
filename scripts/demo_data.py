import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal, engine  # noqa: F401

# Optional: Only if you haven't run migrations yet
# models.Base.metadata.create_all(bind=engine)

# Sample product list
PRODUCTS = [
    {"name": "Echo Dot", "category": "Electronics", "price": 49.99},
    {"name": "iPhone 14", "category": "Mobiles", "price": 999.00},
    {"name": "Air Fryer", "category": "Kitchen", "price": 120.00},
    {"name": "Samsung TV", "category": "Electronics", "price": 599.99},
    {"name": "Yoga Mat", "category": "Fitness", "price": 25.00},
]


def create_demo_data():
    db: Session = SessionLocal()

    # Clear existing data
    db.query(models.Sale).delete()
    db.query(models.Inventory).delete()
    db.query(models.Product).delete()
    db.commit()

    print("Adding demo products...")
    # Insert products
    product_objs = []
    for prod in PRODUCTS:
        p = models.Product(**prod)
        db.add(p)
        product_objs.append(p)
    db.commit()

    print("Adding inventory...")
    # Insert inventory
    for p in product_objs:
        inventory = models.Inventory(product_id=p.id, stock=random.randint(5, 50))
        db.add(inventory)
    db.commit()

    print("Adding sales...")
    # Insert sales for last 30 days
    for p in product_objs:
        for i in range(30):
            if random.random() < 0.5:  # Randomly skip some days
                continue
            quantity = random.randint(1, 5)
            sale_date = datetime.utcnow() - timedelta(days=i)
            sale = models.Sale(product_id=p.id, quantity=quantity, total_amount=quantity * p.price, sale_date=sale_date)
            db.add(sale)
    db.commit()
    db.close()
    print("Demo data created.")


if __name__ == "__main__":
    create_demo_data()
