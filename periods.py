import mysql.connector


# Replace with your MySQL database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "anjan1234.",
    "database": "TEACHER_TIMETABLE_SYSTEM"
}

# Define the SQL command to create the "periods" table
create_periods_table = [

"""
CREATE TABLE periods (
    t_name VARCHAR(50) NOT NULL,
    cls_id VARCHAR(30),
    sub_name VARCHAR(30),
    day VARCHAR(10) NOT NULL,
    period INT NOT NULL
);
""",

"""
    ALTER TABLE periods
    ADD FOREIGN KEY (cls_id) REFERENCES class(cls_id);
""",

"""
    ALTER TABLE periods
    ADD FOREIGN KEY (sub_name) REFERENCES subject(sub_name);
"""
]
# Connect to the MySQL server
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

try:
    # Execute the SQL command to create the "periods" table
    cursor.execute(create_periods_table)

    # Commit the changes to the database
    connection.commit()
    print("Table 'periods' created successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
