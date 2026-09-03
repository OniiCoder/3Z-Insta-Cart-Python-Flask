from .product_routes import product_bp
from .cart_routes import cart_bp
from .order_routes import order_bp
from .customer_routes import customer_bp
from .health_routes import health_bp

__all__ = [
    "product_bp",
    "cart_bp",
    "order_bp",
    "customer_bp",
    "health_bp",
]
