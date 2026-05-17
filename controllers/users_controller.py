from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from config.db import db
from models.user_models import UserUpdate
from bson import ObjectId
from controllers.authentication_controller import get_password_hash


def mongo_to_json(document):
    if not document:
        return None
    document["_id"] = str(document["_id"])  
    return jsonable_encoder(document)

async def get_user_profile(token: str):
    user = await db.users.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    mongo_to_json(user)
    user.pop("_id", None)
    user.pop("password", None)  
    user.pop("token", None)
    return user

async def update_user_profile(token: str, data: UserUpdate):
    user = await db.users.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if data.password:
        data.password = get_password_hash(data.password)

    await db.users.update_one({"token": token}, {"$set": data.dict(exclude_unset=True)})
    updated_user = await db.users.find_one({"token": token})

    mongo_to_json(user)
    updated_user.pop("_id", None)
    updated_user.pop("password", None)  
    updated_user.pop("token", None)

    return updated_user

async def delete_user_profile(token: str):
    user = await db.users.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    await db.users.delete_one({"token": token})
    return {"statusCode": status.HTTP_200_OK, "message": "Usuario eliminado exitosamente"}

async def get_user_by_id(id: str, token: str):
    try:
        user = await db.users.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return mongo_to_json(user)
