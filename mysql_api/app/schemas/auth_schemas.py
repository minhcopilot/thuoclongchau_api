from pydantic import BaseModel,EmailStr
from typing import List
class TokenResponse(BaseModel):
    token: str
    refresh_token: str
    token_type: str
    data:object
    class Config:
        from_attributes = True
        
class RegisterResponse(BaseModel):
    token: str
    refresh_token: str
    token_type: str
    data:object
    class Config:
        from_attributes = True

class EmailSchema(BaseModel):
    email:List[EmailStr]