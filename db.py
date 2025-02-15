import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Katre@123",  # Replace with your MySQL password
        database="astrology"
    )
    return conn
