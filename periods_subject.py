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

# Query to extract unique sub_name values from the periods table
select_query = "SELECT DISTINCT sub_name FROM periods"


# Execute the query
cursor.execute(select_query)

# Fetch all unique sub_name values
unique_sub_names = [row[0] for row in cursor.fetchall()]

# Generate unique sub_id values for each sub_name
sub_id_mapping = {sub_name: f"SUB{index + 1}" for index, sub_name in enumerate(unique_sub_names)}

# Query to insert data into the subject table
insert_query = "INSERT INTO subject (sub_id, sub_name, sub_desc) VALUES (%s, %s, %s)"

# Execute the query for each sub_name
for sub_name in unique_sub_names:
    sub_id = sub_id_mapping[sub_name]
    sub_desc = f"Description for {sub_name}"  # Provide an appropriate description
    cursor.execute(insert_query, (sub_id, sub_name, sub_desc))

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
