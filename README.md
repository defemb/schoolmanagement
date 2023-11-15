# School Management System
#### Video Demo:  <https://www.youtube.com/watch?v=hfMKynQTX9E>
#### Description:

## Introduction

The School Management System is a web application born out of my experience as a coordinator in an educational program. Its primary objective is to assist educational institutions with their administrative tasks, simplifying the management of student enrollment, courses, attendance, and grading.

## Key Functions

### Administrator Functions
Administrators play a crucial role in the system, overseeing various tasks:

#### Teacher Management
- Add, edit, or remove teacher information.
- Assign teachers to specific courses and schedules.
- Search for teachers based on various criteria.

#### Student Management
- Add, edit, or remove student information.
- Enroll and unenroll students in courses.
- Search for students based on various criteria.

#### Course Management
- Create, edit, or delete courses.
- Assign teachers and schedules to courses.
- View and search for courses based on various parameters.

### Teacher Functions
Teachers have specialized access for managing their assigned courses, students, and grades:

#### Course Management
- View courses assigned to the teacher.
- Access course details, schedules, and enrolled students.
- Monitor student attendance and grades for each course.

#### Attendance Management
- Mark student attendance (Present, Late, Absent) for each class.
- Keep track of attendance records.

#### Grades Management
- Record and update student grades.

### User Functions
Both administrators and teachers benefit from these integrated user functions:

#### User Authentication
- Secure login system for users.

#### Personal details
- Users can change their personal details or passwords as needed. Their unique identification ID remains constant.

#### Admin or Teacher Dashboard
- The dashboard offers quick access to various functions, enhancing the efficiency of users in their respective roles.

## Design Choices
The School Management System is built using the Flask web framework and an SQLite database, underpinned by Python. It also employs HTML and JavaScript.
The system effectively separates the roles of administrators and teachers, providing tailored functionality to each user type.
The user-friendly design and trust in the users make it ideal for smaller educational institutions. The system's flexibility allows for future expansion, including the addition of security features and student login/enrollment options.

## Files and Directories
- **app.py**: The main application file that configures and runs the Flask web application.
- **school.db**: The SQLite database file that stores user, teacher, student, course, enrollment, attendance, and grades data.
- **templates/**: Directory containing HTML templates for different web pages.
- **static/**: Directory containing CSS stylesheets and images.

## Functions and Templates

### Layout

The "layout.html" file serves as a fundamental template for rendering various HTML pages in the School Management System web application. It offers a consistent structure, including navigation, headers, and styling. Key components are as follows:
- **HTML Structure**: This file defines the fundamental structure of an HTML page. It incorporates a standard document declaration, meta tags, and a viewport setting for responsive design.
- **Bootstrap Integration**: It links to the Bootstrap framework, enhancing styling and responsiveness, ensuring an appealing and mobile-friendly web application through Bootstrap's CSS and JavaScript.
- **Favicon**: It establishes the website's favicon, the icon displayed in the browser tab, as a school image.
- **Stylesheet**: It links to an external stylesheet file named "styles.css" for custom styling throughout the web application.
- **Title**: The HTML page's title dynamically adjusts based on the page's content.
- **Navigation Bar**: The page includes a navigation bar at the top, featuring the school logo and navigation links. These links adapt to the user's role. If a user logs in as an admin or teacher, they gain access to specific sections like teachers, students, courses, and personal details. For users not logged in, the login option is presented.
- **Flash Messages Handling**: The code accommodates the display of flash messages, categorized as "error" or "success." Error messages appear as red alerts, while success messages are green alerts.
- **Main Content**: The central content of each page is dynamically injected into the "{% block main %}{% endblock %}" section. Various pages extend this layout and provide their content within this section.

### Login and Logout

#### **Login Function**
The login function is accessible via the "/login" route. It enables users to log in to the system. The function comprises the following components:
- **POST Request Handling**: This function caters to both GET and POST requests, primarily when a user submits a login form via POST.
- **Session Clearing**: At the beginning, any existing user session is cleared, ensuring a fresh login process.
- **Form Submission Handling**: When a user submits a login form, the function verifies the submission for both user ID and password.
- **Database Query**: The function queries the SQLite database to find a user with the provided user ID.
- **User Verification**: It validates the existence of the user ID and checks if the entered password matches the stored password hash in the database.
- **Session Variables Setting**: In the case of valid credentials, the function establishes session variables such as "user_id" and "role" to retain the logged-in user's identity.
- **Password Security Alert**: Depending on certain conditions, such as using the user ID as the initial password, the function displays a security alert, advising the user to modify their password for enhanced security.
- **Role-Based Redirection**: After a successful login, the user is directed to a role-specific dashboard. Administrators are led to the admin dashboard, and teachers proceed to the teacher dashboard.

#### **Logout Function**
The logout function is available through the "/logout" route. Users utilize this route to log out of the system. The function consists of these core elements:
- **Session Clearing**: The function clears any active user session, effectively executing the user's log out.
- **Redirection**: Following the session clearance, the user is directed to the login page.
- **Log Out Message**: A success message is displayed to notify the user of their successful log out.

### User Details and Password Change

#### **User Function**
The "user" function, accessible via the "/user" route, handles user profile updates within the School Management System. The following components define its core functionality:
- **User Details Retrieval**: The function retrieves the user's details from the database based on their user ID and stores them in the "user_details" variable. Importantly, the user's ID, an 8-digit unique identifier, remains unmodifiable, serving as a critical element for system identification.
- **GET and POST Handling**: The function responds to both GET and POST requests. When a user accesses the route, their current details are displayed. On a POST request, the function validates and updates user information.
- **Form Handling**: The HTML template includes a form for updating user information, encompassing fields for name, email address, and phone number.
- **Form Submission**: When a user submits the form, the function validates the entered information, updates the database, and displays a success message upon a successful update.
- **Password Change Recommendation**: If the user's password is identical to their ID, a security alert is displayed, recommending a password change for added security.
- **Redirection**: After a successful update, the user is redirected to the "user" page to view the updated information.

#### **Password Change Function**
The "password_change" function is responsible for allowing users to change their passwords, enhancing security.
- **GET and POST Handling**: The function responds to both GET and POST requests. On a GET request, users can access the password change form. On a POST request, users can change their passwords.
- **Password Change Form**: The HTML template includes a form where users can enter their current password, new password, and confirmation.
- **Form Submission**: When a user submits the form, the function validates the input, ensures the current password is correct, and matches the new password and confirmation before updating the hashed password in the database.
- **Password Change Success**: If the password is successfully changed, a success message is displayed.

### Homepage Route and Templates

The homepage route ("/") serves as the initial landing page when users access the School Management System. It customizes the homepage's content based on the user's role, distinguishing between administrators and teachers. The following components define the homepage's core functionality:
- **`index` Route Function:**
  - The `index` function manages the homepage route ("/").
  - It identifies the user's role based on session information and distinguishes between administrators and teachers.
  - If the user is an administrator, the "admin.html" template is rendered to display admin-specific functions.
  - If the user is a teacher, the "teacher.html" template is rendered to showcase teacher-specific functions.
  - If the user's role remains unrecognized, they are directed to the login page ("login.html").
- **Admin Functions:**
  - For administrators, the "admin.html" template presents the following functions:
    - **Manage Teachers**: Admins can add, edit, or remove teachers from the system.
    - **Manage Students**: Admins can add, edit, or remove students' information and manage enrollments.
    - **Manage Courses**: Admins can create, edit, or delete courses, as well as assign teachers and schedules.
  - Each function is presented as a card with a title, a brief description, and a link to the corresponding admin route.
- **Teacher Functions:**
  - For teachers, the "teacher.html" template highlights these functions:
    - **Manage Courses**: Teachers can register attendance and manage grades for their assigned courses.
    - **View Students**: Teachers can access details of students enrolled in their courses.
  - Similar to the admin functions, each teacher function is represented by a card with a title, a brief description, and a link to the corresponding teacher route.

### Admin Functions for Teacher Management

#### **Display and Search Teachers**
The `admin_teachers` function, accessible through the "/admin/teachers" route, handles the display and management of teachers in the School Management System. It offers a variety of features, including searching for teachers and managing their profiles.
- **Display All Teachers**: When the page initially loads, it fetches and displays all teachers in the system. Teachers' details are retrieved from the database using a SQL query.
- **Search Functionality**: The function provides a search feature allowing administrators to find specific teachers based on various details such as ID, name, email, and phone number. Administrators can specify the search detail and enter a query to filter the results.
- **Dynamic SQL Query**: To execute the search, the function dynamically constructs an SQL query with placeholders, making it flexible and adaptable to different search criteria.
- **Validation and Flash Messages**: It validates search inputs and displays error messages if the criteria are not met. A "required fields" error message is shown if search fields are left empty.
- **Search Results Presentation**: The search results are displayed on the same page, allowing administrators to view teacher profiles.

#### **Add New Teacher**
The `add_teacher` function, accessed through the "/admin/teachers_add" route, enables administrators to add a new teacher to the system.
- **Form Submission**: Administrators can fill in the teacher's unique ID, confirm the ID, and provide the teacher's name. Validation is applied to ensure the ID is an 8-digit number, and the confirmation matches the ID.
- **ID Verification**: The function checks if the provided teacher ID already exists in the database. If it exists, an error message is displayed.
- **Password Generation**: For the first login, the function generates the teacher's password as their ID.
- **Database Insertion**: It inserts the teacher's details into the database, including their ID, name, hashed password, and role.
- **Success Message**: After successful teacher addition, a success message is shown to notify administrators.

#### **Edit Teacher Details**
The `edit_teacher` function, accessible via the "/admin/teachers_edit/<teacher_id>" route, allows administrators to edit a teacher's profile.
- **Fetch Teacher Details**: When accessed, the function retrieves the teacher's details from the database, based on their unique ID. The details are displayed for editing.
- **Form Submission and Validation**: Administrators can modify teacher details, including ID, name, email address, and phone number. It validates the entered data, ensuring a valid ID format.
- **Database Update**: Upon validation, the function updates the teacher's information in the database.
- **Updated Details Presentation**: It fetches the updated teacher details from the database and displays them to confirm the changes.

#### **Sorting Functionality**
The HTML templates associated with teacher management include sorting functionality to sort the list of teachers. Administrators can click on column headers to sort the list in ascending or descending order.
- **Sort Teachers**: JavaScript is used to sort teachers based on the clicked column, and arrow buttons indicate the sorting order.
- **Search, Add, and Sort Buttons**: The templates provide convenient buttons for searching teachers, adding new teachers, and sorting the teacher list.

### Admin Functions for Student Management

#### **Display and Search Students**
The `admin_students` function, accessible through the "/admin/students" route, is responsible for displaying and managing student records within the School Management System.
- **Display All Students**: When the page initially loads, it retrieves and displays all student records from the database. These records include details such as student IDs, names, phone numbers, and adult phone numbers.
- **Search Functionality**: The function also provides a search feature that allows administrators to find specific students based on various details, including student ID, name, phone number, and adult phone number. Administrators can specify the search detail and enter a query to filter the results.
- **Dynamic SQL Query**: Similar to the teacher management functionality, the function constructs an SQL query dynamically with placeholders to allow for flexible and adaptable searching.
- **Validation and Error Messages**: It validates search inputs, ensuring that all required fields are filled. If the criteria are not met, an error message is displayed.
- **Search Results Presentation**: The search results are displayed on the same page, enabling administrators to view student profiles that match the search criteria.

#### **Add New Student**
The `add_student` function, accessible via the "/admin/students_add" route, empowers administrators to add new students to the system.
- **Form Submission**: Administrators can input student details such as the student's unique ID, a confirmation of the ID, name, phone number, and an adult's phone number. Validation is applied to ensure the student ID is an 8-digit number and that the confirmation matches the ID.
- **ID Verification**: The function checks if the provided student ID already exists in the database, displaying an error message if it does.
- **Database Insertion**: If the provided details pass validation, the function inserts the new student's information into the database, including student ID, name, phone number, and adult phone number.
- **Success Message**: After successfully adding a student, a success message is displayed to notify administrators.

#### **Edit Student Details**
The `edit_student` function, accessed via the "/admin/students_edit/<student_id>" route, offers administrators the ability to modify student details.
- **Fetch Student Details**: Upon access, the function retrieves the student's details from the database based on their unique ID. These details are presented for editing.
- **Form Submission and Validation**: Administrators can edit student details, including student ID, name, phone number, and adult phone number. The function validates the entered data, ensuring a valid ID format.
- **Database Update**: If the entered information is valid, the function updates the student's details in the database.
- **Updated Details Presentation**: After updating, it fetches the modified student details from the database and displays them to confirm the changes.

#### **Sorting Functionality**
The HTML templates related to student management include sorting functionality that allows administrators to sort the list of students. Clicking on column headers will sort the list in ascending or descending order, and arrow buttons indicate the sorting order.
- **Sort Students**: JavaScript is used to sort students based on the selected column, and arrow buttons reflect the current sorting order.
- **Search, Add, and Sort Buttons**: The templates include user-friendly buttons for searching students, adding new students, and sorting the student list.

### Admin Functions for Courses Management

#### **Display and Manage Courses**
The `admin_courses` function, accessible through the "/admin/courses" route, provides administrators with the ability to view and manage courses within the School Management System.
- **Display All Courses**: When the page initially loads, it retrieves and displays all course records from the database. These records include details such as course ID, name, level, teacher name, schedule, student count, and enrollment information.
- **Search Functionality**: Administrators can perform searches by selecting a specific detail (e.g., course name, level, teacher name) and entering a query to filter the results. The search is conducted by making dynamic SQL queries to the database.
- **Sorting Functionality**: The table of courses allows administrators to sort the list by clicking on the column headers. The arrow buttons indicate the current sorting order (ascending or descending).
- **View Enrollments**: Administrators can view the enrollments for each course by clicking the "View" button, which redirects to the course enrollments page.

#### **Add New Course**
The `add_course` function, accessible via the "/admin/courses_add" route, allows administrators to add new courses to the system.
- **Form Submission**: Administrators input course details, including the course name, level, and teacher name. The function ensures that the required fields are filled.
- **Teacher Validation**: The function validates the provided teacher name, checks if the teacher exists in the database, and retrieves the teacher's user ID.
- **Insert Course Details**: The basic course details, including name, level, and teacher ID, are inserted into the database.
- **Add Schedule**: Administrators can specify the course schedule, including the day of the week, start time, and end time. Multiple schedule entries can be added.
- **Success Message**: After successfully adding a course, a success message is displayed, and administrators are redirected to the courses page.

#### **Edit Course Details**
The `edit_course` function, accessed via the "/admin/courses_edit/<course_id>" route, enables administrators to modify course details.
- **Retrieve Course Data**: Upon access, the function retrieves the course's details from the database, including name, level, teacher name, and the existing schedule.
- **Form Submission and Validation**: Administrators can edit course details, and the function ensures that the required fields are filled.
- **Teacher Validation**: Similar to adding a new course, the function validates the provided teacher name and retrieves the teacher's user ID.
- **Update Course Details**: The function updates the course's details in the database, including the name, level, and teacher ID.
- **Update Schedule**: Administrators can modify the course schedule, and the function updates the schedule entries in the database. Extra entries are deleted if removed.
- **Success Message**: After successfully editing a course, a success message is displayed, and administrators are redirected to the courses page.

### Delete Item Function

The `delete_item` function is a route accessible through the "/admin/delete/<int:item_id>" route, allowing administrators to delete various items (teachers, students, or courses) within the School Management System.
- **Determine Item Type**: This function begins by determining the type of item to be deleted by checking whether the given `item_id` matches an existing teacher, student, or course in the database. It queries the database to retrieve lists of teacher IDs, student IDs, and course IDs.
- **Deletion of Items**: Depending on the item type, one of the following actions is taken:
  - If the `item_id` corresponds to a teacher, the function executes a SQL command to delete the teacher from the "user" table, using their user ID. A success flash message is displayed, indicating that the teacher was deleted successfully, and administrators are redirected to the "/admin/teachers" page.
  - If the `item_id` corresponds to a student, the function deletes the student from the "student" table, and a similar success message is shown, redirecting administrators to the "/admin/students" page.
  - If the `item_id` corresponds to a course, the function deletes the course from the "course" table, again displaying a success message and redirecting administrators to the "/admin/courses" page.
- **Error Handling**: If the `item_id` does not match any existing item type (teacher, student, or course), an error message is displayed, informing administrators that there was a problem with their request. Administrators are redirected to the "/admin" page.

### Student Enroll and Drop Course Functions

#### **Enroll Student Function**
The `enroll_student` function, accessible through the "/admin/enroll" route, allows administrators to enroll students in courses. It involves the following steps:
- **Authentication and Authorization**: This function requires administrators to be logged in and have administrative privileges. It uses the `@login_required` and `@admin_required` decorators to ensure this.
- **Form Submission**: Administrators select a student and a course from drop-down menus in a form and submit it.
- **Enrollment Check**: The function checks if the student is already enrolled in the selected course. If the student is already enrolled, it displays an error message.
- **Data Validation**: It ensures that both the student and course fields are filled. If not, an error message is shown.
- **Enrollment**: If all checks pass, the enrollment is inserted into the database, indicating that the student is now enrolled in the selected course.
- **Feedback Message**: A success message is displayed if the enrollment is successful.
- **Redirection**: The function redirects administrators to the student's enrollments page.

#### **Drop Course Function**
The `drop_course` function, accessed via the "/admin/drop" route, allows administrators to drop courses for students. It follows these steps:
- **Authentication and Authorization**: Similar to the "Enroll Student" function, administrators must be logged in and have administrative privileges.
- **Form Submission and Validation**: Administrators choose a student and a course to drop. The function ensures that both fields are filled. If not, it displays an error message.
- **Course Removal**: The function removes the selected course from the student's enrollments in the database.
- **Feedback Message**: A success message is displayed to confirm that the course has been dropped.
- **Redirection**: Administrators are redirected to the student's enrollments page.
- **Confirmation**: An important note here is that a confirmation dialog is presented when dropping a course to prevent accidental deletions.

#### **Student Enrollments Route**
The "/student/enrollments/<int:student_id>" route is designed for administrators to view and manage the enrollments of a particular student.
- **Route Access**: This route is accessible through the "/student/enrollments/<int:student_id>" URL, where `<int:student_id>` is a placeholder for the unique identifier of the student whose enrollments are to be managed.
- **Retrieve Student Information**: The route begins by querying the database to retrieve information about the specified student. This information includes the student's ID and name.
- **Check Student Existence**: The route checks if the student is found in the database. If the student doesn't exist, it displays an error message and redirects administrators to the student management page.
- **Retrieve Student's Enrollments**: If the student is found, the route constructs a SQL query to retrieve the student's course enrollments, including schedule details. The SQL query joins several tables to gather relevant information:
  - The course ID, name, level, and teacher's name
  - The day of the week, start time, and end time of each course
- **Retrieve Available Courses**: Additionally, the route queries the database to find courses that are not currently enrolled by the student. These are courses that the student can potentially enroll in.
- **Render Template**: The retrieved student information, current enrollments, and available courses are passed to an HTML template, "student_enrollments.html," for rendering.
- **Template Display**: The HTML template organizes the student's course enrollments, presenting them in a tabular format. It displays details such as course name, level, teacher's name, day, and time for each course. Additionally, it provides a list of available courses that the student can choose to enroll in.
- **Data Trust**: It's important to note that this route trusts administrators not to enroll students in courses with overlapping schedules. The system doesn't enforce this constraint within this specific route.
- **Error Handling**: In case the student is not found, the route flashes an error message and redirects administrators to the student management page.

The associated HTML template is designed to display student enrollments with a specific schedule. The school has three possible schedules for classes:
- 8:30 to 10:00
- 10:00 to 11:30
- 11:30 to 1:00

The template organizes enrollments by day and time. It displays the courses a student is enrolled in, including the course name, level, and teacher's name.

Additionally, this template is designed for administrators, and it doesn't allow teachers to alter enrollments. Teachers can only view the schedule of their students. This restriction helps maintain data integrity and prevents unauthorized changes to student enrollments.

### Course Enrollments

#### **Function**
The "/course/enrollments/<int:course_id>" route is designed for teachers to manage and monitor student enrollments, attendance history, and grades for a specific course.
- **Route Access**: This route is accessible through the "/course/enrollments/<int:course_id>" URL, where `<int:course_id>` represents the unique identifier of the course.
- **Authentication and Authorization**: This route is accessible to authenticated users, as indicated by the `@login_required` decorator. It's primarily designed for teachers or instructors to manage their courses and the performance of students within those courses.
- **Retrieve Course Information**: The route starts by querying the database to retrieve detailed information about the specified course. The retrieved information includes course ID, name, level, teacher name, and the course schedule, including the day of the week, start time, and end time. It also orders the schedule entries by the day of the week.
- **Check Course Existence**: The route checks if the course exists in the database. If the course is not found, it displays an error message and redirects users to the courses management page.
- **Retrieve Enrollments**: For the existing course, the route queries the database to obtain a list of students who are currently enrolled in that course. The list includes student ID and name. These student details are used to display the course enrollments.
- **Retrieve Attendance History**: The route also retrieves attendance history for each student in the course. It counts and categorizes attendance records into "Present," "Late," and "Absent" for each student and each course. This data is essential for tracking student attendance over time.
- **Retrieve Grades**: Additionally, the route queries the database for student grades related to the specified course. This information is used to display the grades of students in the course.
- **Render Template**: The retrieved student enrollments, attendance history, grades, and course details are passed to an HTML template, "course_enrollments.html," for rendering and presentation to the teacher.

#### **HTML Template**
The HTML template "course_enrollments.html" is designed to present course-specific data to teachers, including student enrollments, attendance history, and grades. It organizes the information in a structured manner for easy reference and analysis:
- **Course Information**: At the top of the page, the template displays essential course information, including the course name, level, and teacher's name. It also lists the course schedule for the week.
- **Enrollments Table**: The main content of the page is a table that displays student enrollments for the course. It provides the following columns:
  - Student ID: Identifies each enrolled student.
  - Name: Displays the name of each student.
  - Attendance History: Shows a summary of each student's attendance, including the counts of "Present," "Late," and "Absent" occurrences.
  - Grade: Displays the grade of each student in the course.
- **Action Buttons**: At the bottom of the page, there are three action buttons that allow the teacher to navigate to other course-related functionalities:
  - "Courses Dashboard": Links to the teacher's courses dashboard.
  - "Course Attendance": Links to the course attendance page for taking attendance.
  - "Course Grades": Links to the page for managing student grades within the course.

### Teacher Courses Route

- **Route Access**: This route is accessible via a "GET" request to "/teacher/courses."
- **Authentication and Authorization**: Access to this route is restricted to authenticated users, specifically teachers. Teachers can view data related to the courses they are teaching.
- **Display Courses**: When a teacher accesses this route, it retrieves and displays a list of courses they are responsible for. The course information includes course name, level, teacher name, course schedule (including day of the week and timing), and the count of students enrolled in each course.
- **Ordering Courses**: The courses are ordered first by their course ID and then by the day of the week to present them in a logical and consistent manner.
- **HTML Template**: The route renders an HTML template called "teacher_courses.html."
- **JavaScript Sorting**: The template includes JavaScript code for sorting course details. Teachers can sort courses based on their name, level, or other attributes by clicking on the respective column headers. The sorting is indicated by up and down arrows.
- **Course Details**: It displays course details including the course name, level, schedule, student count, and links to view enrollments, attendance, and grades for each course.

### Teacher Students Route

- **Route Access**: This route can be accessed using both "GET" and "POST" requests to "/teacher/students."
- **Authentication and Authorization**: Only authenticated users can access this route, and it is intended for teachers. Teachers can view student details who are enrolled in their courses.
- **Display Students**: When a teacher accesses this route, it retrieves and displays a list of students who are enrolled in courses taught by the teacher.
- **Search Functionality**: The route includes a search feature where teachers can search for specific student details (e.g., student ID, name, phone number) by providing a search query and selecting a specific detail to search by. If a search query is provided, it filters the list of students accordingly.
- **Sorting Functionality**: The route also allows teachers to sort the list of students by various details (e.g., ID, name, phone number, adult phone number) by clicking on the respective column headers. The sorting is dynamic and can be toggled between ascending and descending order.
- **HTML Template**: The route renders an HTML template called "teacher_students.html."
- **JavaScript Sorting**: The template includes JavaScript code for sorting student details based on columns such as student ID, name, phone number, and adult phone number. Teachers can sort students by clicking on the respective column headers.
- **Search Form**: It features a search form where teachers can select a specific detail and enter a query to filter student data. Upon submission, the search results are displayed.
- **Student Details**: It displays student details, including student ID, name, phone number, adult phone number, and a link to view the student's enrollments.

### Course attendance

#### **Viewing Course Attendance**
- **Route**: This route can be accessed via both "GET" and "POST" requests to "/course/attendance/<course_id>."
- **Authentication and Authorization**: It is restricted to authenticated users and is accessible by both teachers and admins. Users can view attendance records for a specific course.
- **Retrieving Course Information**: It retrieves course information, including course name, level, teacher name, and the course schedule, for the specified course ID.
- **Enrollments and Attendance**: It displays a list of students enrolled in the course and their attendance records, sorted by the date in descending order.
- **HTML Template**: The route renders an HTML template called "course_attendance.html."

#### **Registering Course Attendance**:**

- **Route**: Accessible via both "GET" and "POST" requests to "/attendance/register/<course_id>."
- **Authentication and Authorization**: This route is accessible by authenticated users, specifically teachers and admins. Users can record attendance for a specific course.
- **Data Retrieval**: It retrieves information related to the course, including a list of students enrolled in the course, as well as any existing attendance records for the course.
- **Attendance Recording**: Teachers can use the provided form to select a date and specify the attendance status (Present, Late, or Absent) for each student. When the form is submitted, attendance records are updated in the database.
- **HTML Template**: The route renders an HTML template named "attendance_register.html."

#### **Editing Course Attendance**

- **Route**: Accessible via both "GET" and "POST" requests to "/attendance/edit/<course_id>/<date>."
- **Authentication and Authorization**: This route is accessible by authenticated users, mainly teachers and admins. Users can edit existing attendance records for a specific course and date.
- **Data Retrieval**: It retrieves information related to the course, a list of students enrolled in the course, and the existing attendance records for the specified course and date.
- **Attendance Editing**: Teachers can use the provided form to edit attendance records, including changing attendance status for students. When the form is submitted, updated attendance records are saved in the database.
- **HTML Template**: The route renders an HTML template named "attendance_edit.html."
- Both "attendance_register.html" and "attendance_edit.html" share a similar structure.
    - **Form**: The templates contain a form for recording or editing attendance, which includes a date picker and a table listing students and their respective attendance statuses.
    - **JavaScript Validation**: JavaScript is used to validate the form before submission to ensure that an attendance status is selected for each student.
- "course_attendance.html" is designed to display attendance records and course information. It includes tables for listing students and their attendance history, as well as details about the course.

### Grades Register and Edit Route

- **Route**: This route is accessible via both "GET" and "POST" requests to "/teacher/grades/<course_id>."
- **Authentication and Authorization**: This route is protected by user authentication, and only teachers and admins are allowed to access it. It enables teachers to manage grades for students enrolled in a specific course.
- **Course Information Retrieval**: The route retrieves detailed course information, including course name, level, teacher name, and course schedule details (day, start time, end time) from the database for the specified course ID.
- **Student Enrollments and Grades**: The route retrieves a list of students enrolled in the specified course and their respective grades. The students are sorted by their names.
- **Grades Management**: Teachers can use the provided form to manage grades. They can either assign or update grades for each student in the course. The form includes a dropdown menu for selecting the grade (A, B, C, D, F) for each student.
- **Database Operations**: The route performs database operations to update student grades. If a grade for a student and course already exists, it updates the existing grade; otherwise, it inserts a new grade record.
- **Flash Messages**: Flash messages are used to provide feedback to the teacher regarding the success of grade updates.
- **HTML Template**: The route renders an HTML template named "course_grades.html."
- The HTML template is designed to display and manage student grades for a specific course.
- It includes course details at the top, such as course name, level, and teacher name, as well as the course schedule (day and time).
- A form is provided to manage grades, including a table listing students, their names, and grade selection options.
- Teachers can submit the form to update student grades. The table allows teachers to view and edit grades conveniently.
- At the bottom of the template, there are links to navigate to the course dashboard, course enrollments, and course attendance for easy access to related information.
