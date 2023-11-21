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

# Query to extract unique cls_id values from the periods table
select_query = "SELECT DISTINCT cls_id FROM periods"

# Execute the query
cursor.execute(select_query)

# Fetch all unique cls_id values
unique_cls_ids = [row[0] for row in cursor.fetchall()]

# Sort the cls_id values
sorted_cls_ids = sorted(unique_cls_ids)

# Query to insert data into the class table
insert_query = "INSERT INTO class (cls_id, cls_desc) VALUES (%s, %s)"

# Execute the query for each cls_id
for cls_id in sorted_cls_ids:
    cls_desc = f"Class {cls_id}"
    cursor.execute(insert_query, (cls_id, cls_desc))

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
