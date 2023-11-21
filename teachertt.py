import mysql.connector
import streamlit as st
import pandas as pd


# Function to check the username and password
def check_login(username, password):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    query = f"SELECT * FROM login WHERE login_usrnm = '{username}' AND login_passwd = '{password}'"
    cursor.execute(query)
    user_data = cursor.fetchone()

    db.close()  # Close the database connection

    return user_data is not None


# Function to sign up a new teacher
def signup_teacher(login_id, login_usrnm, password):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    # Check if the teacher with the same ID already exists
    query = f"SELECT * FROM login WHERE login_id = '{login_id}'"
    cursor.execute(query)
    existing_teacher = cursor.fetchone()

    if existing_teacher:
        st.warning("Signup failed. Teacher with the same ID already exists.")
    else:
        # If the teacher doesn't exist, insert the new teacher data
        insert_query = f"INSERT INTO login (login_id, login_usrnm, login_passwd) VALUES ('{login_id}', '{login_usrnm}', '{password}')"
        cursor.execute(insert_query)
        db.commit()
        st.success("Signup successful! You can now log in.")

    db.close()


# Function to get unique subject names for the user
def get_unique_subjects(username):
    db = mysql.connector.connect(
       host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    query = f"SELECT DISTINCT sub_name FROM periods WHERE t_name = '{username}'"
    cursor.execute(query)
    unique_subjects = [row[0] for row in cursor.fetchall()]

    db.close()  # Close the database connection

    return unique_subjects

def display_timings():
    # Replace these values with your actual MySQL server configuration
    host = "localhost"
    user = "root"
    password = "anjan1234."
    database = "TEACHER_TIMETABLE_SYSTEM"

    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        cursor = db.cursor()

        # Fetch timings from the 'timings' table
        cursor.execute("SELECT * FROM timings")
        timings_data = cursor.fetchall()

        # Convert the 'Start Time' and 'End Time' columns to strings
        timings_data = [(period, str(start_time), str(end_time)) for period, start_time, end_time in timings_data]

        # Display timings
        st.write("Timings:")
        st.write(pd.DataFrame(timings_data, columns=["Period", "Start Time", "End Time"]))

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()


# Function to get the timetable grid for a specific subject
def get_timetable_grid(username, subject_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = list(range(1, 11))

    # Initialize the timetable grid with empty cells
    timetable = [["" for _ in range(10)] for _ in range(5)]

    query = f"SELECT cls_id, day, period FROM periods WHERE t_name = '{username}' AND sub_name = '{subject_name}'"
    cursor.execute(query)
    subject_info = cursor.fetchall()

    for row in subject_info:
        cls_id, day, period = row
        day_index = days.index(day)
        period_index = period - 1
        timetable[day_index][period_index] = cls_id

    db.close()  # Close the database connection

    return timetable


# Function to add data to periods and update period_changes
def add_period_data(username, subject_name, cls_id, day, period):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anjan1234.",
        database="TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    try:
        # Check if an entry already exists for the given cls_id, day, and period
        existing_query = f"SELECT * FROM periods WHERE t_name = '{username}' AND sub_name = '{subject_name}' AND cls_id = '{cls_id}' AND day = '{day}' AND period = {period}"
        cursor.execute(existing_query)
        existing_entry = cursor.fetchone()

        if existing_entry:
            st.warning("Data entry not possible. Entry already exists for the given Class ID, Day, and Period.")
        else:
            # Check if there is any other entry for the same day and period
            conflicting_query = f"SELECT * FROM periods WHERE t_name = '{username}' AND sub_name = '{subject_name}' AND day = '{day}' AND period = {period}"
            cursor.execute(conflicting_query)
            conflicting_entry = cursor.fetchone()

            if conflicting_entry:
                st.warning("Data entry not possible. Another entry exists for the same Day and Period.")
            else:
                # If there are no conflicts, insert the new data into the periods table
                insert_query = f"INSERT INTO periods (t_name, sub_name, cls_id, day, period) VALUES ('{username}', '{subject_name}', '{cls_id}', '{day}', {period})"
                cursor.execute(insert_query)
                db.commit()

                # Now, update the period_changes table
                update_query = f"INSERT INTO period_changes (username, subject_name, cls_id, day, period, action) VALUES ('{username}', '{subject_name}', '{cls_id}', '{day}', {period}, 'UPDATE')"
                cursor.execute(update_query)
                db.commit()

                # Rerun the script to update the timetable grid
                st.experimental_rerun()

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    finally:
        cursor.close()
        db.close()  # Close the database connection



# Function to delete data from periods
def delete_period_data(username, subject_name, day, period):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
       password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    try:
        # Nested query: Check if an entry exists for the given day and period
        existing_query = f"SELECT * FROM periods WHERE t_name = '{username}' AND sub_name = '{subject_name}' AND day = '{day}' AND period = {period}"
        cursor.execute(existing_query)
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Nested query: Delete the data
            delete_query = f"DELETE FROM periods WHERE t_name = '{username}' AND sub_name = '{subject_name}' AND day = '{day}' AND period = {period}"
            cursor.execute(delete_query)
            db.commit()
            st.success("Data deleted successfully!")

            # Explicitly close the cursor to avoid "Unread result found" error
            cursor.close()

            # Rerun the script to update the timetable grid
            st.experimental_rerun()
        else:
            st.warning("Data deletion not possible. No entry found for the given Day and Period.")

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    db.close()  # Close the database connection


# Function to generate timetable summary
def generate_timetable_summary(username):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    try:
        # Call the stored procedure to generate the summary
        cursor.callproc("GenerateTimetableSummary", (username,))
        results = cursor.stored_results()

        for result in results:
            summary = result.fetchall()[0]

            total_classes, total_subjects, total_periods = summary

            st.write(f"Total Classes: {total_classes}")
            st.write(f"Total Subjects: {total_subjects}")
            st.write(f"Total Assigned Periods: {total_periods}")

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    db.close()


# Function to get the day with minimum and maximum number of periods for the logged-in teacher
def get_min_max_periods_days(username):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anjan1234.",
        database="TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    try:
        # Use an aggregate query to get the day with minimum and maximum number of periods
        query = f"""
        SELECT day,
               MIN(total_periods) AS min_periods,
               MAX(total_periods) AS max_periods
        FROM (
            SELECT day, COUNT(DISTINCT period) AS total_periods
            FROM periods
            WHERE t_name = '{username}'
            GROUP BY day
        ) AS day_total_periods
        GROUP BY day
        ORDER BY max_periods DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        st.write("Day with Minimum and Maximum Number of Periods:")
        st.write(f"Maximum periods: {results[0][0]}")
        st.write(f"Minimum periods: {results[-1][0]}")

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    db.close()


def display_class_subjects(cls_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "anjan1234.",
    database = "TEACHER_TIMETABLE_SYSTEM"
    )
    cursor = db.cursor()

    try:
        # Modified SQL query with a WHERE clause to filter by cls_id
        query = f"""
        SELECT
            c.cls_id,
            c.cls_desc,
            GROUP_CONCAT(DISTINCT p.sub_name) AS subjects
        FROM
            class c
        LEFT JOIN
            periods p ON c.cls_id = p.cls_id
        WHERE
            c.cls_id = '{cls_id}'
        GROUP BY
            c.cls_id, c.cls_desc;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Display the results in a DataFrame
        columns = ["Class ID", "Class Description", "Subjects"]
        df = pd.DataFrame(results, columns=columns)

        if df.empty:
            st.warning(f"No data found for Class ID: {cls_id}")
        else:
            st.dataframe(df)

    except mysql.connector.Error as err:
        st.warning(f"Error: {err}")

    db.close()



# Streamlit UI
st.title("Teacher Timetable")

if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'data_entry_section' not in st.session_state:
    st.session_state.data_entry_section = False
if 'delete_section' not in st.session_state:
    st.session_state.delete_section = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Display login and signup buttons initially
action = st.radio("Select Action:", ["Login", "Signup"])

if action == "Login":
    # Input for teacher's username and password
    if not st.session_state.login_status:
        username = st.text_input("Enter Teacher's Username:")
        password = st.text_input("Enter Password:", type="password")
        login_button = st.button("Login")

        if login_button:
            if check_login(username, password):
                st.session_state.login_status = True
                st.session_state.username = username
                st.success("Login successful!")

elif action == "Signup":
    # Input for teacher's signup information
    t_name = st.text_input("Enter Teacher's ID:")
    t_id = st.text_input("Enter Teacher's Name:")
    signup_password = st.text_input("Enter Password:", type="password")
    signup_button = st.button("Signup")

    if signup_button:
        signup_teacher(t_name, t_id, signup_password)

# Display timetables by default
if st.session_state.login_status:
    st.success("Login successful!")

    # Display timings table
    st.header("Timings Table")
    display_timings()

    # Get unique subject names for the user
    unique_subjects = get_unique_subjects(st.session_state.username)

    for subject_name in unique_subjects:
        st.header(f"{subject_name} Timetable")

        # Get the timetable grid for the subject
        timetable = get_timetable_grid(st.session_state.username, subject_name)

        # Display the timetable grid
        df = pd.DataFrame(timetable, index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                          columns=list(range(1, 11))
                          )
        st.dataframe(df)

    # Data entry section
    data_entry_section = st.checkbox("Data Entry Section")

    if data_entry_section:
        for subject_name in unique_subjects:
            st.header(f"Add Data for {subject_name}")

            # Add data to periods
            cls_id = st.text_input("Class ID", key=f"class_id_{subject_name}")
            day = st.selectbox("Day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                               key=f"day_{subject_name}")
            period = st.number_input("Period", min_value=1, max_value=10, value=1, key=f"period_{subject_name}")

            if st.button(f"Add Data for {subject_name}"):
                add_period_data(st.session_state.username, subject_name, cls_id, day, period)

    # Delete section
    if st.session_state.login_status:
        st.session_state.delete_section = st.checkbox("Delete Section")

        if st.session_state.delete_section:
            for subject_name in unique_subjects:
                st.header(f"Delete Data for {subject_name}")

                # Delete data from periods
                day_delete = st.selectbox("Select Day to Delete", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                          key=f"day_delete_{subject_name}")
                period_delete = st.number_input("Select Period to Delete", min_value=1, max_value=10, value=1,
                                                key=f"period_delete_{subject_name}")

                if st.button(f"Delete Data for {subject_name}"):
                    delete_period_data(st.session_state.username, subject_name, day_delete, period_delete)
                    st.success("Data deleted successfully!")

    # Generate Timetable Summary Report
    if st.session_state.login_status:
        if st.checkbox("Generate Timetable Summary Report"):
            generate_timetable_summary(st.session_state.username)
        if st.checkbox("Minimum and Maximum number of Periods"):
            get_min_max_periods_days(st.session_state.username)
        # Input for the class ID

        if st.checkbox("Display Class Subjects"):
            cls_id_input = st.text_input("Enter Class ID:")
            display_class_subjects(cls_id_input)

     # SQL Query input and execution
    st.header("SQL Query")
    sql_query = st.text_area("Enter your SQL query here:")
    execute_query_button = st.button("Execute Query")

    if execute_query_button:
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anjan1234.",
                database="TEACHER_TIMETABLE_SYSTEM"
            )
            cursor = db.cursor()

            cursor.execute(sql_query)
            results = cursor.fetchall()

            if results:
                st.table(pd.DataFrame(results, columns=[desc[0] for desc in cursor.description]))
            else:
                st.info("No results to display.")

        except mysql.connector.Error as err:
            st.warning(f"Error: {err}")

        finally:
            if db.is_connected():
                cursor.close()
                db.close()
                
    # Logout button
    if st.button("Logout"):
        st.session_state.login_status = False
        st.session_state.data_entry_section = False
        st.session_state.delete_section = False
        st.session_state.username = ""
        st.experimental_rerun()
