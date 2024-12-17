from pydantic import BaseModel
from typing import Optional,List
from models import Product

# User input model
class UserIn(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True  

class ProductIn(BaseModel):
    name: str
    desc: str
    price: float
    quantity: Optional[int] 


class ProductOut(BaseModel):
    id: int
    name: str
    desc: str
    price: float
    quantity: Optional[int] 
    class Config:
        from_attributes = True  

class CartIn(BaseModel):
    product_id: int 
    quantity: int

    class Config:
        from_attributes = True 

class CartItem(BaseModel):
    product: ProductOut   
    quantity: int

    class Config:
        from_attributes = True  

class OrderIn(BaseModel):
    cart_id : int
    quantity :int
     
    class Config:
          from_attributes = True 

class OrderOut(BaseModel):
    cart : List[CartItem]
    total_amount : int
    status : str
    payment :str

    class Config:
        from_attributes = True  


class Token(BaseModel):
    access_token: str
    token_type: str
