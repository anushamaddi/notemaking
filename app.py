from flask import Flask, render_template,request
app = Flask(__name__)



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/addnote', methods =["GET", "POST"])
def addnote():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       name = request.form["name"]
       print(name)
       # getting input with name = lname in HTML form
       note = request.form["note"]
       print(note)
       return "Your note is "+name + note
    return render_template("participants.html")

if __name__ == '__main__':
	app.run(debug=False)
