from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastName: Optional[str] = None
    lastName2: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    cellPhone: Optional[PhoneNumber] = None
