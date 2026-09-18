from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from scripts.insert_user_with_hashed_pw import insert_user
from utils.select_user import select_user
from contextlib import asynccontextmanager
from psycopg2 import pool
from models.models import UserPublic, UserLogin, UserCreate, LoginReponse
from utils.generate_jwt import generate_jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import os

load_dotenv()
secret_key = os.getenv("JWT_SECRET")


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

security = HTTPBearer()
@app.get("/protected")
def read_protected(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    
    try:
        jwt.decode(token, key=secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"message": "You are authorized to read this!"}