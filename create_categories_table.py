import psycopg2

conn = psycopg2.connect(
    dbname="finance_tracker",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE categories (
    id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    created_at TIMESTAMP NOT NULL,
    UNIQUE (user_id, name)
);""")
conn.commit()

cursor.close()
conn.close()
