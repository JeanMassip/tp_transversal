
from flask import Blueprint
from flask.templating import render_template
import requests

events = Blueprint(__name__, "events")


@events.route("/")
def home():
    # r = requests.get("http://127.0.0.1:8000/events")
    # if r.ok:
    #     return render_template("events.html", data=r.json())
    # else:
    #     return "Sorry, something went wrong... Try again later !"
    return render_template("events.html")


@events.route("/<id>")
def event(id):
    return render_template("event.html")
