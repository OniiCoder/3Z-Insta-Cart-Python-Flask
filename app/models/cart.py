from datetime import datetime, timezone
from decimal import Decimal
from app.models import db

class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    customer = db.relationship("Customer", back_populates="cart")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="joined")

    def clear(self):
        self.items.clear()


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", lazy="joined")

    @property
    def item_total(self) -> Decimal:
        return Decimal(str(self.unit_price)) * Decimal(str(self.quantity))

    def to_dict(self):
        return {
            "id": self.id,
            "productId": self.product_id,
            "productName": self.product.name if self.product else None,
            "productSku": self.product.sku if self.product else None,
            "unitPrice": float(self.unit_price),
            "quantity": self.quantity,
            "itemTotal": float(round(self.item_total, 2)),
            "imageUrl": self.product.image_url if self.product else None,
            "unit": self.product.unit if self.product else None,
        }
