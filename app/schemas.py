# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    model_config ={"extra" : "forbid"}

class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config ={"extra" : "forbid"}

class Token(BaseModel):
    user: UserOut
    access_token: str
    token_type: str
