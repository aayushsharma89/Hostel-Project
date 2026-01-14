from flask import Flask, render_template, request, redirect, session, redirect, url_for
import mysql.connector as cc

app = Flask(__name__)
app.secret_key = "hostel123"
con=cc.connect(host="localhost",user="root",password="2705",database="hostel",charset="utf8",use_unicode=True)
cursor = con.cursor()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (user, pwd))
        result = cursor.fetchone()
        if result:
            session["admin"] = user
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        room = request.form["room"]
        course = request.form["course"]
        email = request.form["email"]
        phone = request.form["phone"]
        year = request.form["year"]

        cursor.execute(
            "INSERT INTO students(name, roll_no, room_no, course, email, phone, year) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (name, roll, room, course, email, phone, year)
        )
        con.commit()
        return redirect("/view_students")
    return render_template("add_student.html")

@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        room_number = request.form.get("room_no")
        room_type = request.form.get("room_type")
        capacity = int(request.form.get("capacity"))
        rent = int(request.form.get("rent"))

        cursor.execute(
            "INSERT INTO rooms (room_no, room_type, capacity, available_beds, rent) "
            "VALUES (%s, %s, %s, %s, %s)",
            (room_number, room_type, capacity, capacity, rent)
        )
        con.commit()

        return render_template("success.html", msg="Room Added Successfully")

    return render_template("add_room.html")

@app.route("/delete_student", methods=["GET", "POST"])
def delete_student():
    if request.method == "POST":
        id = request.form["student_id"]
        cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        con.commit()
        return redirect(url_for("view_students"))

    
    return render_template("delete_student.html")




@app.route("/view_students")
def view_students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template("view_students.html", students=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
