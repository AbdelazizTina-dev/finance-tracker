from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import add_pagination, Page
from db_helpers.crud import get_transactions
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db_helpers.database_models import Transaction as TransactionAlchemy, Category as CategoryAlchemy, User as UserAlchemy
from models.models import UserPublic, UserLogin, UserCreate, LoginReponse, CategoryCreate, Category, TransactionCreate, TransactionType, Transaction, TransactionPatch
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

app = FastAPI()
add_pagination(app)

@app.get("/")
def read_root():
    return {"message": "Hello Backend!"}

@app.post("/register", response_model=UserPublic)
def register_user(user: UserCreate,  db: Session = Depends(get_db)):
    pwd_bytes = user.password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("UTF-8")
    new_user = UserAlchemy(
        created_at=datetime.now(),
        email=user.email,
        username=user.username,
        hashed_password=hashed
    )
    
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already taken!")

    db.refresh(new_user)
    
    return new_user

DUMMY_HASH = bcrypt.hashpw(b"not-a-real-password", bcrypt.gensalt())

@app.post("/login", response_model=LoginReponse)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserAlchemy).filter(UserAlchemy.email == user_credentials.email).first()

    if user is not None:
        hash_to_check = user.hashed_password.encode("utf-8")
    else:
        hash_to_check = DUMMY_HASH

    is_password_correct = bcrypt.checkpw(user_credentials.password.encode("utf-8"), hash_to_check)

    if user is not None and is_password_correct:
        return LoginReponse(jwt=generate_jwt(user.id))

    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/categories", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    new_category = CategoryAlchemy(
        created_at=datetime.now(),
        user_id=user_id,
        name=category.name
    )
    
    try:
        db.add(new_category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category Name already taken!")

    db.refresh(new_category)
    
    return new_category

@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    if transaction.category_id is not None:
        category = db.query(CategoryAlchemy).filter(CategoryAlchemy.id == transaction.category_id).filter(CategoryAlchemy.user_id == user_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
    new_tx = TransactionAlchemy(
        user_id=user_id,
        created_at=datetime.now(),
        amount=transaction.amount,
        category_id=transaction.category_id,
        type=transaction.type,
        description=transaction.description
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    
    return new_tx

@app.get("/transactions", response_model=Page[Transaction])
def get_transactions_list(type: TransactionType | None = None, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_transactions(type, db, user_id)

@app.patch("/transactions/{id}", response_model=Transaction)
def patch_transaction(id: int, payload: TransactionPatch,db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    transaction = db.query(TransactionAlchemy).filter(TransactionAlchemy.user_id == user_id).filter(TransactionAlchemy.id == id).first()
    
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    data_dict = payload.model_dump(exclude_unset=True)
    
    if ("amount" in data_dict and data_dict["amount"] is None):
        raise HTTPException(status_code=422, detail="amount cannot be null")
    
    for key, value in data_dict.items():
        setattr(transaction, key, value)

    db.commit()
    
    return transaction
