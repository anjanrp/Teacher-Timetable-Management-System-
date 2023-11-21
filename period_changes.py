import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
)
cursor = db.cursor()

# SQL statement to create the period_changes table
create_table_sql = """
CREATE TABLE period_changes (
    change_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    subject_name VARCHAR(255) NOT NULL,
    cls_id VARCHAR(30) NOT NULL,
    day VARCHAR(10) NOT NULL,
    period INT NOT NULL,
    action VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute the SQL statement to create the table
cursor.execute(create_table_sql)

# Commit the changes
db.commit()

# Close the database connection
db.close()