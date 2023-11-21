import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anjan1234.",
    database="TEACHER_TIMETABLE_SYSTEM"
)

# Create a cursor
cursor = db.cursor()

# Query to insert data into the teacher table from the login table with adjusted t_id
insert_query = """
    INSERT INTO teacher (t_id, t_name, login_id)
    SELECT CONCAT(LEFT(login_usrnm, 2), login_id), login_usrnm, login_id
    FROM login
"""

# Execute the query
cursor.execute(insert_query)

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
