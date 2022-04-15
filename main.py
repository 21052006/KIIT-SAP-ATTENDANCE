from flask import Flask, render_template, request, redirect, flash
import get_data
app = Flask(__name__)
app.secret_key = "ANY KEY"
data = [0]
@app.route("/")
@app.route("/login")
def login():
    data[0] = 0
    return render_template("login.html")

@app.route("/fetch", methods=["GET", "POST"])
def get():
    if request.method == "POST":
        if data[0] == 0:
            data[0] = get_data.get_attendance_record(request.form["username"], request.form['password'])        
        if data[0]!="Failed to pass credentials":
            return render_template("show_table.html", sub=data)
        else:
            flash(message="Failed to pass credentials")
            return redirect("/login")

app.run(debug=True)