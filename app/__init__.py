import os
from flask import Flask
from flasgger import Swagger
from config import config_by_name
from app.models import db
from app.errors import register_error_handlers
from app.routes import product_bp, cart_bp, order_bp, customer_bp, health_bp
from app.seed import seed_database

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "default")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Database setup
    db.init_app(app)

    # Swagger / OpenAPI documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "v3/api-docs",
                "route": "/v3/api-docs",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger-ui.html"
    }

    template = {
        "swagger": "2.0",
        "info": {
            "title": "3Z Insta Cart E-Commerce API",
            "description": "High-performance Python/Flask RESTful API for 3Z Insta Cart instant grocery & e-commerce shopping, cart management, inventory tracking, and order fulfillment.",
            "contact": {
                "name": "3Z Insta Cart Engineering",
                "email": "engineering@threez-instacart.com"
            },
            "version": "1.0.0"
        }
    }

    Swagger(app, config=swagger_config, template=template)

    # Error handlers
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(health_bp)

    # Initialize tables and seed data
    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING"):
            seed_database()

    return app
