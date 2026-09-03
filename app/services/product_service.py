from typing import List, Optional
from app.models import db, Product, Category
from app.schemas.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.errors import ResourceNotFoundError, BadRequestError

class ProductService:

    @staticmethod
    def get_all_products(category: Optional[Category] = None, search: Optional[str] = None) -> List[dict]:
        query = db.session.query(Product).filter(Product.active == True)

        if category:
            query = query.filter(Product.category == category)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                (Product.name.ilike(term)) | (Product.description.ilike(term))
            )

        products = query.all()
        return [p.to_dict() for p in products]

    @staticmethod
    def get_product_by_id(product_id: int) -> dict:
        product = db.session.get(Product, product_id)
        if not product or not product.active:
            raise ResourceNotFoundError(f"Product not found with id: {product_id}")
        return product.to_dict()

    @staticmethod
    def create_product(data: ProductCreateSchema) -> dict:
        existing = db.session.query(Product).filter_by(sku=data.sku).first()
        if existing:
            raise BadRequestError(f"Product with SKU '{data.sku}' already exists")

        product = Product(
            sku=data.sku,
            name=data.name,
            description=data.description,
            category=data.category,
            price=data.price,
            stock_quantity=data.stockQuantity,
            image_url=data.imageUrl,
            unit=data.unit,
            active=True
        )
        db.session.add(product)
        db.session.commit()
        return product.to_dict()

    @staticmethod
    def update_product(product_id: int, data: ProductUpdateSchema) -> dict:
        product = db.session.get(Product, product_id)
        if not product:
            raise ResourceNotFoundError(f"Product not found with id: {product_id}")

        if product.sku != data.sku:
            existing = db.session.query(Product).filter_by(sku=data.sku).first()
            if existing:
                raise BadRequestError(f"Product with SKU '{data.sku}' already exists")

        product.sku = data.sku
        product.name = data.name
        product.description = data.description
        product.category = data.category
        product.price = data.price
        product.stock_quantity = data.stockQuantity
        product.image_url = data.imageUrl
        product.unit = data.unit

        db.session.commit()
        return product.to_dict()

    @staticmethod
    def delete_product(product_id: int) -> None:
        product = db.session.get(Product, product_id)
        if not product:
            raise ResourceNotFoundError(f"Product not found with id: {product_id}")
        product.active = False
        db.session.commit()
