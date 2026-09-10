from models import User

def select_user(connection_pool, email: str) -> User | None:
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""SELECT email, hashed_password, username FROM users WHERE email = %s;""",
        (email,)
    )
    result = cursor.fetchone()
    if result is None:
        return None
    (user_email, user_pw, username) = result
    user = User(username=username, email=user_email, password=user_pw)
    cursor.close()
    connection_pool.putconn(conn)
    return user
