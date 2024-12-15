from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="sqlite://ecom",  # Use actual DB URL
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas() 