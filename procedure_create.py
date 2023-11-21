import mysql.connector

# Database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "anjan1234.",
    "database": "TEACHER_TIMETABLE_SYSTEM"
}

# SQL code to create the stored procedure
create_procedure_sql = """
CREATE PROCEDURE GenerateTimetableSummary(IN username VARCHAR(255))
BEGIN
    DECLARE total_classes INT;
    DECLARE total_subjects INT;
    DECLARE total_periods INT;
    
    SELECT COUNT(DISTINCT cls_id) INTO total_classes FROM periods WHERE t_name = username;
    SELECT COUNT(DISTINCT sub_name) INTO total_subjects FROM periods WHERE t_name = username;
    SELECT COUNT(*) INTO total_periods FROM periods WHERE t_name = username;
    
    SELECT total_classes, total_subjects, total_periods;
END;
"""

try:
    # Connect to the database
    connection = mysql.connector.connect(**db_config)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the SQL code to create the stored procedure
    cursor.execute(create_procedure_sql)

    # Commit the changes to the database
    connection.commit()

    print("Stored procedure 'GenerateTimetableSummary' created successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and database connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()