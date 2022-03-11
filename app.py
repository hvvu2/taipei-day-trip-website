import os
from flask import Flask, render_template
from controllers.api import api

# ===================================================================================== #

app = Flask(__name__, template_folder="./views/templates", static_folder="./views/static")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(api, prefix="/api")

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == "__main__":
	app.run(port=3000)
