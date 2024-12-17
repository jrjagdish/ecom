from fastapi import FastAPI,Depends,HTTPException
import schemas
from database import init  # Database initialization
from models import User,Product,Cart
import crud  # ORM models
from tortoise import Tortoise
from security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import payment

app = FastAPI()

# Initialize the database connection
@app.on_event("startup")
async def startup():
    await init()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise._drop_databases()     

@app.post("/register/")
async def register(user: schemas.UserIn):
    new_user = await crud.create_user(user)
    return new_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await crud.authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@app.post("/product/",response_model=schemas.ProductOut)
async def product(product:schemas.ProductIn,current_user : str = Depends(get_current_user)):
    new_product = await crud.enter_product(product)
    return new_product

@app.get("/products/{product_id}",response_model=schemas.ProductOut)
async def get_product(product_id : int , current_user : str = Depends(get_current_user)):
    product = await crud.get_product_by_id(product_id)
    return product

@app.post("/carts/")
async def cart_items(cart:schemas.CartIn, current_user : str = Depends(get_current_user)):
    items = await crud.cartitems(cart.product_id,cart.quantity)
    return items

@app.get("/cart/",response_model=list[schemas.CartItem])
async def view_cart( current_user : str = Depends(get_current_user)):
    items = await Cart.all().prefetch_related("product")
    return items

@app.post("/create-order/")
async def create_order(put:schemas.OrderIn):
    response = await crud.create_order_from_cart(put.cart_id, put.quantity)
    
    return response

@app.get("/view_order/{order_id}",response_model=schemas.OrderOut)
async def view_order_endpoint(order_id: int):
    order = await crud.get_order(order_id)
    return order

@app.delete("/delete_order/{order_id}")
async def delete_order_endpoint(order_id: int):
    result = await crud.delete_order(order_id)
    return result


