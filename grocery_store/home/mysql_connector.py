import mysql.connector

def get_database_connection():
    # Establish connection to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database_name'
    )
    return conn