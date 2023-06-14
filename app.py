from flask import Flask, render_template,request
app = Flask(__name__)

import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS NOTES (name TEXT, note TEXT)")

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/join')
def join():
	return render_template('join.html')
# @app.route('/opennotes')
# def opennotes():
# 	return render_template('opennotes.html')


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
