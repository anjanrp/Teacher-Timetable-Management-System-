# Teacher-Timetable-Management-System-
This is a basic implementation of a teacher timetable management system where the teacher can login and view their respective timetables .

               
To replicate this , clone the repository and follow the steps given below 

  Requirements - python and mysql connector -- pip install mysql-connector-python
               streamlit -- pip install streamlit 
  
  Change your root password whereever necessary to your mysql password in the python files.
  
  Go to your mysql Terminal, enter password and run the following commands:
  
  CREATE DATABASE TEACHER_TIMETABLE_SYSTEM;
  USE TEACHER_TIMETABLE_SYSTEM;
  
  The mysql terminal can be closed now.
  
  Run the files in the following order:
  1. project.py
  2. periods.py
  3. timings.py
  4. period_changes.py
  5. periods_append.py
  6. periods_teacher.py
  7. pass_gen.py
  8. periods_subject.py
  9. trigger_creation.py
  10. procedure_create.py
  11. periods_class.py
  12. streamlit run teachertt.py (main file, contains main code + streamlit GUI code)


Enter the teacher username ( teacher name ) and password to login and you should be able to see the timetable of the respective teacher ( Go through the pass_gen.py file to know the password of the teacher ) 

