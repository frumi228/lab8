import psycopg2
from faker import Faker
from random import choice, randint

fake = Faker('uk_UA')

# Підключення до бази даних
connection = psycopg2.connect(
    dbname="locomotive_db",
    user="admin",
    password="password",
    host="localhost",
    port=5432
)
cursor = connection.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE main_app_locomotive (
    registration_number SERIAL PRIMARY KEY,
    depot VARCHAR(50) NOT NULL,
    locomotive_type VARCHAR(50) CHECK (locomotive_type IN ('вантажний', 'пасажирський')),
    manufacture_year INT NOT NULL CHECK (manufacture_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE))
);

CREATE TABLE main_app_brigade (
    brigade_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL
);

CREATE TABLE main_app_worker (
    worker_id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    brigade_id INT REFERENCES main_app_brigade(brigade_id),
    is_leader BOOLEAN DEFAULT FALSE,
    birth_date DATE NOT NULL
);

CREATE TABLE main_app_repair (
    repair_id SERIAL PRIMARY KEY,
    locomotive_id INT REFERENCES main_app_locomotive(registration_number) ON DELETE CASCADE,
    repair_type VARCHAR(50) CHECK (repair_type IN ('поточний', 'технічне обслуговування', 'позаплановий')),
    start_date DATE NOT NULL,
    repair_days INT NOT NULL CHECK (repair_days > 0),
    daily_cost DECIMAL(10, 2) NOT NULL,
    brigade_id INT REFERENCES main_app_brigade(brigade_id)
);
""")

# Додавання даних у таблиці
brigades = []
for _ in range(3):
    phone = fake.phone_number()[:15]
    cursor.execute("INSERT INTO main_app_brigade (phone_number) VALUES (%s) RETURNING brigade_id;", (phone,))
    brigades.append(cursor.fetchone()[0])

workers = []
for brigade_id in brigades:
    for _ in range(3):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.first_name()
        birth_date = fake.date_of_birth(minimum_age=25, maximum_age=60)
        is_leader = choice([True, False])
        cursor.execute("""
        INSERT INTO main_app_worker (first_name, last_name, middle_name, brigade_id, is_leader, birth_date)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING worker_id;
        """, (first_name, last_name, middle_name, brigade_id, is_leader, birth_date))
        workers.append(cursor.fetchone()[0])

depots = ['Фастів', 'Козятин', 'П’ятихатки']
locomotives = []
for _ in range(9):
    depot = choice(depots)
    locomotive_type = choice(['вантажний', 'пасажирський'])
    manufacture_year = randint(1900, 2023)
    cursor.execute("""
    INSERT INTO main_app_locomotive (depot, locomotive_type, manufacture_year)
    VALUES (%s, %s, %s) RETURNING registration_number;
    """, (depot, locomotive_type, manufacture_year))
    locomotives.append(cursor.fetchone()[0])

for _ in range(11):
    locomotive_id = choice(locomotives)
    repair_type = choice(['поточний', 'технічне обслуговування', 'позаплановий'])
    start_date = fake.date_this_year()
    repair_days = randint(1, 14)
    daily_cost = round(randint(100, 1000) + fake.random.random(), 2)
    brigade_id = choice(brigades)
    cursor.execute("""
    INSERT INTO main_app_repair (locomotive_id, repair_type, start_date, repair_days, daily_cost, brigade_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (locomotive_id, repair_type, start_date, repair_days, daily_cost, brigade_id))

connection.commit()
cursor.close()
connection.close()
print("Таблиці створені!")
