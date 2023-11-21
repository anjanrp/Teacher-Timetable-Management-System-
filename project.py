import mysql.connector

# Replace with your MySQL database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "anjan1234.",
    "database": "TEACHER_TIMETABLE_SYSTEM"
}

# Connect to the MySQL server
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL queries
cursor = connection.cursor() 

# Define the list of SQL commands to execute
sql_commands = [
    """
    CREATE TABLE login(
        login_id varchar(30) primary key,
        login_usrnm varchar(50),
        login_passwd varchar(50)
    );
    """,
    
    """
    CREATE TABLE teacher(
        t_id varchar(30) primary key,
        t_name varchar(50),
        login_id varchar(30)
    );
    """,
    
    """
    CREATE TABLE class(
        cls_id varchar(30) primary key,
        cls_desc varchar(50)
    );
    """,
    """
    CREATE TABLE subject(
        sub_id varchar(30) primary key,
        sub_name varchar(30),
        sub_desc varchar(50)
    );
    """
]

try:
    # Execute each SQL command one by one
    for sql_command in sql_commands:
        cursor.execute(sql_command)

    # Commit the changes to the database
    connection.commit()
    print("SQL commands executed successfully. Tables created.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
