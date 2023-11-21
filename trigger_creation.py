import mysql.connector

# Replace these values with your actual database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "anjan1234.",
    "database": "TEACHER_TIMETABLE_SYSTEM"
}

try:
    # Connect to the MySQL database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # SQL statement to create the trigger
    trigger_sql = """
    CREATE TRIGGER log_period_changes
    AFTER INSERT ON periods
    FOR EACH ROW
    BEGIN
        INSERT INTO period_changes (username, subject_name, cls_id, day, period, action, timestamp)
        VALUES (NEW.t_name, NEW.sub_name, NEW.cls_id, NEW.day, NEW.period, 'INSERT', NOW());
    END;
    """

    # Execute the trigger creation SQL statement
    cursor.execute(trigger_sql)

    # Commit the changes
    db.commit()

    print("Trigger created and implemented successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the database connection
    if db.is_connected():
        cursor.close()
        db.close()