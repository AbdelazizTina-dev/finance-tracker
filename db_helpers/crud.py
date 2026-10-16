from sqlalchemy.orm import Session
from db_helpers.database_models import Transaction
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc
from models.models import TransactionType

def get_transactions(type: TransactionType, db: Session, user_id: int):
    query = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(desc(Transaction.created_at)).order_by(desc(Transaction.id))
    
    if type:
        query = query.filter(Transaction.type == type)
        
    return paginate(query)