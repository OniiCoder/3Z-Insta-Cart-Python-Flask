from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from app.schemas.customer_schema import CustomerCreateSchema
from app.services.customer_service import CustomerService

customer_bp = Blueprint("customers", __name__, url_prefix="/api/v1/customers")

@customer_bp.route("", methods=["GET"])
def get_customers():
    """List all customers
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of customers
    """
    customers = CustomerService.get_all_customers()
    return jsonify({
        "success": True,
        "message": "Customers retrieved successfully",
        "data": customers,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id: int):
    """Get customer by ID
    ---
    tags:
      - Customers
    responses:
      200:
        description: Customer profile
    """
    customer = CustomerService.get_customer_by_id(customer_id)
    return jsonify({
        "success": True,
        "message": "Customer retrieved successfully",
        "data": customer,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@customer_bp.route("", methods=["POST"])
def create_customer():
    """Create a customer profile
    ---
    tags:
      - Customers
    responses:
      201:
        description: Customer created successfully
    """
    data = CustomerCreateSchema.model_validate(request.get_json() or {})
    customer = CustomerService.create_customer(data)
    return jsonify({
        "success": True,
        "message": "Customer created successfully",
        "data": customer,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 201
