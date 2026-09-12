from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class User(BaseModel):
    email: str
    password: str
    username: str
    id: int
    created_at: datetime
    updated_at: datetime | None

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime | None
    
class LoginReponse(BaseModel):
    jwt: str
