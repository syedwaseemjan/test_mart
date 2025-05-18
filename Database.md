# Database Schema Documentation

## Overview

The database is designed to support the e-commerce admin API, focusing on **product management**, **sales tracking**, and **inventory control**. It uses a normalized relational schema optimized for queries related to sales analytics, revenue tracking, and inventory status.


## Tables and Relationships

### 1. `products`

| Column        | Type     | Description                        |
| ------------- | -------- | ---------------------------------- |
| `id`          | INT (PK) | Unique identifier for each product |
| `name`        | VARCHAR  | Product name                       |
| `category`    | VARCHAR  | Product category                   |
| `price`       | DECIMAL  | Price per unit                     |
| `description` | TEXT     | Product description (optional)     |
| `created_at`  | DATETIME | Timestamp when product was added   |
| `updated_at`  | DATETIME | Timestamp when product was updated |

**Purpose:** Stores basic product information and categorization.
**Indexes:** Primary key on `id`, index on `category` for faster filtering.


### 2. `sales`

| Column         | Type     | Description                                    |
| -------------- | -------- | ---------------------------------------------- |
| `id`           | INT (PK) | Unique identifier for each sale record         |
| `product_id`   | INT (FK) | References `products.id`                       |
| `quantity`     | INT      | Number of units sold                           |
| `total_amount` | DECIMAL  | Total price at which product was sold          |
| `sale_date`    | DATETIME | Timestamp of the sale                          |

**Purpose:** Records individual sales transactions linked to products.
**Indexes:** Primary key on `id`, index on `sale_date` for time-based queries, foreign key index on `product_id`.


### 3. `inventory`

| Column         | Type     | Description                            |
| -------------- | -------- | -------------------------------------- |
| `id`           | INT (PK) | Unique identifier for inventory record |
| `product_id`   | INT (FK) | References `products.id`               |
| `stock`        | INT      | Current stock level                    |
| `last_updated` | DATETIME | Last time the inventory was updated    |

**Purpose:** Tracks current inventory stock levels for each product.
**Indexes:** Primary key on `id`, foreign key index on `product_id`.


### 4. `inventory_log`

| Column       | Type     | Description                                            |
| ------------ | -------- | ------------------------------------------------------ |
| `id`         | INT (PK) | Unique identifier for log entry                        |
| `product_id` | INT (FK) | References `products.id`                               |
| `change`     | INT      | Number of units added (positive) or removed (negative) |
| `reason`     | VARCHAR  | Reason for inventory change (e.g., sale, restock)      |
| `changed_at` | DATETIME | Timestamp of the inventory change                      |

**Purpose:** Keeps a history of inventory level changes over time for audit and tracking.
**Indexes:** Primary key on `id`, foreign key index on `product_id`.


## Relationships

* `products` → `sales`: One-to-many
  Each product can have multiple sales records.

* `products` → `inventory`: One-to-one (or one-to-many if tracking multiple warehouses)
  Each product has a current inventory record.

* `products` → `inventory_log`: One-to-many
  Each product’s inventory changes are tracked over time.


## Additional Notes

* All foreign keys enforce **referential integrity** to avoid orphan records.
* Indexes on date columns (`sale_date`, `changed_at`) optimize queries for sales and inventory analysis over time.
* The schema is normalized to reduce redundancy but supports efficient aggregation queries for reporting.


