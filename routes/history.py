from app import db, app
from flask import render_template

@app.route("/history")
def history():
    return render_template("history.html")