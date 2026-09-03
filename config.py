import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "3z-insta-cart-dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///instacart.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3Z Insta Cart Business Rules
    DEFAULT_TAX_RATE = 0.07  # 7% Sales tax
    DELIVERY_FEE = 3.99     # $3.99 delivery fee
    FREE_DELIVERY_THRESHOLD = 35.00  # Free delivery on orders >= $35

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    "default": Config,
    "development": Config,
    "testing": TestConfig,
}
