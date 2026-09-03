from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from app.models.enums import Category
from app.schemas.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.services.product_service import ProductService

product_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

@product_bp.route("", methods=["GET"])
def get_products():
    """List and search products
    ---
    tags:
      - Products
    parameters:
      - name: category
        in: query
        type: string
        required: false
      - name: search
        in: query
        type: string
        required: false
    responses:
      200:
        description: A list of products
    """
    category_param = request.args.get("category")
    search_param = request.args.get("search")

    category = None
    if category_param:
        try:
            category = Category(category_param.upper())
        except ValueError:
            return jsonify({
                "status": 400,
                "error": "Bad Request",
                "message": f"Invalid category: {category_param}",
                "details": [f"Allowed categories: {[c.value for c in Category]}"],
                "path": request.path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 400

    products = ProductService.get_all_products(category=category, search=search_param)
    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "data": products,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    """Get product by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Product details
    """
    product = ProductService.get_product_by_id(product_id)
    return jsonify({
        "success": True,
        "message": "Product retrieved successfully",
        "data": product,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@product_bp.route("", methods=["POST"])
def create_product():
    """Create a new product
    ---
    tags:
      - Products
    responses:
      201:
        description: Product created successfully
    """
    data = ProductCreateSchema.model_validate(request.get_json() or {})
    product = ProductService.create_product(data)
    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "data": product,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 201

@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int):
    """Update product details
    ---
    tags:
      - Products
    responses:
      200:
        description: Product updated successfully
    """
    data = ProductUpdateSchema.model_validate(request.get_json() or {})
    product = ProductService.update_product(product_id, data)
    return jsonify({
        "success": True,
        "message": "Product updated successfully",
        "data": product,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    """Soft delete a product
    ---
    tags:
      - Products
    responses:
      200:
        description: Product deactivated successfully
    """
    ProductService.delete_product(product_id)
    return jsonify({
        "success": True,
        "message": "Product deactivated successfully",
        "data": None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200
