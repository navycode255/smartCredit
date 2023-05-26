import psycopg2

def create_connection():
    # Connection details
    host = 'localhost'
    dbname = 'credit_risk'
    user = 'navy'
    password = 'navycode255'

    # Connect to PostgreSQL
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    return conn

