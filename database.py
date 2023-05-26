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

# Query for inserting data from the database tables
def execute_query(conn, query):
    # Create a cursor object
    cur = conn.cursor()

    # Execute the query
    cur.execute(query)

    # Fetch all rows
    rows = cur.fetchall()

    # Close the cursor
    cur.close()

    return rows

# Query for creating-table in database
def create_table(query):
    # Create a connection
    conn = create_connection()

    # Execute the table creation query
    execute_query(conn, query)

    # Close the connection
    conn.close()

# Query for 
def display_data(query):
# Create a connection
    conn = create_connection()

    # Execute the data display query
    rows = execute_query(conn, query)

    # Display the fetched data
    for row in rows:
        print(row)

    # Close the connection
    conn.close()