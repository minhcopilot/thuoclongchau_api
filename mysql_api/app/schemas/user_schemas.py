from pydantic import BaseModel,EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    name:str
    email:EmailStr
    password:str
    phone:str
    address:str
    
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool
    phone: Optional[str] = None
    address: Optional[str] = None
    

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_verified: Optional[bool] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    