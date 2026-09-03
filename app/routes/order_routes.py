from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from app.schemas.order_schema import CheckoutSchema, OrderStatusUpdateSchema
from app.services.order_service import OrderService

order_bp = Blueprint("orders", __name__, url_prefix="/api/v1")

@order_bp.route("/checkout", methods=["POST"])
def checkout():
    """Checkout cart and place order
    ---
    tags:
      - Orders & Checkout
    responses:
      201:
        description: Order placed successfully
    """
    data = CheckoutSchema.model_validate(request.get_json() or {})
    order = OrderService.checkout(data)
    return jsonify({
        "success": True,
        "message": "Order placed successfully",
        "data": order,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 201

@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id: int):
    """Get order by ID
    ---
    tags:
      - Orders & Checkout
    responses:
      200:
        description: Order details
    """
    order = OrderService.get_order_by_id(order_id)
    return jsonify({
        "success": True,
        "message": "Order retrieved successfully",
        "data": order,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@order_bp.route("/orders/number/<string:order_number>", methods=["GET"])
def get_order_by_number(order_number: str):
    """Get order by tracking number
    ---
    tags:
      - Orders & Checkout
    responses:
      200:
        description: Order details
    """
    order = OrderService.get_order_by_number(order_number)
    return jsonify({
        "success": True,
        "message": "Order retrieved successfully",
        "data": order,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@order_bp.route("/orders/customer/<int:customer_id>", methods=["GET"])
def get_customer_orders(customer_id: int):
    """Get all orders for a customer
    ---
    tags:
      - Orders & Checkout
    responses:
      200:
        description: Customer orders list
    """
    orders = OrderService.get_orders_by_customer(customer_id)
    return jsonify({
        "success": True,
        "message": "Customer orders retrieved successfully",
        "data": orders,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@order_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_order_status(order_id: int):
    """Update order fulfillment status
    ---
    tags:
      - Orders & Checkout
    responses:
      200:
        description: Order status updated
    """
    data = OrderStatusUpdateSchema.model_validate(request.get_json() or {})
    order = OrderService.update_order_status(order_id, data)
    return jsonify({
        "success": True,
        "message": "Order status updated successfully",
        "data": order,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200
