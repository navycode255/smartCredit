import csv
import random
from faker import Faker

fake = Faker()

tanzania_regions = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera',
    'Katavi', 'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara',
    'Mbeya', 'Morogoro', 'Mtwara', 'Mwanza', 'Njombe', 'Pemba Kusini',
    'Pemba Kaskazini', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga', 'Simiyu',
    'Singida', 'Songwe', 'Tabora', 'Tanga', 'Unguja Kusini', 'Unguja Kaskazini',
    'Zanzibar Central/South', 'Zanzibar North', 'Zanzibar Urban/West'
]

# Generate fake data for customers
customers_data = [
    {
        'customer_id': fake.uuid4(),
        'name': fake.name(),
        'age': random.randint(18, 65),
        'gender': random.choice(['Male', 'Female']),
        'marital_status': random.choice(['Married', 'Single', 'Divorced', 'Widowed']),
        'education_level': random.choice(['High School', 'Bachelor', 'Master', 'PhD']),
        'work_residence': random.choice(tanzania_regions),
        'employment_status': random.choice(['Employed', 'Unemployed', 'Self-employed']),
        'income': random.randint(150000, 3500000)
    }
    for _ in range(500)
]

# Generate data for accounts
accounts_data = []
for customer in customers_data:
    for _ in range(700):
        account_id = fake.uuid4()
        account_data = {
            'account_id': account_id,
            'customer_id': customer['customer_id'],
            'account_type': random.choice(['Savings', 'Checking']),
            'account_number': fake.unique.random_number(digits=10),
            'opening_date': fake.date_between(start_date='-1y', end_date='today'),
            'balance': random.randint(100, 10000)
        }
        accounts_data.append(account_data)

# Generate data for transactions
transactions_data = []
for _ in range(500000):
    transaction_data = {
        'transaction_id': fake.uuid4(),
        'account_id': random.choice(accounts_data)['account_id'],
        'transaction_date': fake.date_between(start_date='-1y', end_date='today'),
        'transaction_type': random.choice(['Deposit', 'Withdrawal']),
        'amount': random.randint(100, 1000)
    }
    transactions_data.append(transaction_data)

# Generate data for credit history
credit_history_data = []
for _ in range(300000):
    credit_history = {
        'customer_id': random.choice(customers_data)['customer_id'],
        'credit_limit': random.randint(5000, 20000),
        'credit_score': random.randint(300, 800)
    }
    credit_history_data.append(credit_history)

# Save data to CSV file
with open('dataset.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=customers_data[0].keys())
    writer.writeheader()
    writer.writerows(customers_data)

with open('dataset.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=accounts_data[0].keys())
    writer.writerows(accounts_data)

with open('dataset.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=transactions_data[0].keys())
    writer.writerows(transactions_data)

with open('dataset.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=credit_history_data[0].keys())
    writer.writerows(credit_history_data)
