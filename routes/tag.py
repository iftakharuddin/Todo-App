from app import db, app
from flask import render_template

@app.route("/tags")
def tags():
    return render_template("tags.html")