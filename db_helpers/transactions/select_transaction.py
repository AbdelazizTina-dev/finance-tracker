from models.models import Transaction

def select_transaction(connection_pool, id: int) -> Transaction | None:
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM transactions WHERE id = %s;""",
        (id,)
    )
    transaction = cursor.fetchone()
    if transaction is None:
        return None
    (id, user_id, category_id, amount, description, created_at) = transaction
    transaction = Transaction(id = id, category_id = category_id, amount = amount, description = description, user_id = user_id, created_at = created_at)
    cursor.close()
    connection_pool.putconn(conn)
    return transaction
