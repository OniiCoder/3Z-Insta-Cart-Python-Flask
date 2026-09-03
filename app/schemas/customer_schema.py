from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CustomerCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Customer full name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    zipCode: Optional[str] = Field(None, description="Postal / Zip code")
