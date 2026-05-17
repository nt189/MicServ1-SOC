from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic_extra_types.phone_numbers import PhoneNumber

class User(BaseModel):
    name: str
    lastName: str
    lastName2: Optional[str] = None
    email: EmailStr
    password: str
    cellPhone: PhoneNumber

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
