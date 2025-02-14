from flask import Flask, render_template
from controllers.attraction import attraction
from controllers.user import user
from controllers.booking import booking
from controllers.order import order
import os

# ===================================================================================== #

app = Flask(__name__, template_folder="./views/templates", static_folder="./views/static")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = os.getenv("TDTW_SECRET_KEY")

app.register_blueprint(attraction)
app.register_blueprint(user)
app.register_blueprint(booking)
app.register_blueprint(order)

# Pages
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


@app.route("/member")
def member():
	return render_template("member.html")


@app.route("/booking")
def booking():
	return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


if __name__ == "__main__":
	app.run(port=3000)
