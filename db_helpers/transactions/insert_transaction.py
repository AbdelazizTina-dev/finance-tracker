from models.models import TransactionCreate, Transaction
from datetime import datetime

def insert_transaction(connection_pool, user_id: int, payload: TransactionCreate):
    conn = connection_pool.getconn()

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO transactions(
        created_at,
        user_id,
        category_id,
        amount,
        description
    ) VALUES(%s, %s, %s, %s, %s)
    RETURNING id, user_id, category_id, amount, description, created_at;""",
        (datetime.now(), user_id, payload.category_id, payload.amount, payload.description))
    
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    connection_pool.putconn(conn)
    
    (id, user_id, category_id, amount, description, created_at) = row
    return Transaction(id=id, user_id=user_id, category_id=category_id, amount=amount, description=description, created_at=created_at)