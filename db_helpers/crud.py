from sqlalchemy.orm import Session
from db_helpers.database_models import Transaction

def get_transactions(db: Session, user_id: int):
    print("USER ID = ", user_id)
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()
