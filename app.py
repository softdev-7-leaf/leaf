from flask import Flask, render_template, request, redirect, url_for, session, escape, flash
import database
import os, urllib2, json
import pymongo
from pymongo import MongoClient
from urllib2 import urlopen
from pymongo import Connection


app=Flask(__name__)
app.secret_key = os.urandom(24)
abc = urllib2.Request("https://data.cityofnewyork.us/resource/mreg-rk5p.json")
text = urlopen(abc)
text2 = text.read()
schoolslist = json.loads(text2)
dbn_codes = []
c= Connection()
client = MongoClient()
db = client.leaf
c.drop_database(db)
schoolinfo=db.one
schoolinfo.insert(schoolslist)

#for a in schoolslist:
#        dbn_codes.append(a['dbn'])


#highschools= urlopen(request)
#response = highschools.read()

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():

        if request.method=="GET":
                print urlopen(abc).read()
                return render_template("login.html")
                #print response
        else:
                #print response
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
        if request.method=="GET":
                return render_template("register.html")
        else:
                button = request.form["b"]
                if button == "Login":
                        return redirect(url_for('login'))
                        username = request.form["username"]
                        password = request.form["password"]
                        emailaddress = request.form["emailaddress"]
                        if not database.addUser(username, password, emailaddress, gender, age):
                                flash("There was a problem with what you submitted.")
                                return redirect(url_for('register'))
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

@app.route('/school/<code>', methods=["GET","POST"])
def school(code = None):
        if request.method == "GET":
                print "YES!"  
                print schoolinfo.find_one({"dbn": code})
                a = schoolinfo.find_one({"dbn": code})
                #print a     
                if a != None:
                        print "YES! 2--------------------------------"
                        #name = schoolslist[n]['printed_school_name']
                        #program_code = schoolslist[n]['program_code']
                        return render_template('schools.html',name=a['printed_school_name']) #program_code=program_code, dbn=dbn)
                else:
                        return render_template('user.html')
        else:
                field = request.form['searchbar']
                #print field
                results = []
                n = schoolinfo.find({ "$or": [
                        {"printed_school_name": {"$regex": ".*" +field + ".*"}},
                        {"program_code":{"$regex": ".*" +field + ".*"}},
                        {"directory_page_":{"$regex": ".*" +field + ".*"}},
                        {"dbn":{"$regex": ".*" +field + ".*"}},
                        {"urls":{"$regex": ".*" +field + ".*"}},
                        {"borough":{"$regex": ".*" +field + ".*"}},
                        {"selection_method":{"$regex": ".*" +field + ".*"}},
                        {"program_name":{"$regex": ".*" +field + ".*"}}]})
                for x in n:
                        if not x in results:
                                results.append(x)
                print "This is the array length" + str(len(results))
                return render_template('search.html', results=results)

#@app.route('/search/', methods=["GET","POST"])
#def search():
 #       if request.method == "GET":
 #               resultslist = []




if __name__=="__main__":
        app.debug = True
        app.run()
