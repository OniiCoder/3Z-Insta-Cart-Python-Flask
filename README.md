# 🛒 3Z Insta Cart - Python / Flask E-Commerce REST API

A production-grade, idiomatic **Python + Flask** REST API for **3Z Insta Cart**, an instant grocery & e-commerce shopping platform matching the full functionality and business rules of the Spring Boot edition.

---

## 🚀 Key Features

- **Product Catalog & Inventory**:
  - Full CRUD operations with category filtering, keyword search, stock tracking, and pricing.
  - Pre-seeded with 12 instant grocery items across categories (`PRODUCE`, `DAIRY_EGGS`, `BAKERY`, `BEVERAGES`, `SNACKS`, `PANTRY`, `MEAT_SEAFOOD`).
- **3Z Insta Cart Shopping Engine**:
  - Add items to cart with automatic duplicate item quantity consolidation.
  - Real-time stock validation and error handling.
  - Dynamic financial computation: subtotal, 7% sales tax, and tiered delivery fee ($3.99, free on orders over $35.00).
- **Atomic Checkout & Order Management**:
  - Validates stock availability and deducts inventory atomically at checkout.
  - Unique order tracking generation (`3Z-YYYYMMDDHHMMSS-XXXX`).
  - Order status tracking (`PENDING` -> `CONFIRMED` -> `PREPARING` -> `OUT_FOR_DELIVERY` -> `DELIVERED`).
- **Interactive Documentation & Observability**:
  - **OpenAPI / Swagger UI** at `http://localhost:8080/swagger-ui.html`.
  - **OpenAPI JSON Spec** at `http://localhost:8080/v3/api-docs`.
  - **Health checks** at `http://localhost:8080/actuator/health` and `http://localhost:8080/health`.

---

## 🛠️ Tech Stack & Requirements

- **Python**: 3.13+
- **Web Framework**: Flask 3.0.3
- **ORM / Database**: Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0, SQLite
- **Validation**: Pydantic 2.8.2 & Email-Validator
- **Documentation**: Flasgger / Swagger UI
- **Testing**: pytest 8.3.2, pytest-flask

---

## 📦 How to Setup and Run

### 1. Activate Virtual Environment
```bash
cd /Users/peterperez/Documents/PythonProjects/3z-insta-cart
source .venv/bin/activate
```

### 2. Run Automated Tests
```bash
pytest -v
```

### 3. Start Application
```bash
python app.py
```
*Or with custom port:*
```bash
PORT=8080 python app.py
```

---

## 📖 API Documentation & Endpoints

### 📍 Interactive Swagger UI
Open your browser at:
👉 **[http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)**
👉 OpenAPI JSON Spec: `http://localhost:8080/v3/api-docs`

---

### 🛒 1. Shopping Cart API (`/api/v1/carts`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/carts/<cart_id>` | Get cart details with calculated totals & items |
| `GET` | `/api/v1/carts/customer/<customer_id>` | Get or create cart for customer |
| `POST` | `/api/v1/carts/<cart_id>/items` | Add product to cart (body: `{"productId": 1, "quantity": 2}`) |
| `PUT` | `/api/v1/carts/<cart_id>/items/<item_id>` | Update item quantity in cart |
| `DELETE` | `/api/v1/carts/<cart_id>/items/<item_id>` | Remove specific item |
| `DELETE` | `/api/v1/carts/<cart_id>/clear` | Clear all items from cart |

---

### 📦 2. Orders & Checkout API (`/api/v1`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/checkout` | Checkout cart, deduct stock, create order |
| `GET` | `/api/v1/orders/<id>` | Get order details by ID |
| `GET` | `/api/v1/orders/number/<order_number>` | Lookup order by 3Z tracking number |
| `GET` | `/api/v1/orders/customer/<customer_id>` | View order history for a customer |
| `PATCH` | `/api/v1/orders/<id>/status` | Update order delivery status |

---

### 🍎 3. Products API (`/api/v1/products`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/products` | List active products (supports `?category=` and `?search=`) |
| `GET` | `/api/v1/products/<id>` | Get product details |
| `POST` | `/api/v1/products` | Create a new product |
| `PUT` | `/api/v1/products/<id>` | Update product information/stock |
| `DELETE` | `/api/v1/products/<id>` | Soft delete product |

---

### 👤 4. Customers API (`/api/v1/customers`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/customers` | List registered customers |
| `GET` | `/api/v1/customers/<id>` | Get customer profile |
| `POST` | `/api/v1/customers` | Register a new customer |

---

## 🧪 Quick Test Walkthrough (cURL)

```bash
# 1. Fetch available products
curl http://localhost:8080/api/v1/products

# 2. Add Organic Avocados and Whole Milk to Cart 1
curl -X POST http://localhost:8080/api/v1/carts/1/items \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 2}'

curl -X POST http://localhost:8080/api/v1/carts/1/items \
  -H "Content-Type: application/json" \
  -d '{"productId": 4, "quantity": 1}'

# 3. View Cart Summary & Totals
curl http://localhost:8080/api/v1/carts/1

# 4. Instant Checkout
curl -X POST http://localhost:8080/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "cartId": 1,
    "deliveryAddress": "742 Evergreen Terrace",
    "deliveryCity": "Springfield",
    "deliveryZipCode": "97477",
    "deliveryInstructions": "Leave on front porch"
  }'

# 5. Track Order Status
curl http://localhost:8080/api/v1/orders/1
```
# 3Z-Insta-Cart-Python-Flask
