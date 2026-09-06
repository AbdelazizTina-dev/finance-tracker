import psycopg2

conn = psycopg2.connect(
    dbname="finance_tracker",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE users(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL
);""")
conn.commit()
cursor.execute("SELECT * FROM users;")
result = cursor.fetchone()
print(result)

cursor.close()
conn.close()
