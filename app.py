from flask import Flask, render_template,request,flash , session,redirect

from datetime import timedelta

app = Flask(__name__)
app.secret_key = "27eduCBjmmnA09"
app.permanent_session_lifetime = timedelta(minutes=5)

import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS USER(userid INT PRIMARY KEY, email TEXT, password TEXT,firstname TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS NOTE (noteid INT PRIMARY KEY, name TEXT, note TEXT ,userid INT,FOREIGN KEY (userid) REFERENCES USER(userid))")
@app.route("/loginsession")
def loginsession():
    if not session.get("email"):
        return redirect("/login")
    return render_template('index.html')

@app.route('/')
def index():
	return render_template('authenticate.html')
@app.route('/join')
def join():
	return render_template('join.html')
@app.route('/registration')
def registration():
	return render_template('registration.html')
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/loginhere', methods =["GET", "POST"])
def loginhere():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
            
            # cursor.execute
                user=cursor.execute('SELECT email FROM USER u WHERE email=u.email')
                pwd=cursor.execute('SELECT email FROM USER u WHERE password=u.password')
    
        if user==email and password==pwd:
             session["email"]=email
             return render_template("join.html")
        else:
            # msg="Please register"
            return render_template("registration.html")             
@app.route("/logout")
def logout():
    session["email"] = None
    return render_template("/login")
        

@app.route('/register', methods =["GET", "POST"])
def register():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        email = request.form["email"]
        firstname = request.form["firstname"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        print(email,firstname)
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
        
        # cursor.execute
            print(cursor.execute('SELECT * FROM USER u WHERE email=u.email'))
            user=cursor.execute('SELECT * FROM USER u WHERE email=u.email')
    
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            with sqlite3.connect("database.db") as users:
                
                cursor = users.cursor()
                
            # cursor.execute
                cursor.execute("INSERT INTO USER (email,firstname,password) VALUES (?,?,?)",
                           (email,firstname,password1))
                print("inserted")
                users.commit()
                print("User create succeesfully")
            # db.session.add(new_user)
            # db.session.commit()
            
            flash('Account created!', category='success')
            return render_template("login.html")
    else:
         return render_template("registration.html")
@app.route('/addnote', methods =["GET", "POST"])
def addnote():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        name = request.form["name"]
        # print(name)
        # getting input with name = lname in HTML form
        note = request.form["note"]
        # print(note)

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO NOTES \
            (name,note) VALUES (?,?)",
                        (name, note))
            users.commit()
            print("Note created successfully")
        return render_template("index.html")
    else:
        return render_template('join.html')
@app.route('/opennotes')
def opennotes():
    connect = sqlite3.connect('database.db')
    cur = connect.cursor()
    print("Cursor created")
    statement='''SELECT * FROM NOTES'''
    cur.execute(statement)
    # # print("Cursor created",cursor)
    # data = cursor.fetchall()
    # print("data extracted",data)
    
    output = cur.fetchall()
    for row in output:
        print(row)
    connect.commit()
    
    # Close the connection
    connect.close()
    return render_template("checknotes.html", data=output)
    
if __name__ == '__main__':
	app.run(debug=False)
