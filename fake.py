import random
from faker import Faker
from database import create_connection, close_connection

fake = Faker()

tanzania_regions = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera',
    'Katavi', 'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara',
    'Mbeya', 'Morogoro', 'Mtwara', 'Mwanza', 'Njombe', 'Pemba Kusini',
    'Pemba Kaskazini', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga', 'Simiyu',
    'Singida', 'Songwe', 'Tabora', 'Tanga', 'Unguja Kusini', 'Unguja Kaskazini',
    'Zanzibar Central/South', 'Zanzibar North', 'Zanzibar Urban/West'
]

# Create database connection
conn = create_connection()
cursor = conn.cursor()

# Create customers table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id UUID PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER,
        gender VARCHAR(10),
        marital_status VARCHAR(20),
        education_level VARCHAR(50),
        work_residence VARCHAR(100),
        employment_status VARCHAR(50),
        income INTEGER
    )
''')

# Generate fake data for customers table
customers_data = [
    (
        fake.uuid4(),
        fake.name(),
        random.randint(18, 65),
        random.choice(['Male', 'Female']),
        random.choice(['Married', 'Single', 'Divorced', 'Widowed']),
        random.choice(['High School', 'Bachelor', 'Master', 'PhD']),
        random.choice(tanzania_regions),
        random.choice(['Employed', 'Unemployed', 'Self-employed']),
        random.randint(350000, 3500000)
    )
    for _ in range(500)
]

# Insert customers data into customers table
cursor.executemany('''
    INSERT INTO customers (customer_id, name, age, gender, marital_status, education_level, work_residence, employment_status, income)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
''', customers_data)

# Define the table schemas (including relationships)
table_schemas = {
    'accounts': '''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id UUID PRIMARY KEY,
            customer_id UUID,
            account_type VARCHAR(20),
            account_number VARCHAR(50),
            opening_date DATE,
            balance NUMERIC(10, 2),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''',
    'transactions': '''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id UUID PRIMARY KEY,
            account_id UUID,
            transaction_date DATE,
            transaction_type VARCHAR(20),
            amount NUMERIC(10, 2),
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        )
    ''',
    'credit_history': '''
        CREATE TABLE IF NOT EXISTS credit_history (
            customer_id UUID PRIMARY KEY,
            credit_limit NUMERIC(10, 2),
            credit_score INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    '''
}

# Create additional tables
for table_name, table_schema in table_schemas.items():
    cursor.execute(table_schema)

# Generate and insert data for accounts
accounts_data = [
    (
        fake.uuid4(),
        random.choice(customers_data)[0],
        random.choice(['Savings', 'Checking']),
        fake.credit_card_number(),
        fake.date_between(start_date='-10y', end_date='today'),
        random.randint(10000, 25000000)
    )
    for _ in range(700)
]

cursor.executemany('''
    INSERT INTO accounts (account_id, customer_id, account_type, account_number, opening_date, balance)
    VALUES (%s, %s, %s, %s, %s, %s)
''', accounts_data)

# Generate and insert data for transactions
transactions_data = [
    (
        fake.uuid4(),
        random.choice(accounts_data)[0],
        fake.date_between(start_date='-2y', end_date='today'),
        random.choice(['Deposit', 'Withdrawal', 'Transfer']),
        random.randint(10000, 15000000)
    )
    for _ in range(500000)
]

cursor.executemany('''
    INSERT INTO transactions (transaction_id, account_id, transaction_date, transaction_type, amount)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
''', transactions_data)

# Generate and insert data for credit history
credit_history_data = [
    (
        random.choice(customers_data)[0],
        random.randint(1000, 50000),
        random.randint(300, 850)
    )
    for _ in range(300000)
]

cursor.executemany('''
    INSERT INTO credit_history (customer_id, credit_limit, credit_score)
    VALUES (%s, %s, %s)
    ON CONFLICT DO NOTHING
''', credit_history_data)

# Commit the changes
conn.commit()

# Close the connection
close_connection(conn)
