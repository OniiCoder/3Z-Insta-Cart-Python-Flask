from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from app.schemas.cart_schema import AddToCartSchema, UpdateCartItemSchema
from app.services.cart_service import CartService

cart_bp = Blueprint("carts", __name__, url_prefix="/api/v1/carts")

@cart_bp.route("/<int:cart_id>", methods=["GET"])
def get_cart(cart_id: int):
    """Get cart by ID
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Cart details and totals
    """
    cart = CartService.get_cart_by_id(cart_id)
    return jsonify({
        "success": True,
        "message": "Cart retrieved successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@cart_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_cart(customer_id: int):
    """Get or create customer cart
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Customer cart details
    """
    cart = CartService.get_or_create_cart_for_customer(customer_id)
    return jsonify({
        "success": True,
        "message": "Customer cart retrieved successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@cart_bp.route("/<int:cart_id>/items", methods=["POST"])
def add_item_to_cart(cart_id: int):
    """Add item to cart
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Item added successfully
    """
    data = AddToCartSchema.model_validate(request.get_json() or {})
    cart = CartService.add_item_to_cart(cart_id, data)
    return jsonify({
        "success": True,
        "message": "Item added to cart successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@cart_bp.route("/<int:cart_id>/items/<int:item_id>", methods=["PUT"])
def update_cart_item(cart_id: int, item_id: int):
    """Update cart item quantity
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Cart item updated successfully
    """
    data = UpdateCartItemSchema.model_validate(request.get_json() or {})
    cart = CartService.update_cart_item_quantity(cart_id, item_id, data)
    return jsonify({
        "success": True,
        "message": "Cart item updated successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@cart_bp.route("/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
def remove_cart_item(cart_id: int, item_id: int):
    """Remove item from cart
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Item removed successfully
    """
    cart = CartService.remove_cart_item(cart_id, item_id)
    return jsonify({
        "success": True,
        "message": "Item removed from cart successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@cart_bp.route("/<int:cart_id>/clear", methods=["DELETE"])
def clear_cart(cart_id: int):
    """Clear all items in cart
    ---
    tags:
      - Shopping Cart
    responses:
      200:
        description: Cart cleared successfully
    """
    cart = CartService.clear_cart(cart_id)
    return jsonify({
        "success": True,
        "message": "Cart cleared successfully",
        "data": cart,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200
