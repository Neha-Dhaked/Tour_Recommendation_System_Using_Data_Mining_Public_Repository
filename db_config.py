import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Your MySQL password
        database="newtrs2"
    )
