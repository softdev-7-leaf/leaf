from flask import Flask, render_template, request, redirect, url_for, session, escape, flash
import database
import os

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
        if request.method=="GET":
                return render_template("login.html")
        else:
                username = request.form["username"]
                password = request.form["password"]
                button = request.form["b"]
                if button == "Login":
                        if(database.validateUser(username,password) == False):
                                error = 'Unregistered username or incorrect password'
                                return redirect(url_for('login'))
                                flash("You've logged in successfully")
                                session['username'] = request.form['username']
                                gender = "male"
                                age = 42
                                return render_template("user.html", username = username, gender = gender, age = age)
                        else:
                                return redirect(url_for('register'))

@app.route("/register",methods=["GET","POST"])
def register():
        a = []
        for num in range(0,123):
                a.append(num)
                if request.method=="GET":
                        return render_template("register.html", a=a)
                else:
                        button = request.form["b"]
                        if button == "Login":
                                return redirect(url_for('login'))
                                username = request.form["username"]
                                password = request.form["password"]
                                emailaddress = request.form["emailaddress"]
                                if not database.addUser(username, password, emailaddress, gender, age):
                                        flash("There was a problem with what you submitted.")
                                        return redirect(url_for('signup'))
                                        flash("Great! You're registered! Now you can log in.")
                                        return redirect(url_for('login'))

@app.route("/user/<username>",methods=["GET","POST"])
def user(username):
        if request.method=="GET":
                return render_template("user.html", username = username)
        else:
                return render_template("user.html", username = username)

@app.route('/logout')
def logout():
        flash("You've been logged out")
        session["username"] = ""
        return redirect(url_for("login"))

if __name__=="__main__":
        app.debug = True
        app.run()
