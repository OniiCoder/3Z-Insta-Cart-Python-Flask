from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from app.models.enums import Category

class ProductCreateSchema(BaseModel):
    sku: str = Field(..., min_length=1, description="Product SKU identifier")
    name: str = Field(..., min_length=1, description="Product name")
    description: Optional[str] = Field(None, description="Detailed product description")
    category: Category = Field(..., description="Product Category")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Unit price")
    stockQuantity: int = Field(..., ge=0, description="Available stock quantity")
    imageUrl: Optional[str] = Field(None, description="Product image URL")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., '1 bunch', '1 gal')")

class ProductUpdateSchema(BaseModel):
    sku: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    category: Category
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stockQuantity: int = Field(..., ge=0)
    imageUrl: Optional[str] = None
    unit: Optional[str] = None
