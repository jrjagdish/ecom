from tortoise import fields,models
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    hashed_password = fields.CharField(max_length=255)

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    desc = fields.TextField()
    price = fields.FloatField()
    quantity = fields.IntField(null=True)  # Corrected typo here

    def __str__(self):
        return f"Product(name={self.name}, price={self.price}, quantity={self.quantity})"
    
class Cart(Model):
    id = fields.IntField(pk=True)    
    product = fields.ForeignKeyField('models.Product', related_name='carts')
    quantity = fields.IntField(null = True)

    def __str__(self) -> str:
        return f"Cart {self.id} for Product {self.product.name}"
    

class Order(Model):
    id = fields.IntField(pk=True)
    cart = fields.ForeignKeyField('models.Cart', related_name='orders')
    total_amount = fields.FloatField()

    
    def __str__(self):
        return f"Order {self.id}"
    

