from flask import Blueprint
from flask.templating import render_template

events = Blueprint(__name__, "events")

@events.route("/")
def home():
    return render_template("events.html")

@events.route("/<id>")
def event(id):
    return render_template("event.html")