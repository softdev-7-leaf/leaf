from flask import Flask, render_template, request, redirect, url_for, session, escape, flash
import database
import os, urllib2, json
import pymongo
import re
from pymongo import MongoClient
from urllib2 import urlopen
from pymongo import Connection


app=Flask(__name__)
#abc
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
abc = urllib2.Request("https://data.cityofnewyork.us/resource/mreg-rk5p.json")
sat = urllib2.Request("https://data.cityofnewyork.us/resource/zt9s-n5aj.json")
text = urlopen(abc)
sattext = urlopen(sat)
text2 = text.read()
sattext2 = sattext.read()
schoolslist = json.loads(text2)
schoolslist2 = json.loads(sattext2)
dbn_codes = []
c= Connection()
client = MongoClient()
db = client.leaf
c.drop_database(db)
users = db.users
schoolinfo=db.one
ratedschools={}
schoolinfo.insert(schoolslist)
schoolinfo.insert(schoolslist2)
shortened = schoolinfo.aggregate([{"$group": {
        "_id": "$dbn",
        "printed_school_name": {"$first": "$printed_school_name"},
        "program_name": {"$addToSet": "$program_name"},
        "program_code": {"$addToSet": "$program_code"},
        "directory_page_": {"$first": "$directory_page_"},
        "borough": {"$first": "$borough"},
        "interest_area": {"$addToSet": "$interest_area"},
        "writing_mean": {"$addToSet": "$writing_mean"},
        "critical_reading_mean": {"$addToSet": "$critical_reading_mean"},
        "mathematics_mean": {"$addToSet": "$mathematics_mean"},
        "number_of_test_takers": {"$addToSet": "$number_of_test_takers"}
        }}])
#schoolinfo.group(key={"dbn":1},
schoolinfo2 = db.two
schoolinfo2.insert(shortened['result'])
#for a in schoolslist:
#        dbn_codes.append(a['dbn'])


#highschools= urlopen(request)
#response = highschools.read()
def refined_aggregate(coll):
    dummyvar = coll.aggregate([{"$group":{
        "_id": "$dbn",
        "printed_school_name": {"$first": "$printed_school_name"},
        "program_name": {"$addToSet": "$program_name"},
        "program_code": {"$addToSet": "$program_code"},
        "directory_page_": {"$first": "$directory_page_"},
        "borough": {"$first": "$borough"},
        "interest_area": {"$addToSet": "$interest_area"},
        "writing_mean": {"$addToSet": "$writing_mean"},
        "critical_reading_mean": {"$addToSet": "$critical_reading_mean"},
        "mathematics_mean": {"$addToSet": "$mathematics_mean"},
        "number_of_test_takers": {"$addToSet": "$number_of_test_takers"},
        "rating":{"$avg": "$rating"}
        }}])
    #print dummyvar['result']
    coll.remove({})
    coll.insert(dummyvar['result'])


def validate_email(email):
    at = str.find(email, "@")
    period = str.find(email, ".")
    if (at <= 0) or (period <= 0) or (at >= len(email)-5) or (period >= len(email) - 3):
        return False
    else:
        return True

def upper(password):
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for p in password:
        if (str.find(uppers, p) >= 0):
            return True
    return False

def lower(password):
    lowers = "abcdefghijklmnopqrstuvwxyz"
    for p in password:
        if (str.find(lowers, p) >= 0):
            return True
    return False

def digit(password):
    digits = "1234567890"
    for p in password:
        if (str.find(digits, p) >= 0):
            return True
    return False
def validate_password(password):
    return (len(password) >= 5) and (len(password) <= 21) and (upper(password)) and (lower(password)) and (digit(password))


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():

        if request.method=="GET":
                #print urlopen(abc).read()
                return render_template("login.html")
                #print response
        else:
                #print response
                username = request.form["username"]
                password = request.form["password"]
                button = request.form["b"]
                if button == "Login":
                    user = users.find_one({'username': username})
                    if user == None:
                        flash("Not a Valid Username")
                        return redirect(url_for('login'))
                    elif user['password'] != password:
                        flash("Password and username do not match")
                        return redirect(url_for('login'))
                    else:
                            #flash("Welcome to Leaf")
                        session['username'] = username
                        session['password'] = password
                        session['gender'] = user['gender']
                        session['emailaddress'] = user['emailaddress']
                        session['month'] = user['month']
                        session['day'] = user['day']
                        session['year'] = user['year']
                        print ratedschools
                        if username not in ratedschools:
                            ratedschools['%s' % username] = []
                        if user['first'] == 0:
                            return redirect(url_for('profile'))
                        return redirect(url_for('user_home', username=username))
                #flash("Welcome to leaf")
				#flash("Welcome to Leaf")
				#return redirect(url_for('user_home', username=username))
		else: 
                    return redirect(url_for('register'))
def add_user(username, password, emailaddress, gender, month, day, year) : #, age
    user = {'username' : username, 
                        'password' : password,
                        'emailaddress' : emailaddress,
                        'gender' : gender,
                        'month' : month,
                        'day' : day,
                        'year' : year,
                        'first' : 0,
                        #'age' : age
                        }
    return users.insert(user)
@app.route("/register",methods=["GET","POST"])
def register():
	if request.method=="GET":
                m = []
                for x in range(1,13):
                    m.append(x)
                d = []
                for x in range(1,32):
                    d.append(x)
                y = []
                for x in range(97,1,-1):
                    y.append(x + 1919)
                return render_template("register.html", m=m, d=d, y=y)
	else: 
        	button = request.form["b"]
		if button == "Login":
        	        return redirect(url_for('login'))
         	username = request.form["username"]
        	password = request.form["password"]
		password2 = request.form["password2"]
		gender = request.form["gender"]
                month = request.form["month"]
                day = request.form["day"]
                year = request.form["year"]
        	emailaddress = request.form["emailaddress"]
		if users.find_one({'username': username}) != None:
			flash("The username you submitted is already taken, please try again.")
			return redirect(url_for('register'))
		if users.find_one({'emailaddress': emailaddress}) != None:
			flash("The email you submitted already has an account tied to it, please try again.")
			return redirect(url_for('register'))
		if not validate_email(str(emailaddress)):
			flash("This is not an email")
			return redirect(url_for('register'))
		if not password == password2:
			flash("Passwords do not match")
			return redirect(url_for('register'))
		if not validate_password(str(password)):
			flash("The password does not meet the above requirements.")
			return redirect(url_for('register'))
		add_user(username, password, emailaddress, gender, month, day, year) #, age
		flash("You've sucessfully registered, now login!")
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
    	session.pop('username', None)
    	session.pop('password', None)
    	session.pop('first_name', None)
    	session.pop('last_name', None)
	flash("You have successfully logged out")
    	return redirect(url_for('login'))

@app.route("/home/<username>",methods=["GET","POST"])
def user_home(username=None):
    if request.method == "GET":
        session['username'] = username
        #print session['username']
        session.modified=True
        return render_template("home.html", username=username)
    else:
        if 'b' in request.form:
            button = request.form["b"]
    	    if button=="Logout":
                    return redirect(url_for("logout"))
        value = request.form['q']
        #print "this is the value"
        #print value
        return redirect(url_for("search",field=value))


@app.route('/school/<code>', methods=["GET","POST"])
def school(code = None):
        if request.method == "GET":
                #print "YES!"  
                #print schoolinfo.find_one({"dbn": code})
                a = schoolinfo2.find_one({"_id": code})
                #print schoolinfo2     
                if a != None:
                        if 'rating' in a:
                            #print "YES!----------------------"
                            total = 0.0
                            for n in a['rating']:
                                total = total + float(n)
                            rating = total / len(a['rating'])
                        else:
                            rating = "None"
                        #print "YES! 2--------------------------------"
                        #name = schoolslist[n]['printed_school_name']
                        #program_code = schoolslist[n]['program_code']
                        #print rating
                        return render_template('schools.html',name=a['printed_school_name'], 
                                dbn=a['_id'], 
                                program_code=a['program_name'],
                                critread=a['critical_reading_mean'],
                                mathematics= a['mathematics_mean'],
                                writing= a['writing_mean'],
                                Interest= a['interest_area'],
                                username=session['username'],
                                rating=rating) #program_code=program_code, dbn=dbn)
        else: 
                if 'searchbar' in request.form:
                    field = request.form['searchbar']
                    return redirect(url_for("search", field=field ))
                elif 'rating' in request.form:
                    rating = request.form['rating']
                    #print "THIS IS THE RATING"
                    #print rating
                    username = session['username']
                    if not code in ratedschools['%s' % session['username']]:
                        if 'rating' in schoolinfo2.find_one({"_id":code}):
                            currentratings=schoolinfo2.find_one({"_id":code})['rating']
                        #print currentratings
                        #print rating
                            currentratings.append(rating)
                        #print currentratings
                            schoolinfo2.update({"_id":code},{"$set": {"rating": currentratings}})
                            ratedschools['%s'% session['username']].append(code)
                        #print schoolinfo2.find_one({"_id":code})['rating']
                        else:
                            newarray=[]
                            newarray.append(rating)
                            schoolinfo2.update({"_id":code},{"$set":{"rating":newarray}})
                            ratedschools['%s' % session ['username']].append(code)
                    else:
                        flash("You have already rated this once. You cannot rate again")
                    #print schoolinfo2.find_one({'_id':code})
                    return redirect(url_for("school", code=code))


@app.route('/search/', methods=["GET","POST"])
def search(results=None):
        print session['username']
        field = request.args.get('field')
        field2 = field.split(" ")
        #print field
        results = []
        #print "2.0"
        fieldstring = ".*"
        for value in field2:
            fieldstring = fieldstring + value + ".*"
        regx = re.compile(fieldstring, re.IGNORECASE)
        n = schoolinfo2.find({ "$or": [
                {"printed_school_name": {"$regex": regx}},
                {"program_code":{"$regex": regx}},
                {"directory_page_":{"$regex": regx}},
                {"dbn":{"$regex": regx}},
                {"urls":{"$regex": regx}},
                {"borough":{"$regex": regx}},
                {"selection_method":{"$regex": regx}},
                {"program_name":{"$regex": regx}}]})
        for x in n:
                if not (x in results):
                        results.append(x)
        #print "This is the array length" + str(len(results))
        #print "3.0--------------------------------------------------"
        #print results
        #print "4.0-----------------------------------------------------------"
        if request.method == "GET":
                #print "GOT TO THIS STEP-----------------"
        #results = request.args.get("results")
        #for x in results:
                #print x
                #print "\n"
        #print 'These are the session results'
        #print escape(session['results'])
                return render_template("search.html",results=results, Search="'"+field+"'", username=session['username'])
        else:
            field = request.form['searchbar']
            return redirect(url_for("search", field=field))
@app.route("/editprofile", methods=["GET","POST"])
def editprofile():
    if request.method=="GET":
        return render_template("editprofile.html", username=session['username'],emailaddress= session['emailaddress'], gender = session['gender'], month= session['month'], day= session['day'], year = session['year'])
    else:
        if 'edit' in request.form:
            button = request.form["edit"]
    	    if button=="edit":
                user = users.find_one({'username': session['username']})
                emailaddress = request.form['emailaddress']
                gender = request.form['gender']
                if users.find_one({'emailaddress': emailaddress}) != None and not session['emailaddress'] == emailaddress:
                    flash("The email you submitted already has an account tied to it, please try again.")
                    return redirect(url_for('editprofile'))
                if not validate_email(str(emailaddress)):
                    flash("This is not an email")
                    return redirect(url_for('editprofile'))
                users.update(user, {
                        'username' : session['username'], 
                        'password' : session['password'],
                        'emailaddress' : emailaddress,
                        'gender' : gender,
                        'first' : 1,
                        'month' : session['month'],
                        'day' : session['day'],
                        'year' : session['year'],
                        #'age' : age
                        })
                session['emailaddress'] = emailaddress
                session['gender'] = gender
                session['first'] = 1
                return redirect(url_for("profile"))
        if 'pwchange' in request.form:
            button = request.form["pwchange"]
            if button=="pwchange":
                user = users.find_one({'username': session['username']})
                password = request.form['password']
                password2 = request.form['password2']                    
                password3 = request.form['password3']
                if not password == user['password']:
                    flash("Wrong password")
                    return redirect(url_for('editprofile'))
                if not password2 == password3:
                    flash("Passwords do not match")                        
                    return redirect(url_for('editprofile'))
                if not validate_password(str(password)):
                    flash("The password does not meet the requirements: The length must be greater than 4 and less than 20, and have at least one digit, one uppercase letter and one lowercase letter.")
                    return redirect(url_for('editprofile'))
                users.update(user, {
                        'username' : session['username'], 
                        'password' : password2,
                        'emailaddress' : session['emailaddress'],
                        'gender' : session['gender'],                            
                        'first' : 1,
                        #'age' : age
                        })
                session['password'] = password
                session['first'] = 1
                return redirect(url_for("profile"))
        if 'searchbar' in request.form:
            field = request.form['searchbar']
            return redirect(url_for("search", field=field))
            

@app.route("/profile", methods=["GET","POST"])
def profile():
    if request.method=="GET":
        return render_template("profile.html",username= session['username'],emailaddress= session['emailaddress'], gender = session['gender'], month = session['month'], day = session['day'], year = session['year'])
    else:
        if 'edit' in request.form:
            button = request.form['edit']
            if button=="edit":
                return redirect(url_for('editprofile'))
        if 'searchbar' in request.form:
            field = request.form['searchbar']
            return redirect(url_for("search", field=field))

@app.route("/about", methods=["GET","POST"])
def about():
    if request.method=="GET":
        print session['username']
        return render_template("about.html", username= session['username'])
    else:
        if 'searchbar' in request.form:
            field = request.form['searchbar']
            return redirect(url_for("search", field=field))
@app.route("/help", methods=["GET","POST"])
def help():
    if request.method=="GET":
        return render_template("help.html", username= session['username'])
    else:
        if 'searchbar' in request.form:
            field = request.form['searchbar']
            return redirect(url_for("search", field=field))

if __name__=="__main__":
        app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
        app.debug = True
        app.run()
        
