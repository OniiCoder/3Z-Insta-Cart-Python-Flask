from pydantic import BaseModel, Field
from typing import Optional
from app.models.enums import OrderStatus

class CheckoutSchema(BaseModel):
    cartId: int = Field(..., gt=0, description="Cart ID to checkout")
    deliveryAddress: str = Field(..., min_length=1, description="Shipping street address")
    deliveryCity: Optional[str] = Field(None, description="City")
    deliveryZipCode: Optional[str] = Field(None, description="ZIP/Postal code")
    deliveryInstructions: Optional[str] = Field(None, description="Delivery drop-off instructions")

class OrderStatusUpdateSchema(BaseModel):
    status: OrderStatus = Field(..., description="New fulfillment status")
