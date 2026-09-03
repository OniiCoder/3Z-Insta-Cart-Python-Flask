import secrets
from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from flask import current_app
from app.models import db, Cart, CartItem, Product, Order, OrderItem, OrderStatus, PaymentStatus
from app.schemas.order_schema import CheckoutSchema, OrderStatusUpdateSchema
from app.errors import ResourceNotFoundError, InsufficientStockError, CartEmptyError, BadRequestError

class OrderService:

    @staticmethod
    def _generate_order_number() -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = secrets.randbelow(9000) + 1000
        return f"3Z-{timestamp}-{suffix}"

    @classmethod
    def checkout(cls, data: CheckoutSchema) -> dict:
        cart = db.session.get(Cart, data.cartId)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {data.cartId}")

        if not cart.items:
            raise CartEmptyError("Cannot checkout an empty cart")

        if not cart.customer:
            raise BadRequestError("Cart must be linked to a customer before checkout")

        # 1. Verify stock and deduct inventory
        for item in cart.items:
            product = db.session.get(Product, item.product_id)
            if not product or not product.active:
                raise BadRequestError(f"Product '{item.product.name}' is no longer available.")

            if product.stock_quantity < item.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for product '{product.name}'. "
                    f"Requested: {item.quantity}, Available: {product.stock_quantity}"
                )

            # Deduct stock
            product.stock_quantity -= item.quantity

        # 2. Financial totals
        tax_rate = Decimal(str(current_app.config.get("DEFAULT_TAX_RATE", 0.07)))
        delivery_fee_default = Decimal(str(current_app.config.get("DELIVERY_FEE", 3.99)))
        free_threshold = Decimal(str(current_app.config.get("FREE_DELIVERY_THRESHOLD", 35.00)))

        subtotal = round(sum(item.item_total for item in cart.items), 2)
        tax = round(subtotal * tax_rate, 2)
        delivery_fee = Decimal("0.00") if subtotal >= free_threshold else delivery_fee_default
        total = round(subtotal + tax + delivery_fee, 2)

        # 3. Create Order
        order_number = cls._generate_order_number()
        order = Order(
            order_number=order_number,
            customer_id=cart.customer_id,
            subtotal=subtotal,
            tax_amount=tax,
            delivery_fee=delivery_fee,
            total_amount=total,
            status=OrderStatus.CONFIRMED,
            payment_status=PaymentStatus.PAID,
            delivery_address=data.deliveryAddress,
            delivery_city=data.deliveryCity or cart.customer.city,
            delivery_zip_code=data.deliveryZipCode or cart.customer.zip_code,
            delivery_instructions=data.deliveryInstructions
        )
        db.session.add(order)
        db.session.flush()

        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                sku=item.product.sku,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=round(item.item_total, 2)
            )
            db.session.add(order_item)

        # 4. Clear Cart
        db.session.query(CartItem).filter_by(cart_id=cart.id).delete()

        db.session.commit()
        return order.to_dict()

    @staticmethod
    def get_order_by_id(order_id: int) -> dict:
        order = db.session.get(Order, order_id)
        if not order:
            raise ResourceNotFoundError(f"Order not found with id: {order_id}")
        return order.to_dict()

    @staticmethod
    def get_order_by_number(order_number: str) -> dict:
        order = db.session.query(Order).filter_by(order_number=order_number).first()
        if not order:
            raise ResourceNotFoundError(f"Order not found with order number: {order_number}")
        return order.to_dict()

    @staticmethod
    def get_orders_by_customer(customer_id: int) -> List[dict]:
        orders = db.session.query(Order).filter_by(customer_id=customer_id).order_by(Order.created_at.desc()).all()
        return [o.to_dict() for o in orders]

    @staticmethod
    def update_order_status(order_id: int, data: OrderStatusUpdateSchema) -> dict:
        order = db.session.get(Order, order_id)
        if not order:
            raise ResourceNotFoundError(f"Order not found with id: {order_id}")

        order.status = data.status
        db.session.commit()
        return order.to_dict()
