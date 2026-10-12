from fastapi import FastAPI, HTTPException, Depends
from db_helpers.users.insert_user_with_hashed_pw import insert_user
from db_helpers.users.select_user import select_user
from db_helpers.categories.insert_category import insert_category
from db_helpers.categories.select_category import select_category
from db_helpers.transactions.insert_transaction import insert_transaction
from db_helpers.crud import get_transactions
from database import SessionLocal
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from psycopg2 import pool
from models.models import UserPublic, UserLogin, UserCreate, LoginReponse, CategoryCreate, TransactionCreate, TransactionType
from utils.generate_jwt import generate_jwt
from utils.get_current_user_id import get_current_user_id
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()
secret_key = os.getenv("JWT_SECRET")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dbname="finance_tracker",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
    yield
    app.state.pool.closeall()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello Backend!"}

@app.post("/register", response_model=UserPublic)
def register_user(user: UserCreate):
    insert_user(app.state.pool, user.username, user.email, user.password)
    user = select_user(app.state.pool, user.email)
    return user

@app.post("/login", response_model=LoginReponse)
def login_user(user_credentials: UserLogin):
    user = select_user(app.state.pool, user_credentials.email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if bcrypt.checkpw(user_credentials.password.encode("utf-8"), user.password.encode("utf-8")):
        return LoginReponse(jwt=generate_jwt(user.id))
    
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/categories")
def create_category(category: CategoryCreate, user_id: int = Depends(get_current_user_id)):
    insert_category(app.state.pool, user_id, category)
    category = select_category(app.state.pool, category.name, user_id)
    return category

@app.post("/transactions")
def create_transaction(transaction: TransactionCreate, user_id: int = Depends(get_current_user_id)):
    return insert_transaction(app.state.pool, user_id, transaction)

@app.get("/transactions")
def get_transactions_list(type: TransactionType | None = None, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_transactions(type, db, user_id)
