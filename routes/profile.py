from app import db, app
from models.user import User
from flask import render_template
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/profile")
def profile():
    user = User.query.filter_by(id = current_user.id).first()
    user.created_at = user.created_at.strftime("%A, %B %d, %Y %I:%M %p")
    user.verified_on = user.verified_on.strftime("%A, %B %d, %Y %I:%M %p")
    # print(user.created_at, flush=True)
    return render_template("profile.html", user=user)