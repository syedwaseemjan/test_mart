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

    print("Adding inventory with initial logs...")
    # Insert inventory
    for p in product_objs:
        initial_stock = random.randint(5, 50)
        inventory = models.Inventory(product_id=p.id, stock=initial_stock)
        db.add(inventory)

        # Create initial inventory log
        log = models.InventoryLog(
            product_id=p.id,
            change=initial_stock,
            reason="initial stock",
            changed_at=datetime.utcnow() - timedelta(days=31),  # Before any sales
        )
        db.add(log)
    db.commit()

    print("Adding sales with inventory adjustments...")
    # Insert sales for last 30 days with inventory logs
    for p in product_objs:
        inventory = db.query(models.Inventory).filter(models.Inventory.product_id == p.id).first()
        for i in range(30):
            if random.random() < 0.5:  # Randomly skip some days
                continue

            quantity = random.randint(1, 5)
            sale_date = datetime.utcnow() - timedelta(days=i)

            sale = models.Sale(product_id=p.id, quantity=quantity, total_amount=quantity * p.price, sale_date=sale_date)
            db.add(sale)

            inventory.stock -= quantity

            # Create inventory log for sale
            log = models.InventoryLog(product_id=p.id, change=-quantity, reason="sale", changed_at=sale_date)
            db.add(log)
    db.commit()

    print("Adding occasional restocks...")
    for p in product_objs:
        for i in range(3):  # 3 restocks per product
            restock_date = datetime.utcnow() - timedelta(days=random.randint(1, 28))
            restock_qty = random.randint(10, 30)

            inventory = db.query(models.Inventory).filter(models.Inventory.product_id == p.id).first()
            inventory.stock += restock_qty

            # Create restock log
            log = models.InventoryLog(
                product_id=p.id, change=restock_qty, reason="manual adjustment", changed_at=restock_date
            )
            db.add(log)
    db.commit()

    db.close()
    print("Demo data created with complete inventory history.")


if __name__ == "__main__":
    create_demo_data()
