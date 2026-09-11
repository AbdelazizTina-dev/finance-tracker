from fastapi import FastAPI, HTTPException
from insert_user_with_hashed_pw import insert_user
from select_user import select_user
from contextlib import asynccontextmanager
from psycopg2 import pool
from models import UserPublic, UserLogin, UserCreate
import bcrypt

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

@app.post("/login", response_model=UserPublic)
def login_user(user_credentials: UserLogin):
    user = select_user(app.state.pool, user_credentials.email)
    
    if user is None:
         raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if bcrypt.checkpw(user_credentials.password.encode("utf-8"), user.password.encode("utf-8")):
        return user
    
    raise HTTPException(status_code=401, detail="Invalid email or password")