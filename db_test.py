import psycopg2

conn = psycopg2.connect(
    dbname="finance_tracker",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
result = cursor.fetchone()
print(result)

cursor.close()
conn.close()
