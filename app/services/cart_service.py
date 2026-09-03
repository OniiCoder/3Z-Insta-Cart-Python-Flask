from decimal import Decimal
from flask import current_app
from app.models import db, Cart, CartItem, Product, Customer
from app.schemas.cart_schema import AddToCartSchema, UpdateCartItemSchema
from app.errors import ResourceNotFoundError, InsufficientStockError, BadRequestError

class CartService:

    @staticmethod
    def get_cart_response(cart: Cart) -> dict:
        tax_rate = Decimal(str(current_app.config.get("DEFAULT_TAX_RATE", 0.07)))
        delivery_fee_default = Decimal(str(current_app.config.get("DELIVERY_FEE", 3.99)))
        free_threshold = Decimal(str(current_app.config.get("FREE_DELIVERY_THRESHOLD", 35.00)))

        items_dict = [item.to_dict() for item in cart.items]
        total_count = sum(item.quantity for item in cart.items)

        subtotal = sum(item.item_total for item in cart.items) if cart.items else Decimal("0.00")
        subtotal = round(subtotal, 2)

        tax = round(subtotal * tax_rate, 2) if subtotal > 0 else Decimal("0.00")

        if subtotal == Decimal("0.00"):
            delivery_fee = Decimal("0.00")
        elif subtotal >= free_threshold:
            delivery_fee = Decimal("0.00")
        else:
            delivery_fee = delivery_fee_default

        total = round(subtotal + tax + delivery_fee, 2)

        return {
            "id": cart.id,
            "customerId": cart.customer_id,
            "customerName": cart.customer.name if cart.customer else None,
            "items": items_dict,
            "totalItemCount": total_count,
            "subtotal": float(subtotal),
            "taxAmount": float(tax),
            "deliveryFee": float(delivery_fee),
            "totalAmount": float(total),
        }

    @classmethod
    def get_cart_by_id(cls, cart_id: int) -> dict:
        cart = db.session.get(Cart, cart_id)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {cart_id}")
        return cls.get_cart_response(cart)

    @classmethod
    def get_or_create_cart_for_customer(cls, customer_id: int) -> dict:
        customer = db.session.get(Customer, customer_id)
        if not customer:
            raise ResourceNotFoundError(f"Customer not found with id: {customer_id}")

        cart = db.session.query(Cart).filter_by(customer_id=customer_id).first()
        if not cart:
            cart = Cart(customer_id=customer_id)
            db.session.add(cart)
            db.session.commit()

        return cls.get_cart_response(cart)

    @classmethod
    def add_item_to_cart(cls, cart_id: int, data: AddToCartSchema) -> dict:
        cart = db.session.get(Cart, cart_id)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {cart_id}")

        product = db.session.get(Product, data.productId)
        if not product or not product.active:
            raise ResourceNotFoundError(f"Product not found with id: {data.productId}")

        existing_item = db.session.query(CartItem).filter_by(cart_id=cart_id, product_id=data.productId).first()
        target_qty = data.quantity + (existing_item.quantity if existing_item else 0)

        if product.stock_quantity < target_qty:
            raise InsufficientStockError(
                f"Insufficient stock for product '{product.name}'. "
                f"Requested total: {target_qty}, Available: {product.stock_quantity}"
            )

        if existing_item:
            existing_item.quantity = target_qty
            existing_item.unit_price = product.price
        else:
            new_item = CartItem(
                cart_id=cart_id,
                product_id=product.id,
                quantity=data.quantity,
                unit_price=product.price
            )
            db.session.add(new_item)

        db.session.commit()
        return cls.get_cart_response(cart)

    @classmethod
    def update_cart_item_quantity(cls, cart_id: int, item_id: int, data: UpdateCartItemSchema) -> dict:
        cart = db.session.get(Cart, cart_id)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {cart_id}")

        item = db.session.query(CartItem).filter_by(id=item_id, cart_id=cart_id).first()
        if not item:
            raise ResourceNotFoundError(f"Cart item not found with id: {item_id} in cart: {cart_id}")

        if data.quantity <= 0:
            db.session.delete(item)
        else:
            if item.product.stock_quantity < data.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for product '{item.product.name}'. "
                    f"Requested: {data.quantity}, Available: {item.product.stock_quantity}"
                )
            item.quantity = data.quantity
            item.unit_price = item.product.price

        db.session.commit()
        return cls.get_cart_response(cart)

    @classmethod
    def remove_cart_item(cls, cart_id: int, item_id: int) -> dict:
        cart = db.session.get(Cart, cart_id)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {cart_id}")

        item = db.session.query(CartItem).filter_by(id=item_id, cart_id=cart_id).first()
        if not item:
            raise ResourceNotFoundError(f"Cart item not found with id: {item_id} in cart: {cart_id}")

        db.session.delete(item)
        db.session.commit()
        return cls.get_cart_response(cart)

    @classmethod
    def clear_cart(cls, cart_id: int) -> dict:
        cart = db.session.get(Cart, cart_id)
        if not cart:
            raise ResourceNotFoundError(f"Cart not found with id: {cart_id}")

        db.session.query(CartItem).filter_by(cart_id=cart_id).delete()
        db.session.commit()
        return cls.get_cart_response(cart)
