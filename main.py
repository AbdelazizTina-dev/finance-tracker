from fastapi import FastAPI
from pydantic import BaseModel
from insert_user_with_hashed_pw import insert_user
from contextlib import asynccontextmanager
from psycopg2 import pool

class User(BaseModel):
    username: str
    email: str
    password: str

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
    return {"message": "Hello, backend world"}

@app.post("/register")
def register_user(user: User):
    insert_user(app.state.pool, user.username, user.email, user.password)
    return user
