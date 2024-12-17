from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="sqlite://ecom",  
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas() 