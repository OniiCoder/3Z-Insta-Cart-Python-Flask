from decimal import Decimal
from app.models import db, Customer, Product, Cart, Category

def seed_database():
    # 1. Customer
    customer = Customer.query.filter_by(email="alice@example.com").first()
    if not customer:
        customer = Customer(
            name="Alice Johnson",
            email="alice@example.com",
            phone="+1 (555) 234-5678",
            address="742 Evergreen Terrace",
            city="Springfield",
            zip_code="97477"
        )
        db.session.add(customer)
        db.session.flush()

    # 2. Cart
    cart = Cart.query.filter_by(customer_id=customer.id).first()
    if not cart:
        cart = Cart(customer_id=customer.id)
        db.session.add(cart)

    # 3. Products
    if Product.query.count() == 0:
        catalog = [
            # Produce
            Product(
                sku="SKU-PROD-001",
                name="Organic Hass Avocados",
                description="Ripe and ready-to-eat organic avocados.",
                category=Category.PRODUCE,
                price=Decimal("4.99"),
                stock_quantity=50,
                image_url="https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=500",
                unit="4 pack",
                active=True
            ),
            Product(
                sku="SKU-PROD-002",
                name="Organic Bananas",
                description="Fresh sweet organic yellow bananas.",
                category=Category.PRODUCE,
                price=Decimal("1.89"),
                stock_quantity=100,
                image_url="https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500",
                unit="1 bunch (~2 lbs)",
                active=True
            ),
            Product(
                sku="SKU-PROD-003",
                name="Honeycrisp Apples",
                description="Crisp, sweet, and juicy fresh apples.",
                category=Category.PRODUCE,
                price=Decimal("5.49"),
                stock_quantity=40,
                image_url="https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500",
                unit="2 lb bag",
                active=True
            ),
            # Dairy & Eggs
            Product(
                sku="SKU-DAIR-001",
                name="Organic Whole Milk",
                description="Farm fresh pasteurized organic whole milk.",
                category=Category.DAIRY_EGGS,
                price=Decimal("4.29"),
                stock_quantity=30,
                image_url="https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500",
                unit="1 Gallon",
                active=True
            ),
            Product(
                sku="SKU-DAIR-002",
                name="Pasture-Raised Grade A Large Eggs",
                description="Certified humane, rich golden yolks.",
                category=Category.DAIRY_EGGS,
                price=Decimal("5.99"),
                stock_quantity=45,
                image_url="https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=500",
                unit="12 Count",
                active=True
            ),
            Product(
                sku="SKU-DAIR-003",
                name="Greek Yogurt Plain 0% Fat",
                description="High protein authentic strained Greek yogurt.",
                category=Category.DAIRY_EGGS,
                price=Decimal("6.49"),
                stock_quantity=25,
                image_url="https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500",
                unit="32 oz",
                active=True
            ),
            # Bakery
            Product(
                sku="SKU-BAKE-001",
                name="San Francisco Sourdough Bread",
                description="Freshly baked artisan sourdough loaf.",
                category=Category.BAKERY,
                price=Decimal("4.99"),
                stock_quantity=20,
                image_url="https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=500",
                unit="24 oz",
                active=True
            ),
            Product(
                sku="SKU-BAKE-002",
                name="All-Butter French Croissants",
                description="Flaky, buttery, bakery-fresh croissants.",
                category=Category.BAKERY,
                price=Decimal("6.99"),
                stock_quantity=15,
                image_url="https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500",
                unit="4 pack",
                active=True
            ),
            # Beverages
            Product(
                sku="SKU-BEV-001",
                name="Cold Brew Nitro Coffee",
                description="Smooth, low-acidity single-origin Colombian cold brew.",
                category=Category.BEVERAGES,
                price=Decimal("3.99"),
                stock_quantity=60,
                image_url="https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500",
                unit="12 fl oz can",
                active=True
            ),
            Product(
                sku="SKU-BEV-002",
                name="Fresh Squeezed Orange Juice",
                description="100% pure orange juice with pulp.",
                category=Category.BEVERAGES,
                price=Decimal("5.79"),
                stock_quantity=25,
                image_url="https://images.unsplash.com/photo-1613478223719-2ab802602423?w=500",
                unit="52 fl oz",
                active=True
            ),
            # Snacks & Pantry
            Product(
                sku="SKU-SNAK-001",
                name="Artisan Kettle Sea Salt Potato Chips",
                description="Slow-cooked crunchy kettle chips.",
                category=Category.SNACKS,
                price=Decimal("3.49"),
                stock_quantity=50,
                image_url="https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500",
                unit="8.5 oz",
                active=True
            ),
            Product(
                sku="SKU-PAN-001",
                name="Extra Virgin Cold Pressed Olive Oil",
                description="Single estate Mediterranean olive oil.",
                category=Category.PANTRY,
                price=Decimal("14.99"),
                stock_quantity=20,
                image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500",
                unit="500 ml",
                active=True
            )
        ]
        db.session.add_all(catalog)

    db.session.commit()
