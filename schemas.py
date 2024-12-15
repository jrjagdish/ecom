from pydantic import BaseModel
from typing import Optional,List
from models import Product

# User input model
class UserIn(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True  # Make it compatible with Tortoise ORM

# Product input model (for creating or updating products)
class ProductIn(BaseModel):
    name: str
    desc: str
    price: float
    quantity: Optional[int]  # Mark quantity as Optional (can be None)

# Product output model (for returning data to the client)
class ProductOut(BaseModel):
    id: int
    name: str
    desc: str
    price: float
    quantity: Optional[int]  # Mark quantity as Optional (can be None)

    class Config:
        from_attributes = True  # Make it compatible with Tortoise ORM

class CartIn(BaseModel):
    product_id: int  # Ensure this field is correctly annotated with 'int'
    quantity: int

    class Config:
        from_attributes = True 

class CartItem(BaseModel):
    product: ProductOut   # Ensure this field is correctly annotated with 'int'
    quantity: int

    class Config:
        from_attributes = True  

class OrderIn(BaseModel):
    product_id: int  # Ensure this field is correctly annotated with 'int'
    quantity: int

    class Config:
        from_attributes = True  # Make it compatible with Tortoise ORM


# Order Output Schema (for returning order data)
class OrderOut(BaseModel):
    product : int   # Ensure this field is correctly annotated with 'int'
    total_amount : int

    class Config:
        from_attributes = True  

# Token model for authentication responses
class Token(BaseModel):
    access_token: str
    token_type: str
