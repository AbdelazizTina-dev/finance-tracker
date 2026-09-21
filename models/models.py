from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from constants.constants import TRANSACTION_AMOUNT_DECIMAL_PLACES, TRANSACTION_AMOUNT_MAX_DEGITS

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

class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    
class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    
class Category(BaseModel):
    name: str
    type: CategoryType
    id: int
    user_id: int
    created_at: datetime

class TransactionCreate(BaseModel):
    amount: Decimal = Field(max_digits=TRANSACTION_AMOUNT_MAX_DEGITS, decimal_places=TRANSACTION_AMOUNT_DECIMAL_PLACES)
    category_id: int | None = None
    description: str | None = None
    
class Transaction(BaseModel):
    id: int
    user_id: int
    category_id: int | None = None
    amount: Decimal = Field(max_digits=TRANSACTION_AMOUNT_MAX_DEGITS, decimal_places=TRANSACTION_AMOUNT_DECIMAL_PLACES)
    description: str | None = None
    created_at: datetime

