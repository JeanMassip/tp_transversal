from flask import Flask
from flask.templating import render_template
from events import events

app = Flask(__name__)
app.register_blueprint(events, url_prefix="/events")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)