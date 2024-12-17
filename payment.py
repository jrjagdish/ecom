import razorpay
from fastapi import HTTPException
import requests

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("YOUR_API_KEY", "YOUR_API_SECRET"))

async def create_payment_link(order_id: int, total_amount: float):
    try:
        
        razorpay_order = razorpay_client.order.create(dict(
            amount=int(total_amount * 100),  
            currency="INR",
            payment_capture="1",
        ))
        
      
        return razorpay_order['id']
    except razorpay.errors.RazorpayError as e:
     
        raise HTTPException(status_code=500, detail=f"Razorpay error: {str(e)}")
    except requests.exceptions.RequestException as e:
   
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
