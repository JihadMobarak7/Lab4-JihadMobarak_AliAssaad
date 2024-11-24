import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection successful")
    except Error as e:
        print(f"Failed to create a connection: {e}")
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement using a connection."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()  # Explicitly commit changes
        print("Table created successfully")
    except Error as e:
        print(f"Failed to create table: {e}")

def main():
    database = "school_management.db"

    sql_create_students_table = """CREATE TABLE IF NOT EXISTS Students (
                                    student_id TEXT PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    age INTEGER,
                                    email TEXT NOT NULL UNIQUE
                                    );"""

    sql_create_instructors_table = """CREATE TABLE IF NOT EXISTS Instructors (
                                      instructor_id TEXT PRIMARY KEY,
                                      name TEXT NOT NULL,
                                      email TEXT NOT NULL UNIQUE
                                      );"""
    
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_instructors_table)
        conn.close()  # Explicitly close the connection
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()