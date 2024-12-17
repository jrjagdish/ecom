from schemas import UserIn, ProductIn, ProductOut,CartIn,CartItem,OrderOut
from models import User, Product,Cart,Order
import security
from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError
from payment import create_payment_link



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



async def create_order_from_cart(cart_id: int, quantity: int):
    
    buy = await Cart.filter(id=cart_id).prefetch_related("product")

    if not buy:
        raise HTTPException(status_code=404, detail="Items not found")

    total_amount = 0

   
    cart_instance = buy[0]  
    for item in buy:
        if not item.product:
            raise HTTPException(status_code=400, detail="Product not found in cart")

        total_amount += item.product.price * quantity  
    order = await Order.create(
        cart=cart_instance, 
        total_amount=total_amount
    )



    
    return {"msg:order created visit to payment and view your order"}


async def get_order(order_id: int):
    try:
        
        order = await Order.get(id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        
        payment_link = await create_payment_link(order.id, order.total_amount)
        
        return {
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "payment_link": payment_link
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {str(e)}")
    
async def delete_order(order_id: int):
        
        order = await Order.get(id=order_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        

        await order.delete()
        
        return {"msg": "Order deleted successfully"}    
    
