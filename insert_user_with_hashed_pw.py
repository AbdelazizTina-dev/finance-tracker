import psycopg2
import bcrypt
from datetime import datetime

conn = psycopg2.connect(
    dbname="finance_tracker",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

password = b"testpassword1234"
hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("UTF-8")

cursor = conn.cursor()
cursor.execute("""INSERT INTO users(  
    created_at,
    username,
    email,
    hashed_password
) VALUES(
    %s, %s, %s, %s
);""", (datetime.now(), "test_user", "test@email.com", hashed))
conn.commit()
cursor.execute("SELECT * FROM users;")
result = cursor.fetchone()
print(result)

cursor.close()
conn.close()
