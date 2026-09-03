from pydantic import BaseModel, Field

class AddToCartSchema(BaseModel):
    productId: int = Field(..., gt=0, description="ID of the product to add")
    quantity: int = Field(..., ge=1, description="Quantity to add (must be at least 1)")

class UpdateCartItemSchema(BaseModel):
    quantity: int = Field(..., ge=0, description="New quantity (0 removes the item)")
