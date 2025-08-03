from pydantic import BaseModel, EmailStr
from typing import Optional

# Define the schemas for user operations
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    model_config ={"extra" : "forbid"}

# Schema for user output
class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config ={"extra" : "forbid"}

# Schema for token response
class Token(BaseModel):
    user: UserOut
    access_token: str
    token_type: str
