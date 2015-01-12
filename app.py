from flask import Flask, render_template, request

app = Flask(__name__);

@app.route("/", methods = ["GET","POST"])
@app.route("/login", methods = ["GET","POST"])

if __name__ == "__main__":
	app.debug = True
	app.run()

