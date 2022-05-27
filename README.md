INITIAL STEPS FOR RUNNING THE CODE:

- Create a `virtualenv` in the root folder. By following instructions based on your OS.
- Once `virtualenv` is created and activated run : `pip install CMake` and `pip install -r requirements.txt` (CMake has been mentioned as one of the requirements too but in my local machine, while running only the second command it gives an error related to installation of CMake)
- Go into `attendance_tracker_site` and run the migrations :`python manage.py makemigrations` 
- Run `python manage.py migrate`- sync models and database
- Run the dev server `python manage.py runserver`
- Go to `http://localhost:8000/` (Home page)
- Login to admin portal : `http://localhost:8000/admin` (username: `vinita` and password `vinita`)



PROBLEM STATEMENT (ATTENDANCE TRACKING WITH FACE RECOGNITION):

A student management system wherein all the data related to the attendance of students is being tracked, recorded and displayed. Attendance of a particular student, for a particular class gets updated when the student clicks his/her picture in the web app. Student database can be accessed and modified easily. Attendance reports are generated at the click of a button. Wholistic management system catering to the needs of students, faculty and administration.



LINK TO THE DOCUMENTATION LISTING ALL FEATURES (WITH SCREENSHOTS)-

https://docs.google.com/presentation/d/1LuuSjjN69Swd0JWQVuofDZmjlBmcuyyY/edit?usp=sharing&ouid=103219114594843910597&rtpof=true&sd=true



LINK TO THE MOCK TIMETABLES I USED FOR DEMO PURPOSE-

https://docs.google.com/spreadsheets/d/1mobsrezPVo_nAkb9wtQjy-UxR8jTDQvR/edit?usp=sharing&ouid=103219114594843910597&rtpof=true&sd=true
Attendance for students has been entered from 9th-13th May, 2022. Please generate reports for those dates to get good values for attendance.



LINK TO THE VIDEO DEMO-

https://drive.google.com/file/d/1EPFSK3KJaPXo8eA7FRHFUnG8HM1lAWSo/view?usp=sharing