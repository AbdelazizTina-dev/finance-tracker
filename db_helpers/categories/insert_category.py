from models.models import CategoryCreate
from datetime import datetime

def insert_category(connection_pool, user_id: int, payload: CategoryCreate):
    conn = connection_pool.getconn()

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO categories(
        created_at,
        user_id,
        name
    ) VALUES(
        %s, %s, %s
    );""", (datetime.now(), user_id, payload.name)
    )
    conn.commit()

    cursor.close()
    connection_pool.putconn(conn)
