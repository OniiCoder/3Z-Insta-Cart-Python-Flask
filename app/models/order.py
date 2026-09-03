from datetime import datetime, timezone
from app.models import db
from app.models.enums import OrderStatus, PaymentStatus

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.CONFIRMED, nullable=False)
    payment_status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PAID, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_city = db.Column(db.String(100), nullable=True)
    delivery_zip_code = db.Column(db.String(20), nullable=True)
    delivery_instructions = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    customer = db.relationship("Customer", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "orderNumber": self.order_number,
            "customerId": self.customer_id,
            "customerName": self.customer.name if self.customer else None,
            "items": [item.to_dict() for item in self.items],
            "subtotal": float(self.subtotal),
            "taxAmount": float(self.tax_amount),
            "deliveryFee": float(self.delivery_fee),
            "totalAmount": float(self.total_amount),
            "status": self.status.value if isinstance(self.status, OrderStatus) else self.status,
            "paymentStatus": self.payment_status.value if isinstance(self.payment_status, PaymentStatus) else self.payment_status,
            "deliveryAddress": self.delivery_address,
            "deliveryCity": self.delivery_city,
            "deliveryZipCode": self.delivery_zip_code,
            "deliveryInstructions": self.delivery_instructions,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    sku = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "productId": self.product_id,
            "productName": self.product_name,
            "sku": self.sku,
            "unitPrice": float(self.unit_price),
            "quantity": self.quantity,
            "totalPrice": float(self.total_price),
        }
