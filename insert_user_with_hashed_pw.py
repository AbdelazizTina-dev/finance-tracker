import bcrypt
from datetime import datetime


def insert_user(connection_pool, username: str, email: str, password):
    pwd_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("UTF-8")

    conn = connection_pool.getconn()

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users(  
        created_at,
        username,
        email,
        hashed_password
    ) VALUES(
        %s, %s, %s, %s
    );""", (datetime.now(), username, email, hashed))
    conn.commit()

    cursor.close()
    connection_pool.putconn(conn)
