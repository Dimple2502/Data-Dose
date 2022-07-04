# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__, static_url_path='/static')
app.secret_key = "7534291534"

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "rohit"
app.config["MYSQL_DB"] = "simp"

db = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])


# For Login/Home Page
def index():
    if request.method == 'POST':
        select = request.form.get('dropdwn')
        if select == 'admindrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info is not None:
                    if info['username'] == username and info['password'] == password:
                        session['loginsuccess'] = True
                        return redirect(url_for('profile_admin'))
                else:
                    return redirect(url_for('index'))
        elif select == 'teacherdrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM teacher WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info is not None:
                    if info['username'] == username and info['password'] == password:
                        session['loginsuccess'] = True
                        return redirect(url_for('profile_teacher'))
                else:
                    return redirect(url_for('index'))
        elif select == 'studentdrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM student WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info is not None:
                    if info['username'] == username and info['password'] == password:
                        session['loginsuccess'] = True
                        return redirect(url_for('profile_student'))
                else:
                    return redirect(url_for('index'))
    return render_template("login.html")

# For Register
@app.route('/new', methods=['GET','POST'])
def new_user():
    if request.method == "POST":
        if request.form['action'] == 'Student':
            if "reg_id" in request.form and "fullname" in request.form and "phone" in request.form and "dob" in request.form and "username" in request.form and "password" in request.form:
                reg_id = request.form['reg_id']
                fullname = request.form['fullname']
                phone = request.form['phone']
                dob = request.form['dob']
                username = request.form['username']
                password = request.form['password']
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO simp.student(reg_id, name, phone_no, username, password, dob)VALUES(%s, %s, %s, %s, %s, %s)",(reg_id, fullname, phone, username, password, dob))
                db.connection.commit()
                return redirect(url_for('index'))
        elif request.form['action'] == 'Teacher':
            if "reg_id" in request.form and "fullname" in request.form and "phone" in request.form and "dob" in request.form and "username" in request.form and "password" in request.form:
                reg_id = request.form['reg_id']
                fullname = request.form['fullname']
                phone = request.form['phone']
                dob = request.form['dob']
                username = request.form['username']
                password = request.form['password']
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO simp.teacher(reg_id, name, phone_no, username, password, dob)VALUES(%s, %s, %s, %s, %s, %s)",(reg_id, fullname, phone, username, password, dob))
                db.connection.commit()
                return redirect(url_for('index'))

    return render_template('Register.html')

# Admin Profile - Edit teacher
@app.route('/profile/admin', methods=['GET','POST'])
def profile_admin():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from teacher")
        data = curs.fetchall()
        curs.close()

        return render_template('admin_teacher.html', teacher = data)


# Admin Profile - Edit student
@app.route('/profile/s_admin', methods=['GET','POST'])
def profile_admin_student():
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        cur.execute("SELECT * from student")
        data = cur.fetchall()
        cur.close()

    return render_template('admin_student.html', student = data)

#edit for teacher
@app.route('/updateteacher/<string:id>', methods=['GET','POST'])
def update_teacher(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            reg_id = request.form['reg_id']
            fullname = request.form['fullname']
            phone = request.form['phone']
            dob = request.form['dob']
            username = request.form['username']
            password = request.form['password']
            sql = "UPDATE teacher SET reg_id = %s, name = %s, phone_no = %s, username = %s, password = %s, dob = %s WHERE reg_id = %s"
            cur.execute(sql,[reg_id, fullname, phone, username, password, dob, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('profile_admin'))
            cur = db.connection.cursor()
            
        sql = "SELECT * FROM teacher WHERE reg_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_user.html", data = res)

#edit for student
@app.route('/updatestudent/<string:id>', methods=['GET','POST'])
def update_student(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            reg_id = request.form['reg_id']
            fullname = request.form['fullname']
            phone = request.form['phone']
            dob = request.form['dob']
            username = request.form['username']
            password = request.form['password']
            sql = "UPDATE student SET reg_id = %s, name = %s, phone_no = %s, username = %s, password = %s, dob = %s WHERE reg_id = %s"
            cur.execute(sql,[reg_id, fullname, phone, username, password, dob, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('profile_admin_student'))
            cur = db.connection.cursor()
            
        sql = "SELECT * FROM student WHERE reg_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_user.html", data = res)

#delete for teacher
@app.route('/delete/teacher/<string:id_data>', methods=['POST','GET'])
def delete_teacher(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM teacher WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('profile_admin'))

#delete for student
@app.route('/delete/student/<string:id_data>', methods=['POST','GET'])
def delete_student(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM student WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('profile_admin_student'))

# Teacher Profile
@app.route('/profile/teacher')
def profile_teacher():
    if session['loginsuccess'] == True:
        return render_template('sd_teacher.html')

# Student Profile/Details
@app.route('/profile/student', methods=['GET','POST'])
def profile_student():
    if session['loginsuccess'] == True:
        if request.method == 'POST':
            if "fname" in request.form and "lname" in request.form and "reg_id" in request.form and "gen" in request.form and "branchdrp" in request.form:
                fname = request.form['fname']
                lname = request.form['lname']
                f_name = request.form['f_name']
                m_name = request.form['m_name']
                date_of_birth = request.form['date_of_birth']
                gender = request.form['gen']
                address = request.form['address']
                phone_number = request.form['phone_number']
                reg_id = request.form['reg_id']
                branch = request.form.get('branchdrp')
                roll_number = request.form['roll_number']
                submitcur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                submitcur.execute("INSERT INTO simp.studentdetails(reg_id, f_name, l_name, father_name, mother_name, dob, gender, address, phone_no, branch, roll_no)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(reg_id, fname, lname, f_name, m_name, date_of_birth, gender, address, phone_number, branch, roll_number))
                db.connection.commit()
                return redirect(url_for('success'))

        return render_template('sd_student.html')


# Student - Course
@app.route('/profile/studentcourse', methods=['GET','POST'])
def course_student():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from course")
        data = curs.fetchall()
        curs.close()
    return render_template('course_student.html', course = data)

# Teacher - Course
@app.route('/profile/teachercourse', methods=['GET','POST'])
def course_teacher():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from course")
        data = curs.fetchall()
        curs.close()
    return render_template('course_teacher.html', course = data)

#Update course
@app.route('/updatecourse/<string:id>', methods=['GET','POST'])
def update_course(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            subject_id = request.form['sub_id']
            subject_name = request.form['sub_name']
            teacher_name = request.form['teacher_name']
            sql = "UPDATE course SET subject_id = %s, subject = %s, teacher = %s WHERE subject_id = %s"
            cur.execute(sql,[subject_id, subject_name, teacher_name, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('course_teacher'))
            cur = db.connection.cursor()
        sql = "SELECT * FROM course WHERE subject_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_course.html", data = res)



#Delete course
@app.route('/delete/course/<string:id_data>', methods=['POST','GET'])
def delete_course(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM course WHERE subject_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('course_teacher'))


# For Logout 
@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))

# About 
@app.route('/about')
def about():
    return render_template('about.html')

# Team
@app.route('/team')
def team():
    return render_template('team.html')

# Help
@app.route('/help')
def help():
    return render_template('help.html')

@app.route("/testpage")
def success():
     return "<p>Success!</p>"

if __name__ == "__main__":
    app.run(debug=True)

        