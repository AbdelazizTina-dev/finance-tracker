from models import User

def select_user(connection_pool, email: str) -> User | None:
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE email = %s;""",
        (email,)
    )
    user = cursor.fetchone()
    if user is None:
        return None
    (id, created_at, updated_at, username, user_email, password) = user
    user = User(id = id, username = username, password=password, created_at = created_at, updated_at=updated_at, email=user_email)
    cursor.close()
    connection_pool.putconn(conn)
    return user
