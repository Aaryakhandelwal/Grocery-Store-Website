import mysql.connector

def get_database_connection():
    # Establish connection to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aarya-123',
        database='dbms_project'
    )
    return conn