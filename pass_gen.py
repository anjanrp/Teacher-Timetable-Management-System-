import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
)
cursor = db.cursor()


# Function to retrieve unique t_names from the 'periods' table
def get_unique_t_names():
    query = "SELECT DISTINCT t_name FROM periods"
    cursor.execute(query)
    unique_t_names = [row[0] for row in cursor.fetchall()]
    return unique_t_names


# Get the list of unique t_names
t_name_list = get_unique_t_names()

# Generate passwords and login IDs
passwords = [t_name.replace(" ", "").lower() + "123" for t_name in t_name_list]
login_ids = [str(i).zfill(2) for i in range(1, len(t_name_list) + 1)]

# Store usernames, passwords, and login IDs in the login table
for i in range(len(t_name_list)):
    username = t_name_list[i]
    password = passwords[i]
    login_id = login_ids[i]

    # Insert the data into the login table
    query = "INSERT INTO login (login_id, login_usrnm, login_passwd) VALUES (%s, %s, %s)"
    values = (login_id, username, password)
    cursor.execute(query, values)

# Commit changes and close the database connection
db.commit()
db.close()