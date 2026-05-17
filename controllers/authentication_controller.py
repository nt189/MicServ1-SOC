from fastapi import HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
from jose import jwt

from models.authentication_models import User, UserLogin
from config.db import db
from config.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

ph = PasswordHasher()
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        print(f"Verificando contraseña: {plain_password} contra hash: {hashed_password}")
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def register(user: User, response: Response):
    userExists = await db.users.find_one({"email": str(user.email)})
    if userExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # Cambiar codigo de estado a uno mas ambiuo para evitar ataques de enumeración de usuarios   
            detail="El correo electrónico ya está registrado." 
        )

    userDict = jsonable_encoder(user)
    
    userDict["password"] = get_password_hash(userDict["password"])
     
    
    accessToken = create_token({"sub": str(user.email), "auth": True}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refreshToken = create_token({"sub": str(user.email), "auth": True}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    userDict["token"] = accessToken
    await db.users.insert_one(userDict)
    
    response.set_cookie(key="accessToken", value=accessToken, samesite="none", httponly=True, secure=True)
    response.set_cookie(key="refreshToken", value=refreshToken, samesite="none", httponly=True, secure=True)

    return {
        "statusCode": status.HTTP_201_CREATED,
        "message": "Usuario registrado exitosamente"
    }

async def login(userLogin: UserLogin, response: Response):
    userInDb = await db.users.find_one({"email": str(userLogin.email)})
    if not userInDb or not verify_password(userInDb["password"], userLogin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos."
        )

    accessToken = create_token({"sub": str(userInDb["email"])}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refreshToken = create_token({"sub": str(userInDb["email"])}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    await db.users.update_one(
        {"email": userInDb["email"]},
        {"$set": {"token": accessToken}}
    )

    response.set_cookie(key="accessToken", value=accessToken, samesite="none", httponly=True, secure=True)
    response.set_cookie(key="refreshToken", value=refreshToken, samesite="none", httponly=True, secure=True)

    return {
        "statusCode": status.HTTP_200_OK,
        "message": "Inicio de sesión exitoso",
        "user": {
            "name": userInDb["name"],
            "lastName": userInDb["lastName"],
            "email": userInDb["email"],
            "cellPhone": userInDb["cellPhone"]
        }
    }

async def logout(token: str, response: Response):
    await db.revoked_tokens.insert_one({
        "token": token,
        "revoked_at": datetime.utcnow()
    })
    
    response.delete_cookie(key="accessToken")
    response.delete_cookie(key="refreshToken")

    return {
        "statusCode": status.HTTP_200_OK,
        "message": "Cierre de sesión exitoso. El token ha sido invalidado."
    }

async def refresh_token(refreshToken: str, response: Response):
    try:
        tokenRevoked = await db.revoked_tokens.find_one({"token": refreshToken})
        if tokenRevoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token proporcionado ha sido revocado."
            )

        payload = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido."
            )
        
        userInDb = await db.users.find_one({"email": email})
        if not userInDb:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El usuario ya no existe."
            )

        accessToken = create_token({"sub": email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        response.set_cookie(key="accessToken", value=accessToken, httponly=True)

        return {
            "statusCode": status.HTTP_200_OK,
            "message": "Access token renovado exitosamente"
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El refresh token ha expirado. Inicia sesión nuevamente."
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token."
        )

async def forgot_password(email: str):
    userInDb = await db.users.find_one({"email": email})
    
    if userInDb:
        reset_token = create_token({"sub": email, "type": "reset_password"}, timedelta(minutes=15))
        
        print(f"-> Simulando envío de OTP/Token de recuperación a {email}: {reset_token}")

    return {
        "statusCode": status.HTTP_200_OK,
        "message": "Si el correo electrónico está registrado, recibirás instrucciones para restablecer tu contraseña."
    }

async def reset_password(reset_token: str, new_password: str):
    tokenRevoked = await db.revoked_tokens.find_one({"token": reset_token})
    if tokenRevoked:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token proporcionado ya ha sido utilizado o revocado."
        )

    try:
        payload = jwt.decode(reset_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if token_type != "reset_password":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de tipo incorrecto."
            )

        userInDb = await db.users.find_one({"email": email})
        if not userInDb:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )

        hashed_password = get_password_hash(new_password)
        await db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})

        # Invalidar el token después de usarlo con éxito
        await db.revoked_tokens.insert_one({
            "token": reset_token,
            "revoked_at": datetime.utcnow()
        })

        return {
            "statusCode": status.HTTP_200_OK,
            "message": "Contraseña restablecida exitosamente."
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token de restablecimiento ha expirado."
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de restablecimiento inválido."
        )