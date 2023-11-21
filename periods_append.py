import mysql.connector

# Function to execute MySQL commands
def execute_mysql_commands(mysql_commands, connection):
    try:
        cursor = connection.cursor()

        for cmd in mysql_commands:
            cursor.execute(cmd)

        connection.commit()

    except Exception as e:
        print(f"Error executing MySQL commands: {str(e)}")
    finally:
        cursor.close()

# Connect to your MySQL database
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password ="anjan1234.",
        database = "TEACHER_TIMETABLE_SYSTEM"
    )

    # Specify the path to your .txt file containing SQL commands
    txt_file_path = "periods_data.txt"

    # Read SQL commands from the .txt file
    with open(txt_file_path, "r") as file:
        mysql_commands = [line.strip() for line in file if line.strip()]

    # Execute MySQL commands
    if mysql_commands:
        execute_mysql_commands(mysql_commands, connection)
        print("MySQL commands executed successfully.")
    else:
        print("No MySQL commands found in the .txt file.")
except Exception as e:
    print(f"Error connecting to the MySQL database: {str(e)}")
finally:
    if 'connection' in locals():
        connection.close()