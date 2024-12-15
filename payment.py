import razorpay
from models import Order
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist



razorpay_client = razorpay.Client(auth=("your_razorpay_key_id", "your_razorpay_key_secret"))

def create_razorpay_payment_link(order_id: int):
    try:
        order = Order.get(id=order_id)
        
        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create(dict(
            amount=int(order.total_amount * 100),  
            currency="INR",  
            payment_capture="1",  
        ))
        
        return {
            "payment_link": f"https://checkout.razorpay.com/v1/checkout.js?order_id={razorpay_order['id']}",
            "razorpay_order_id": razorpay_order['id']
        }
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")