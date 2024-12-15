from schemas import UserIn, ProductIn, ProductOut,CartIn,CartItem,OrderOut
from models import User, Product,Cart,Order
import security
from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError



async def create_user(user: UserIn):
    # Check if the user already exists by username
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered"
        )
    
    # Hash the password before storing it
    hashed_password = security.hash_password(user.password)
    
        # Create a new user record
    new_user = await User.create(
         username=user.username,
         email=user.email,
         hashed_password=hashed_password
         )
    return {"msg": "User registered successfully"}
  


async def authenticate_user(username: str, password: str) -> str:
    
    user = await User.filter(username=username).first()
    if not user or not security.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    

    return security.create_access_token(data={"sub": user.username})


async def enter_product(product: ProductIn):
        # Insert the new product into the database
        new_product = await Product.create(
            name=product.name,
            desc=product.desc,
            price=product.price,
            quantity=product.quantity
        )
        return new_product


async def get_product_by_id(product_id :int):
     product = await Product.filter(id = product_id).first()
     if not product:
          raise HTTPException(
               status_code= status.HTTP_404_NOT_FOUND,
               detail="product not found"
          )
     return product

async def cartitems(product_id : int,quantity:int):
     product = await Product.get(id = product_id)
     if not product:
          raise HTTPException(status_code=404,detail="not found")
     
     if product.quantity < quantity:
          raise HTTPException(status_code=400,detail="not enough stock")
     

     product.quantity -= quantity
     await product.save()

     await Cart.create(product = product,quantity = quantity)


     return "msg:product addded successfully"



async def create_order_from_cart( product_id: int,quantity : int):
        
        items = await Product.get(id =  product_id)
        
        if not items:
            raise HTTPException(status_code=404, detail="items not found")

        total_amount = items.price * quantity 
        
        # Create the order
        order = await Order.create(
             product_id=  product_id,
            total_amount=total_amount
            
        )
         
        return order