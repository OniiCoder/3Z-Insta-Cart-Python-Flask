from datetime import datetime, timezone
from flask import jsonify, request
from pydantic import ValidationError

class ResourceNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class InsufficientStockError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class CartEmptyError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class BadRequestError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

def register_error_handlers(app):

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found(e):
        return jsonify({
            "status": 404,
            "error": "Not Found",
            "message": e.message,
            "details": [e.message],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 404

    @app.errorhandler(InsufficientStockError)
    def handle_insufficient_stock(e):
        return jsonify({
            "status": 400,
            "error": "Insufficient Stock",
            "message": e.message,
            "details": [e.message],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 400

    @app.errorhandler(CartEmptyError)
    def handle_cart_empty(e):
        return jsonify({
            "status": 400,
            "error": "Cart Is Empty",
            "message": e.message,
            "details": [e.message],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 400

    @app.errorhandler(BadRequestError)
    def handle_bad_request(e):
        return jsonify({
            "status": 400,
            "error": "Bad Request",
            "message": e.message,
            "details": [e.message],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 400

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        errors = [f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in e.errors()]
        return jsonify({
            "status": 400,
            "error": "Validation Failed",
            "message": "Input validation failed. Please check the 'details' field for specific issues.",
            "details": errors,
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 400

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "status": 404,
            "error": "Not Found",
            "message": "The requested resource was not found on this server.",
            "details": [str(e)],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "details": [str(e)],
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500
