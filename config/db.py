from motor.motor_asyncio import AsyncIOMotorClient
from config.envLoader import mongoDBConn

client = AsyncIOMotorClient(mongoDBConn)

db = client.identity_db

async def check_db_connection() -> bool:
    try:
        await client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False
