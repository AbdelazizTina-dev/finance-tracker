import psycopg2

conn = psycopg2.connect(
    dbname="finance_tracker",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE transactions (
    id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL
);""")
conn.commit()

cursor.close()
conn.close()
