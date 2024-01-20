import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from helper import login_required, otp_mail, password_mail, resend_mail
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///iiit-courier.db")

@app.route("/")
def index():
    if session.get("user_id") is None:
        redirect("/login")
    else:
        students = db.execute("SELECT * FROM students WHERE roll_number = ?", session["user_id"])
        if(len(students) != 0):
            redirect("/student")
        
        security = db.execute("SELECT * FROM security WHERE id = ?", session["user_id"])
        if(len(security) != 0):
            redirect("/security")
        
        redirect("/login")
    
@app.route("/login")
def login():
    redirect("/login/student")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if(request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            flash("No username!")
            return render_template("admin.html")
        elif not password:
            flash("No password!")
            return render_template("admin.html")
        
        rows = db.execute("SELECT hash FROM admins WHERE id = ?", username)

        if len(rows) != 1 or password != rows[0]["hash"]:
            flash("Invalid username or password!")
            return render_template("admin.html")
        
        session["user_id"] = username
        return redirect("/admin/home")
    else:
        return render_template("admin.html")
    
@app.route("/admin/home")
@login_required
def adminHome():
    return render_template("adminhome.html")

@app.route("/admin/student", methods=["GET", "POST"])
@login_required
def addStudent():
    if(request.method == "POST"):
        name = request.form.get("name")
        rollNum = request.form.get("rollNum")
        email = request.form.get("email")
        passs = secrets.randbelow(100000)
        password = ""
        if(passs < 1000):
            password += "0"
        elif(passs < 100):
            password += "00"
        elif(passs < 10):
            password += "000"
        password += passs

        if not name:
            flash("No name!")
            return render_template("addstudent.html")
        elif not rollNum:
            flash("No roll number!")
            return render_template("addstudent.html")
        elif not email:
            flash("No email!")
            return render_template("addstudent.html")
        hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        db.execute("INSERT INTO students (roll_number, name, email, hash) VALUES (?, ?, ?, ?)", rollNum, name, email, hash)
        password_mail(rollNum, password, email)

        flash("Student created successfully!")
        return redirect("/admin/home")
        
    else:
        return render_template("addstudent.html")
    
@app.route("/admin/security", methods=["GET", "POST"])
@login_required
def addSecurity():
    if(request.method == "POST"):
        name = request.form.get("name")
        id = request.form.get("id")
        email = request.form.get("email")
        passs = secrets.randbelow(100000)
        password = ""
        if(passs < 1000):
            password += "0"
        elif(passs < 100):
            password += "00"
        elif(passs < 10):
            password += "000"
        password += passs

        if not name:
            flash("No name!")
            return render_template("addsecurity.html")
        elif not id:
            flash("No ID!")
            return render_template("addsecurity.html")
        elif not email:
            flash("No email!")
            return render_template("addsecurity.html")
        
        hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        db.execute("INSERT INTO security (id, name, email, hash) VALUES (?, ?, ?, ?)", id, name, email, hash)
        password_mail(id, password, email)

        flash("Security created successfully!")
        return redirect("/admin/home")
        
    else:
        return render_template("addsecurity.html")
        

@app.route("/login/student", methods=["GET", "POST"])
def loginStudent():
    session.clear()

    if request.method == "POST":
        rollNum = request.form.get("rollNum") # what is the tag I need to put in parentheses?
        password = request.form.get("password")

        if not rollNum:
            flash("No roll number!")
            return render_template("loginstudent.html")
        elif not password:
            flash("No password!")
            return render_template("loginstudent.html")
        
        rows = db.execute("SELECT hash FROM students WHERE roll_number = ?", rollNum)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username or password!")
            return render_template("loginstudent.html")
        
        session["user_id"] = rollNum
        return redirect("/")
    else:
        render_template("loginstudent.html")
    
@app.route("/login/security", methods=["GET", "POST"])
def loginSecurity():
    session.clear()

    if request.method == "POST":
        id = request.form.get("id") # what is the tag I need to put in parentheses?
        password = request.form.get("password")

        if not id:
            flash("No security ID!")
            return render_template("loginsecurity.html")
        elif not password:
            flash("No password!")
            return render_template("loginsecurity.html")
        
        rows = db.execute("SELECT hash FROM security WHERE id = ?", id)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username or password!")
            return render_template("loginsecurity.html")
        
        session["user_id"] = id
        return redirect("/")
    else:
        render_template("loginsecurity.html")
    
@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/")

@app.route("/student")
@login_required
def student():
    rows = db.execute("SELECT * FROM couriers JOIN security ON couriers.security_id=security.id WHERE student_id = ? AND collected = ? ORDER BY arrival DESC", session["user_id"], 0)

    return render_template("student.html", packages=rows) # Give rows of couriers and anything else too?
# Student has to be able to resend OTP... among other things...?


@app.route("/security")
@login_required
def security():
    return render_template("security.html")

numPackages = 0

@app.route("/security/add", methods=["GET", "POST"])
@login_required
def add():
    if(request.method == "POST"):
        rollNum = request.form.get("rollNum")
        src = request.form.get("src")
        arrival = db.execute("SELECT datetime('now', 'localtime')")

        if not rollNum:
            flash("No roll number!")
            return render_template("addpackage.html")
        elif not src:
            flash("No source!")
            return render_template("addpackage.html")
        
        students = db.execute("SELECT * FROM students WHERE roll_number = ?", rollNum)
        if(len(students) == 0):
            flash("Student does not exist!")
            return render_template("addpackage.html")

        id = numPackages
        numPackages += 1
        otpp = secrets.randbelow(100000)
        otp = ""
        if(otpp < 1000):
            otp += "0"
        elif(otpp < 100):
            otp += "00"
        elif(otpp < 10):
            otp += "000"
        otp += otpp
        hash = generate_password_hash(otp, method="pbkdf2:sha256", salt_length=8)
        toMail = students[0]["mail"]
        otp_mail(id, otp, toMail)

        db.execute("INSERT INTO couriers (id, student_id, security_id, source, collected, hash, arrival, collection) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", id, rollNum, session["user_id"], src, 0, hash, arrival, "-")
        flash(f"Courier added successfully! Package ID is {id}")
        return redirect("/security")
    else:
        return render_template("addpackage.html")

@app.route("/security/collect", methods=["GET", "POST"])
@login_required
def collect():
    if(request.method == "POST"):
        packageId = request.form.get("id")
        if not packageId:
            flash("No ID!")
            return render_template("collectpackage.html")
        
        otp = request.form.get("otp")
        if not otp:
            flash("No OTP!")
            return render_template("collect.html")
        rows = db.execute("SELECT hash FROM couriers WHERE id = ?", packageId)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], otp):
            flash("Invalid ID or OTP!")
            return render_template("collectpackage.html")

        db.execute("UPDATE couriers SET hash = ? WHERE id = ?", "", packageId)
        db.execute("UPDATE couriers SET collected = ? WHERE id = ?", 1, packageId)
        collection = db.execute("SELECT datetime('now', 'localtime')")
        db.execute("UPDATE couriers SET collection = ? WHERE id = ?", collection, packageId)
        flash("Package collected successfully!")
        return redirect("/security")
    else:
        return render_template("collectpackage.html")
    
@app.route("/student/history")
@login_required
def history():
    packages = db.execute("SELECT * FROM couriers JOIN security ON couriers.security_id=security.id WHERE student_id = ? ORDER BY arrival DESC", session["user_id"])
    # Does the above select work? Who knows.
    return render_template("history.html") # Give package data and other shit?.