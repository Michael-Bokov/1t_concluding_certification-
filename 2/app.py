import psycopg2
import os

def create_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                department VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()

def insert_data(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO employees (name, age, department)
            VALUES
            ('Alice', '25', 'code:New York'),
            ('Test1','00000','code:000'),
            ('Test2','00000','code:000'),
            ('Bob','30', 'code:Los Angeles'),
            ('Charlie','35','Chicago'),
            ('David', '40', 'Houston'),
            ('Eve', '45', 'Phoenix'),
            ('Alice2', 30, 'HR'),
            ('Bob2', 25, 'Engineering'),
            ('Charlie', 35, 'Finance');
        """)
        conn.commit()

def fetch_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM employees;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def main():
    conn = create_connection()
    create_table(conn)
    insert_data(conn)
    fetch_data(conn)
    conn.close()

if __name__ == '__main__':
    main()
