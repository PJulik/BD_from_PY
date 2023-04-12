import psycopg2
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_book;
        DROP TABLE clients;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_book(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id),
            phone_number VARCHAR(10)
        );
        """)
        conn.commit()

        cur.execute("""
        INSERT INTO clients(first_name, last_name, email) VALUES
        ('Анна', 'Павлова', 'pavlova@mail.ru'),
        ('Борис', 'Корчагин', 'korchagin@mail.ru');
        """)

        cur.execute("""
        INSERT INTO phone_book(client_id, phone_number) VALUES 
        (1, '9116758945'),
        (2, '9526593457');
        """)

        conn.commit()

def add_client(conn, first_name, last_name, email, phone_number = None):
    with conn.cursor() as cur:
        cur.execute("""SELECT email FROM clients WHERE email = %s""", (email,))
        if cur.fetchone() is None:
            cur.execute("""INSERT INTO clients(first_name, last_name, email) VALUES (%s, %s, %s);""", (first_name, last_name, email))
            cur.execute("""INSERT INTO phone_book(phone_number) VALUES (%s);""", (phone_number,))
            conn.commit()
            print('Вы успешно зарегистрировались!')
        else:
            print(f'Пользователь с таким email {email} уже существует!')

def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""SELECT client_id FROM phone_book WHERE client_id=%s;""", (client_id,))
        if cur.fetchone() is None:
            print('Нет такого клиента')
        else:
            cur.execute("""
            INSERT INTO phone_book(client_id, phone_number) VALUES (%s, %s);""", (client_id, phone_number))
            conn.commit()
            print('Номер добавлен')

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients SET first_name=%s WHERE client_id=%s;""", (first_name, client_id,))
        cur.execute("""
        UPDATE clients SET last_name=%s WHERE client_id=%s;""", (last_name, client_id,))
        cur.execute("""
        UPDATE clients SET email=%s WHERE client_id=%s;""", (email, client_id,))
        cur.execute("""
        UPDATE phone_book SET phone_number=%s WHERE client_id=%s;""", (phone_number, client_id,))

def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_book WHERE client_id=%s;""", (client_id,))

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_book WHERE client_id=%s;""", (client_id,))
        cur.execute("""
        DELETE FROM clients WHERE client_id=%s;""", (client_id,))


def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c LEFT JOIN phone_book pb ON c.client_id = pb.client_id WHERE c.first_name=%s;""", (first_name,))
            print(cur.fetchall())
        if last_name is not None:
            cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c LEFT JOIN phone_book pb ON c.client_id = pb.client_id WHERE c.last_name=%s;""",
            (last_name,))
            print(cur.fetchall())
        if email is not None:
            cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c LEFT JOIN phone_book pb ON c.client_id = pb.client_id WHERE c.email=%s;""",
            (email,))
            print(cur.fetchall())
        if phone_number is not None:
            cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c LEFT JOIN phone_book pb ON c.client_id = pb.client_id WHERE pb.phone_number=%s;""",
            (phone_number,))
            print(cur.fetchall())

with psycopg2.connect(database='Clients', user='postgres', password='...') as conn:
    add_client(conn, '...', '...', '...')
    add_phone(conn, '...', '...')
    change_client(conn, '...', '...', '...', '...', '...')
    delete_phone(conn, '...', '...')
    delete_client(conn, '...')
    find_client(conn, '...', '...', '...', '...')

conn.close()



