from typing import List
from app.models import db, Customer, Cart
from app.schemas.customer_schema import CustomerCreateSchema
from app.errors import ResourceNotFoundError, BadRequestError

class CustomerService:

    @staticmethod
    def get_all_customers() -> List[dict]:
        customers = db.session.query(Customer).all()
        return [c.to_dict() for c in customers]

    @staticmethod
    def get_customer_by_id(customer_id: int) -> dict:
        customer = db.session.get(Customer, customer_id)
        if not customer:
            raise ResourceNotFoundError(f"Customer not found with id: {customer_id}")
        return customer.to_dict()

    @staticmethod
    def create_customer(data: CustomerCreateSchema) -> dict:
        existing = db.session.query(Customer).filter_by(email=data.email).first()
        if existing:
            raise BadRequestError(f"Customer with email '{data.email}' already exists")

        customer = Customer(
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
            city=data.city,
            zip_code=data.zipCode
        )
        db.session.add(customer)
        db.session.flush()

        # Initialize an empty cart for the customer
        cart = Cart(customer_id=customer.id)
        db.session.add(cart)

        db.session.commit()
        return customer.to_dict()
