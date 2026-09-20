from models.models import Category

def select_category(connection_pool, name: str, user_id: int) -> Category | None:
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM categories WHERE name = %s AND user_id = %s;""",
        (name, user_id)
    )
    category = cursor.fetchone()
    if category is None:
        return None
    (id, user_id, name, type, created_at) = category
    category = Category(id = id, name = name, type = type, user_id = user_id, created_at = created_at)
    cursor.close()
    connection_pool.putconn(conn)
    return category
