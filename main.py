from fastapi import FastAPI, status
from insert_user_with_hashed_pw import insert_user
from select_user import select_user
from contextlib import asynccontextmanager
from psycopg2 import pool
from models import User, UserCredentials
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

@app.post("/register")
def register_user(user: User):
    insert_user(app.state.pool, user.username, user.email, user.password)
    return user

@app.post("/login")
def login_user(user_credentials: UserCredentials):
    user = select_user(app.state.pool, user_credentials.email)
    
    if user is None:
        return None
    
    if bcrypt.checkpw(user_credentials.password.encode("utf-8"), user.password.encode("utf-8")):
        return user
    
    return None