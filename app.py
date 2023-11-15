from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, admin_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route for the homepage
@app.route("/")
def index():
    """Show functions assigned to the currently user"""
    role = session.get("role")

    if role == "Admin":
        return render_template("admin.html")
    elif role == "Teacher":
        return render_template("teacher.html")
    else:
        return render_template("login.html")


@app.route("/teacher")
@login_required
def teacher():
    """Show courses and students assigned to the currently logged-in teacher"""

    return render_template("teacher.html")


@app.route("/admin")
@login_required
@admin_required
def admin():
    """Show admin functions"""

    return render_template("admin.html")


@app.route("/admin/teachers", methods=["GET", "POST"])
@login_required
@admin_required
def admin_teachers():
    """Implement logic to display and manage teachers"""
    # Display all teachers when the page loads
    teachers = db.execute("SELECT * FROM user WHERE role = 'Teacher'")

    if request.method == "POST":
        # Handle search functionality
        detail = request.form.get("detail")
        query = request.form.get("query")

        if detail and query:
            # Build the SQL query dynamically with placeholders
            sql = f"SELECT * FROM user WHERE {detail} LIKE ? AND role = 'Teacher'"
            # Provide the values as a tuple
            results = db.execute(sql, ("%" + query + "%",))
            return render_template("admin_teachers.html", teachers=results)
        else:
            flash("All fields are required.", "error")
            return render_template("admin_teachers.html", teachers=teachers)

    else:
        return render_template("admin_teachers.html", teachers=teachers)


@app.route("/admin/teachers_add", methods=["GET", "POST"])
@login_required
@admin_required
def add_teacher():
    """Add a new teacher to the system"""

    if request.method == "POST":
        # Get the teacher ID from the form
        teacher_id = request.form.get("teacher_id")
        confirmation_id = request.form.get("confirmation_id")

        # Ensure the ID is an 8-digit number
        if not teacher_id.isdigit() or len(teacher_id) != 8:
            flash("Please enter a valid ID.", "error")
            return render_template("admin_teachers_add.html")

        # Ensure the ID and confirmation match
        if confirmation_id != teacher_id:
            flash("Teacher ID and confirmation do not match.", "error")
            return render_template("admin_teachers_add.html")

        # Check if the teacher ID already exists in the database
        existing_teacher = db.execute(
            "SELECT * FROM user WHERE user_id = ? AND role = 'Teacher'", teacher_id
        )
        if existing_teacher:
            flash("Teacher ID already exists.", "error")
            return render_template("admin_teachers_add.html")

        # Generate the password as the teacher ID (only for the first login)
        teacher_password = teacher_id

        # Insert the teacher details into the database
        teacher_name = request.form.get("teacher_name")
        db.execute(
            "INSERT INTO user (user_id, name, hash, role) VALUES (?, ?, ?, ?)",
            teacher_id,
            teacher_name,
            generate_password_hash(teacher_password),
            "Teacher",
        )

        # Redirect to the teacher's page and display a success message
        flash("Teacher added successfully.", "success")
        return redirect("/admin/teachers")

    else:
        return render_template("admin_teachers_add.html")


@app.route("/admin/teachers_edit/<teacher_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_teacher(teacher_id):
    """Edit teacher's details"""

    # Fetch the teacher's details from the database
    teacher_details = db.execute("SELECT * FROM user WHERE user_id = ?", teacher_id)

    if request.method == "POST":
        # Validate and update user information
        id = request.form.get("user_id")
        if not id.isdigit() or len(id) != 8:
            flash("Please enter a valid ID.", "error")
            return render_template("admin_teachers_edit.html", user=teacher_details[0])
        # If ID is valid, update teacher details
        else:
            name = request.form.get("name")
            mail = request.form.get("mail")
            phone = request.form.get("phone")
            db.execute(
                "UPDATE user SET user_id = ?, mail = ?, phone = ?, name = ? WHERE user_id = ?",
                id,
                mail,
                phone,
                name,
                teacher_id,
            )

        # Fetch the updated teacher details from the database
        details = db.execute("SELECT * FROM user WHERE user_id = ?", teacher_id)
        new_details = details[0] if details else None

        flash("Teacher's details were updated successfully.", "success")
        return render_template("admin_teachers_edit.html", user=new_details)

    else:
        # Fetch the teacher details from the database
        details = db.execute("SELECT * FROM user WHERE user_id = ?", teacher_id)
        teacher_details = details[0] if details else None
        return render_template("admin_teachers_edit.html", user=teacher_details)


@app.route("/admin/students", methods=["GET", "POST"])
@login_required
@admin_required
def admin_students():
    """Implement logic to display and manage students"""

    students = db.execute("SELECT * FROM student")

    if request.method == "POST":
        # Handle search functionality
        detail = request.form.get("detail")
        query = request.form.get("query")

        if detail and query:
            # Provide the values as a tuple
            results = db.execute(
                f"SELECT * FROM student WHERE {detail} LIKE ?", ("%" + query + "%",)
            )
            return render_template("admin_students.html", students=results)
        else:
            flash("All fields are required.", "error")
            return render_template("admin_students.html", students=students)

    else:
        # Display all students when the page loads
        return render_template("admin_students.html", students=students)


@app.route("/admin/students_add", methods=["GET", "POST"])
@login_required
@admin_required
def add_student():
    """Add a new student to the system"""

    if request.method == "POST":
        # Get the student data from the form
        student_id = request.form.get("student_id")
        confirmation_id = request.form.get("confirmation_id")
        name = request.form.get("name")
        phone = request.form.get("phone")
        adult_phone = request.form.get("adult_phone")

        # Ensure the ID is an 8-digit number
        if not student_id.isdigit() or len(student_id) != 8:
            flash("Please enter a valid ID.", "error")
            return render_template("admin_students_add.html")

        # Ensure the ID and confirmation match
        if confirmation_id != student_id:
            flash("Student ID and confirmation do not match.", "error")
            return render_template("admin_students_add.html")

        # Check if the student ID already exists in the database
        existing_student = db.execute(
            "SELECT * FROM student WHERE student_id = ?", student_id
        )
        if existing_student:
            flash("Student ID already exists.", "error")
            return render_template("admin_students_add.html")

        # Insert the student details into the database
        db.execute(
            "INSERT INTO student (student_id, name, phone, adult_phone) VALUES (?, ?, ?, ?)",
            student_id,
            name,
            phone,
            adult_phone,
        )

        # Redirect to the students page and display a success message
        flash("Student added successfully.", "success")
        return redirect("/admin/students")

    else:
        return render_template("admin_students_add.html")


@app.route("/admin/students_edit/<student_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_student(student_id):
    """Edit student's details"""

    # Fetch the teacher's details from the database
    student_details = db.execute(
        "SELECT * FROM student WHERE student_id = ?", student_id
    )

    if request.method == "POST":
        # Validate and update user information
        id = request.form.get("student_id")
        if not id.isdigit() or len(id) != 8:
            flash("Please enter a valid ID.", "error")
            return render_template(
                "admin_students_edit.html", student=student_details[0]
            )
        else:
            name = request.form.get("name")
            phone = request.form.get("phone")
            adult_phone = request.form.get("adult_phone")
            db.execute(
                "UPDATE student SET student_id = ?, name = ?, phone = ?, adult_phone = ? WHERE student_id = ?",
                id,
                name,
                phone,
                adult_phone,
                student_id,
            )

        # Fetch the updated teacher details from the database
        details = db.execute("SELECT * FROM student WHERE student_id = ?", student_id)
        new_details = details[0] if details else None

        flash("Student's details were updated successfully.", "success")
        return render_template("admin_students_edit.html", student=new_details)

    else:
        # Fetch the student details from the database
        details = db.execute("SELECT * FROM student WHERE student_id = ?", student_id)
        student_details = details[0] if details else None
        return render_template("admin_students_edit.html", student=student_details)


@app.route("/admin/courses", methods=["GET", "POST"])
@login_required
@admin_required
def admin_courses():
    """Implement logic to display and manage courses"""

    # Display all courses when the page loads
    courses = db.execute(
        """
        SELECT
            course.course_id,
            course.name,
            course.level,
            user.name AS teacher_name,
            course_schedule.dayofweek,
            course_schedule.start_time,
            course_schedule.end_time,
            (SELECT COUNT(*) FROM enrollment WHERE enrollment.course_id = course.course_id) AS student_count
        FROM course
        LEFT JOIN user ON course.teacher_id = user.user_id
        LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
        ORDER BY course.course_id, CASE course_schedule.dayofweek
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            ELSE 6
        END
    """
    )

    if request.method == "POST":
        # Handle search functionality
        detail = request.form.get("detail")
        query = request.form.get("query")

        if detail and query:
            # Provide the values as a tuple
            results = db.execute(
                f"""
            SELECT
                course.course_id,
                course.name,
                course.level,
                user.name AS teacher_name,
                course_schedule.dayofweek,
                course_schedule.start_time,
                course_schedule.end_time,
                (SELECT COUNT(*) FROM enrollment WHERE enrollment.course_id = course.course_id) AS student_count
            FROM course
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE {detail} LIKE ?
            ORDER BY course.course_id, CASE course_schedule.dayofweek
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                ELSE 6
            END
        """,
                ("%" + query + "%",),
            )

            return render_template("admin_courses.html", courses=results)

        else:
            flash("All fields are required.", "error")
            return render_template("admin_courses.html", courses=courses)

    else:
        return render_template("admin_courses.html", courses=courses)


@app.route("/admin/courses_add", methods=["GET", "POST"])
@login_required
@admin_required
def add_course():
    """Add a new course to the system"""

    if request.method == "POST":
        # Get the basic course data from the form
        name = request.form.get("name")
        level = request.form.get("level")
        teacher_name = request.form.get("teacher_name")

        # Ensure the required fields are provided
        if not name or not level:
            flash("Please fill in the required fields.", "error")
            return render_template("admin_courses_add.html")

        # Retrieve the teacher_id based on the teacher_name
        teacher_id = db.execute("SELECT user_id FROM user WHERE name = ?", teacher_name)

        if not teacher_id:
            flash("Teacher not found.", "error")
            return render_template("admin_courses_add.html")

        teacher_id = teacher_id[0]["user_id"]

        # Insert the basic course details into the database
        course_id = db.execute(
            "INSERT INTO course (name, level, teacher_id) VALUES (?, ?, ?)",
            name,
            level,
            teacher_id,
        )

        # Get the course schedule data
        dayofweek = request.form.getlist("dayofweek[]")
        start_time = request.form.getlist("start_time[]")
        end_time = request.form.getlist("end_time[]")

        # Insert the course schedule details into the course_schedule table
        for i in range(len(dayofweek)):
            db.execute(
                "INSERT INTO course_schedule (course_id, dayofweek, start_time, end_time) VALUES (?, ?, ?, ?)",
                course_id,
                dayofweek[i],
                start_time[i],
                end_time[i],
            )

        # Redirect to the courses page and display a success message
        flash("Course added successfully.", "success")
        return redirect("/admin/courses")

    else:
        # Query the database to get the list of teacher names
        teachers = db.execute("SELECT name FROM user WHERE role = 'Teacher'")
        teacher_names = [teacher["name"] for teacher in teachers]
        return render_template("admin_courses_add.html", teacher_names=teacher_names)


@app.route("/admin/courses_edit/<int:course_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course(course_id):
    """Edit an existing course in the system"""

    if request.method == "POST":
        # Get the basic course data from the form
        name = request.form.get("name")
        level = request.form.get("level")
        teacher_name = request.form.get("teacher_name")

        # Ensure the required fields are provided
        if not name or not level:
            flash("Please fill in the required fields.", "error")
            return render_template("admin_courses_edit.html")

        # Retrieve the teacher_id based on the teacher_name
        teacher_id = db.execute("SELECT user_id FROM user WHERE name = ?", teacher_name)

        if not teacher_id:
            flash("Teacher not found.", "error")
            return render_template("admin_courses_edit.html")

        teacher_id = teacher_id[0]["user_id"]

        # Update the basic course details in the database
        db.execute(
            "UPDATE course SET name = ?, level = ?, teacher_id = ? WHERE course_id = ?",
            name,
            level,
            teacher_id,
            course_id,
        )

        # Get the course schedule data
        dayofweek = request.form.getlist("dayofweek[]")
        start_time = request.form.getlist("start_time[]")
        end_time = request.form.getlist("end_time[]")

        # Retrieve existing course schedule entries
        schedule_entries = db.execute(
            "SELECT * FROM course_schedule WHERE course_id = ?", course_id
        )

        # Update or insert schedule entries
        if schedule_entries:
            for i, entry in enumerate(schedule_entries):
                if i < len(dayofweek):
                    # Update existing entry
                    db.execute(
                        "UPDATE course_schedule SET dayofweek = ?, start_time = ?, end_time = ? WHERE id = ?",
                        dayofweek[i],
                        start_time[i],
                        end_time[i],
                        entry["id"],
                    )
                else:
                    # Delete extra entries if there are more schedule entries in the database
                    db.execute("DELETE FROM course_schedule WHERE id = ?", entry["id"])

        # If there are more schedule entries in the form, insert them
        elif len(schedule_entries) < len(dayofweek):
            for i in range(len(schedule_entries), len(dayofweek)):
                db.execute(
                    "INSERT INTO course_schedule (course_id, dayofweek, start_time, end_time) VALUES (?, ?, ?, ?)",
                    course_id,
                    dayofweek[i],
                    start_time[i],
                    end_time[i],
                )

        # Redirect to the courses page and display a success message
        flash("Course edited successfully.", "success")
        return redirect("/admin/courses")

    else:
        # Query the database to get the course and its schedule data
        course = db.execute("SELECT * FROM course WHERE course_id = ?", course_id)
        schedule_entries = db.execute(
            "SELECT * FROM course_schedule WHERE course_id = ?", course_id
        )
        teacher_names = db.execute("SELECT * FROM user WHERE role = 'Teacher'")

        return render_template(
            "admin_courses_edit.html",
            course=course[0],
            schedule_entries=schedule_entries,
            teacher_names=teacher_names,
        )


@app.route("/admin/delete/<int:item_id>", methods=["POST"])
@login_required
@admin_required
def delete_item(item_id):
    # Identify the type of item (teacher, student, course)
    teachers = db.execute("SELECT user_id FROM user")
    students = db.execute("SELECT student_id FROM student")
    courses = db.execute("SELECT course_id FROM course")

    # Check if the item_id exists in teachers, students, or courses
    is_teacher = any(item_id == teacher["user_id"] for teacher in teachers)
    is_student = any(item_id == student["student_id"] for student in students)
    is_course = any(item_id == course["course_id"] for course in courses)

    if is_teacher:
        db.execute("DELETE FROM user WHERE user_id = ?", item_id)
        flash("Teacher deleted successfully.", "success")
        return redirect("/admin/teachers")
    elif is_student:
        db.execute("DELETE FROM student WHERE student_id = ?", item_id)
        flash("Student deleted successfully.", "success")
        return redirect("/admin/students")
    elif is_course:
        db.execute("DELETE FROM course WHERE course_id = ?", item_id)
        flash("Course deleted successfully.", "success")
        return redirect("/admin/courses")
    else:
        flash("There was a problem with your request.", "error")
        return redirect("/admin")


@app.route("/admin/enroll", methods=["POST"])
@login_required
@admin_required
def enroll_student():
    student_id = request.form.get("student")
    course_id = request.form.get("course")

    # Check if the student is already enrolled in the course
    enrollment = db.execute(
        "SELECT * FROM enrollment WHERE student_id = ? AND course_id = ?",
        student_id,
        course_id,
    )

    if enrollment:
        flash("Student is already enrolled in the course.", "error")
    elif not student_id or not course_id:
        flash("Please fill in the required fields.", "error")
        return redirect(f"/student/enrollments/{student_id}")
    else:
        # Insert the enrollment into the database
        db.execute(
            "INSERT INTO enrollment (student_id, course_id) VALUES (?, ?)",
            student_id,
            course_id,
        )
        flash("Student enrolled successfully.", "success")

    return redirect(f"/student/enrollments/{student_id}")


@app.route("/admin/drop", methods=["POST"])
@login_required
@admin_required
def drop_course():
    if request.method == "POST":
        # Get the student ID and the course to drop from the form
        student_id = request.form.get("student")
        dropcourse_id = request.form.get("drop_course")

        if not student_id or not dropcourse_id:
            flash("Please fill in the required fields.", "error")
            return redirect(f"/student/enrollments/{student_id}")

        # Remove the course from the student's enrollments
        db.execute(
            "DELETE FROM enrollment WHERE student_id = ? AND course_id = ?",
            student_id,
            dropcourse_id,
        )

        # Redirect to the student's enrollment page or another appropriate location
        flash("Course dropped succesfully.", "success")
        return redirect(f"/student/enrollments/{student_id}")
    else:
        flash("Invalid request method.", "error")
        return redirect(f"/student/enrollments/{student_id}")


@app.route("/student/enrollments/<int:student_id>")
@login_required
@admin_required
def student_enrollments(student_id):
    # Retrieve student information from the database
    student = db.execute(
        "SELECT student_id, name FROM student WHERE student_id = ?", student_id
    )

    if student:
        # Retrieve the student's enrollments with schedule details
        sql = """
            SELECT
                course.course_id,
                course.name AS course_name,
                course.level AS course_level,
                user.name AS teacher_name,
                course_schedule.dayofweek,
                course_schedule.start_time,
                course_schedule.end_time
            FROM enrollment
            JOIN course ON enrollment.course_id = course.course_id
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE enrollment.student_id = ?
        """
        student_enrollments = db.execute(sql, student_id)

        new_courses = db.execute(
            """
            SELECT course.course_id, course.name, course.level, user.name AS teacher_name
            FROM course
            LEFT JOIN user ON course.teacher_id = user.user_id
            WHERE course.course_id NOT IN (
                SELECT enrollment.course_id
                FROM enrollment
                WHERE enrollment.student_id = ?
            )
        """,
            student_id,
        )

        return render_template(
            "student_enrollments.html",
            student=student[0],
            student_enrollments=student_enrollments,
            courses=new_courses,
        )
    else:
        flash("Student not found.", "error")
        return redirect("/admin/students")


@app.route("/course/enrollments/<int:course_id>")
@login_required
def course_enrollments(course_id):
    # Retrieve course information from the database
    sql = """
            SELECT
                course.course_id,
                course.name,
                course.level,
                user.name AS teacher_name,
                course_schedule.dayofweek AS course_day,
                course_schedule.start_time AS course_start,
                course_schedule.end_time AS course_end
            FROM course
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE course.course_id = ?
            ORDER BY CASE course_schedule.dayofweek
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END;"""
    course = db.execute(sql, course_id)

    if course:
        # Display students enrolled in the course when the page loads
        sql = """SELECT
                    student.student_id AS student_id,
                    student.name AS student_name
                FROM course
                LEFT JOIN enrollment ON course.course_id = enrollment.course_id
                LEFT JOIN student ON enrollment.student_id = student.student_id
                WHERE course.course_id = ?
                ORDER BY student.name"""
        enrollments = db.execute(sql, course_id)

        attendance_history = db.execute(
            """SELECT
                    student_id,
                    course_id,
                    COUNT(CASE WHEN student_attendance = 'Present' THEN 1 ELSE NULL END) AS present_count,
                    COUNT(CASE WHEN student_attendance = 'Late' THEN 1 ELSE NULL END) AS late_count,
                    COUNT(CASE WHEN student_attendance = 'Absent' THEN 1 ELSE NULL END) AS absent_count
                FROM
                    attendance
                WHERE
                    course_id = ?
                GROUP BY
                    student_id, course_id""",
            course_id,
        )

        grades = db.execute("SELECT * FROM grades WHERE course_id = ?", course_id)

        return render_template(
            "course_enrollments.html",
            enrollments=enrollments,
            attendance_history=attendance_history,
            grades=grades,
            course=course,
        )

    else:
        flash("Course not found.", "error")
        return redirect("/admin/courses")


@app.route("/teacher/courses", methods=["GET"])
@login_required
def teacher_courses():
    """Implement logic to display and manage courses"""

    # Display all courses when the page loads
    courses = db.execute(
        """
        SELECT
            course.course_id,
            course.name,
            course.level,
            user.name AS teacher_name,
            course_schedule.dayofweek,
            course_schedule.start_time,
            course_schedule.end_time,
            (SELECT COUNT(*) FROM enrollment WHERE enrollment.course_id = course.course_id) AS student_count
        FROM course
        LEFT JOIN user ON course.teacher_id = user.user_id
        LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
        WHERE course.teacher_id = ?
        ORDER BY course.course_id, CASE course_schedule.dayofweek
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            ELSE 6
        END
    """,
        session["user_id"],
    )

    return render_template("teacher_courses.html", courses=courses)


@app.route("/teacher/students", methods=["GET", "POST"])
@login_required
def teacher_students():
    """Implement logic to display students' details when the user is the teacher"""

    # Display students enrolled in courses taught by the teacher
    teacher_id = session["user_id"]
    sql = """
        SELECT student.*
        FROM student
        JOIN enrollment ON student.student_id = enrollment.student_id
        JOIN course ON enrollment.course_id = course.course_id
        WHERE course.teacher_id = ?
    """
    students = db.execute(sql, (teacher_id,))

    if request.method == "POST":
        detail = request.form.get("detail")
        query = request.form.get("query")

        if detail and query:
            # Build the SQL query to select students enrolled in courses taught by the teacher
            teacher_id = session["user_id"]
            results = db.execute(
                f"""
                SELECT student.*
                FROM student
                JOIN enrollment ON student.student_id = enrollment.student_id
                JOIN course ON enrollment.course_id = course.course_id
                WHERE course.teacher_id = ? AND {detail} LIKE ?
            """,
                teacher_id,
                "%" + query + "%",
            )
            return render_template("teacher_students.html", students=results)

        else:
            flash("All fields are required.", "error")
            return render_template("teacher_students.html", students=students)

    else:
        return render_template("teacher_students.html", students=students)


@app.route("/teacher/student/enrollments/<int:student_id>")
@login_required
def teacher_student_enrollments(student_id):
    # Retrieve student information from the database
    student = db.execute(
        "SELECT student_id, name FROM student WHERE student_id = ?", student_id
    )

    if student:
        # Retrieve the student's enrollments with schedule details
        sql = """
            SELECT
                course.course_id,
                course.name AS course_name,
                course.level AS course_level,
                user.name AS teacher_name,
                course_schedule.dayofweek,
                course_schedule.start_time,
                course_schedule.end_time
            FROM enrollment
            JOIN course ON enrollment.course_id = course.course_id
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE enrollment.student_id = ?
        """
        student_enrollments = db.execute(sql, student_id)

        return render_template(
            "teacher_student_enrollments.html",
            student=student[0],
            student_enrollments=student_enrollments,
        )
    else:
        flash("Student not found.", "error")
        return redirect("/teacher/students")


@app.route("/course/attendance/<int:course_id>", methods=["GET", "POST"])
@login_required
def course_attendance(course_id):
    # Retrieve course information from the database
    sql = """
            SELECT
                course.course_id,
                course.name,
                course.level,
                user.name AS teacher_name,
                course_schedule.dayofweek AS course_day,
                course_schedule.start_time AS course_start,
                course_schedule.end_time AS course_end
            FROM course
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE course.course_id = ?
            ORDER BY CASE course_schedule.dayofweek
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END;"""
    course = db.execute(sql, course_id)

    if course:
        # Display students enrolled in the course when the page loads
        sql = """SELECT
                    student.student_id AS student_id,
                    student.name AS student_name
                FROM course
                LEFT JOIN enrollment ON course.course_id = enrollment.course_id
                LEFT JOIN student ON enrollment.student_id = student.student_id
                WHERE course.course_id = ?
                ORDER BY student.name"""

        enrollments = db.execute(sql, course_id)
        attendance = db.execute(
            "SELECT * FROM attendance WHERE course_id = ? ORDER BY date DESC", course_id
        )
        return render_template(
            "course_attendance.html",
            enrollments=enrollments,
            attendance=attendance,
            course=course,
        )

    else:
        flash("Course not found.", "error")
        if session["role"] == "Admin":
            return redirect("/admin/courses")
        else:
            return redirect("/teacher/courses")


@app.route("/attendance/register/<course_id>", methods=["GET", "POST"])
@login_required
def register_attendance(course_id):
    # Retrieve a list of students in the selected course
    attendance = db.execute("SELECT * FROM attendance WHERE course_id = ?", course_id)
    course = db.execute("SELECT * FROM course WHERE course_id = ?", course_id)
    students = db.execute(
        """
        SELECT student.student_id, student.name
        FROM student
        JOIN enrollment ON student.student_id = enrollment.student_id
        WHERE enrollment.course_id = ?
        ORDER BY student.name
    """,
        course_id,
    )

    if request.method == "POST":
        # Get the selected date and attendance data from the form
        date = request.form.get("date")

        # Loop through the students in the course and record their attendance
        for student in students:
            # Check if an attendance record already exists for the given course, student, and date
            existing_record = db.execute(
                "SELECT * FROM attendance WHERE course_id = ? AND student_id = ? AND date = ?",
                course_id,
                student["student_id"],
                date,
            )
            attendance_status = request.form.get(f"attendance_{student['student_id']}")

            if existing_record:
                # If an attendance record exists, update it
                db.execute(
                    "UPDATE attendance SET student_attendance = ? WHERE course_id = ? AND student_id = ? AND date = ?",
                    attendance_status,
                    course_id,
                    student["student_id"],
                    date,
                )
            else:
                # If no attendance record exists, insert a new one
                db.execute(
                    "INSERT INTO attendance (course_id, student_id, date, student_attendance) VALUES (?, ?, ?, ?)",
                    course_id,
                    student["student_id"],
                    date,
                    attendance_status,
                )

        flash("Attendance recorded successfully.", "success")
        return redirect(f"/course/attendance/{course_id}")

    else:
        return render_template(
            "attendance_register.html",
            attendance=attendance,
            course=course[0],
            students=students,
        )


@app.route("/attendance/edit/<course_id>/<date>", methods=["GET", "POST"])
@login_required
def edit_attendance(course_id, date):
    # Retrieve a list of students in the selected course
    attendance = db.execute(
        "SELECT * FROM attendance WHERE course_id = ? AND date = ?", course_id, date
    )
    course = db.execute("SELECT * FROM course WHERE course_id = ?", course_id)
    students = db.execute(
        """
        SELECT student.student_id, student.name
        FROM student
        JOIN enrollment ON student.student_id = enrollment.student_id
        WHERE enrollment.course_id = ?
        ORDER BY student.name
    """,
        course_id,
    )

    if request.method == "POST":
        # Get the selected date and attendance data from the form
        date = request.form.get("date")

        # Loop through the students in the course and record their attendance
        for student in students:
            # Check if an attendance record already exists for the given course, student, and date
            existing_record = db.execute(
                "SELECT * FROM attendance WHERE course_id = ? AND student_id = ? AND date = ?",
                course_id,
                student["student_id"],
                date,
            )
            attendance_status = request.form.get(f"attendance_{student['student_id']}")

            if existing_record:
                # If an attendance record exists, update it
                db.execute(
                    "UPDATE attendance SET student_attendance = ? WHERE course_id = ? AND student_id = ? AND date = ?",
                    attendance_status,
                    course_id,
                    student["student_id"],
                    date,
                )
            else:
                # If no attendance record exists, insert a new one
                db.execute(
                    "INSERT INTO attendance (course_id, student_id, date, student_attendance) VALUES (?, ?, ?, ?)",
                    course_id,
                    student["student_id"],
                    date,
                    attendance_status,
                )

        flash("Attendance updated successfully.", "success")
        return redirect(f"/course/attendance/{course_id}")

    else:
        return render_template(
            "attendance_edit.html",
            attendance=attendance,
            course=course[0],
            students=students,
        )


@app.route("/teacher/grades/<int:course_id>", methods=["GET", "POST"])
@login_required
def grades(course_id):
    # Retrieve course information from the database
    sql = """
            SELECT
                course.course_id,
                course.name,
                course.level,
                user.name AS teacher_name,
                course_schedule.dayofweek AS course_day,
                course_schedule.start_time AS course_start,
                course_schedule.end_time AS course_end
            FROM course
            LEFT JOIN user ON course.teacher_id = user.user_id
            LEFT JOIN course_schedule ON course.course_id = course_schedule.course_id
            WHERE course.course_id = ?
            ORDER BY CASE course_schedule.dayofweek
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END;"""
    course = db.execute(sql, course_id)

    # Retrieve student enrollments and grades for the course
    enrollments = db.execute(
        "SELECT student_id, name FROM enrollment JOIN student USING (student_id) WHERE course_id = ? ORDER BY student.name",
        course_id,
    )
    grades = db.execute(
        "SELECT student_id, grade FROM grades WHERE course_id = ?", course_id
    )

    if request.method == "POST":
        for student in enrollments:
            grade = request.form.get(f"grade_{student['student_id']}")

            # Check if the grade for this student and course already exists
            existing_grade = db.execute(
                "SELECT grade FROM grades WHERE course_id = ? AND student_id = ?",
                course_id,
                student["student_id"],
            )

            if existing_grade:
                # If a grade exists, update it
                db.execute(
                    "UPDATE grades SET grade = ? WHERE course_id = ? AND student_id = ?",
                    grade,
                    course_id,
                    student["student_id"],
                )
            else:
                # If no grade exists, insert a new one
                db.execute(
                    "INSERT INTO grades (course_id, student_id, grade) VALUES (?, ?, ?)",
                    course_id,
                    student["student_id"],
                    grade,
                )

        flash("Grades updated successfully.", "success")
        return redirect(f"/teacher/grades/{course_id}")

    # Retrieve course information
    if not course:
        flash("Course not found.", "error")
        return redirect("/teacher/courses")

    return render_template(
        "course_grades.html", course=course, enrollments=enrollments, grades=grades
    )


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    """User profile page where users can update their information"""

    # Get user details from the database
    details = db.execute("SELECT * FROM user WHERE user_id = ?", session["user_id"])
    user_details = details[0] if details else None

    if request.method == "POST":
        # Validate and update user information
        name = request.form.get("name")
        mail = request.form.get("mail")
        phone = request.form.get("phone")

        if not name:
            flash("Please enter a valid name.", "error")
        elif not mail:
            flash("Please enter a valid email address.", "error")
        elif not phone:
            flash("Please enter a valid phone number.", "error")
        else:
            # Update user details in the database
            db.execute(
                "UPDATE user SET mail = ?, phone = ?, name = ? WHERE user_id = ?",
                mail,
                phone,
                name,
                session["user_id"],
            )

        # Fetch the updated user details from the database
        updated_details = db.execute(
            "SELECT * FROM user WHERE user_id = ?", session["user_id"]
        )
        updated_user_details = updated_details[0] if updated_details else None

        # If the password is the same as the ID, encourage password change
        if check_password_hash(
            str(updated_user_details["hash"]), str(updated_user_details["user_id"])
        ):
            flash(
                "Your password is the same as your ID. Please change your password to a more secure one.",
                "error",
            )
            return render_template("password_change.html")
        else:
            flash("Your details were updated successfully.", "success")
            return render_template("user.html", user=updated_user_details)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Fetch the user details from the database
        details = db.execute("SELECT * FROM user WHERE user_id = ?", session["user_id"])
        user_details = details[0] if details else None
        return render_template("user.html", user=user_details)


@app.route("/password_change", methods=["GET", "POST"])
@login_required
def password_change():
    """Change user password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Validate and update user password
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure all fields are filled out
        if not current_password or not new_password or not confirmation:
            flash("All fields are required.", "error")
            return render_template("password_change.html")

        # Query database for current password hash
        rows = db.execute("SELECT hash FROM user WHERE user_id = ?", session["user_id"])

        # Ensure the current password is correct
        if not rows or not check_password_hash(rows[0]["hash"], current_password):
            flash("Current password is incorrect.", "error")
            return render_template("password_change.html")

        # Ensure the new password and confirmation match
        if new_password != confirmation:
            flash("New password and confirmation do not match.", "error")
            return render_template("password_change.html")

        # Hash the new password and update it in the database
        hashed_password = generate_password_hash(new_password)
        db.execute(
            "UPDATE user SET hash = ? WHERE user_id = ?",
            hashed_password,
            session["user_id"],
        )

        flash("Password changed successfully.", "success")
        return render_template("password_change.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password_change.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if not user_id or not password:
            flash("ID and password are required", "error")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE user_id = ?", user_id)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid ID or password", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        session["role"] = rows[0]["role"]

        # Encourage the user to enter personal details and change password
        if not rows[0]["mail"] or not rows[0]["phone"]:
            return redirect("/user")
        elif check_password_hash(str(rows[0]["hash"]), str(rows[0]["user_id"])):
            flash(
                "Your password is the same as your ID. Please change your password to a more secure one.",
                "error",
            )
            return render_template("password_change.html")
        else:
            # Customize the experience based on the role
            flash("Logged in successfully as " + session["role"] + ".", "success")
            if session["role"] == "Admin":
                return redirect("/admin")
            elif session["role"] == "Teacher":
                return redirect("/teacher")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect to the login page
    flash("You have been successfully logged out.", "success")
    return redirect("/")
