import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anjan1234.",
    database="TEACHER_TIMETABLE_SYSTEM"
)

cursor = db.cursor()

# Create timings table if not exists
create_timings_table = """
CREATE TABLE IF NOT EXISTS timings (
    period INT PRIMARY KEY,
    start_time TIME,
    end_time TIME
)
"""
cursor.execute(create_timings_table)

# Insert timings for periods
timings_data = [
    (1, '08:30:00', '09:00:00'),
    (2, '09:00:00', '09:30:00'),
    (3, '09:30:00', '10:00:00'),
    (4, '10:00:00', '10:30:00'),
    (5, '10:30:00', '11:00:00'),
    (6, '11:00:00', '11:30:00'),
    (7, '12:30:00', '01:00:00'),
    (8, '01:00:00', '01:30:00'),
    (9, '01:30:00', '02:00:00'),
    (10, '02:00:00', '02:30:00')
]

insert_query = "INSERT INTO timings (period, start_time, end_time) VALUES (%s, %s, %s)"
cursor.executemany(insert_query, timings_data)

# Commit the changes and close the connection
db.commit()
cursor.close()
db.close()
