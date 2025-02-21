from extensions import db
from flask import redirect, url_for, render_template, request, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from src.utils.email import send_email
from src.accounts.token import generate_token, confirm_token
from models.user import User
from datetime import datetime

userr = Blueprint('userr', __name__)

@userr.route('/login')
def login():
    return render_template('signup_login.html')

@userr.route('/signup', methods = ['POST'])
def signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    cpassword = request.form.get('confirm_password')

    if password != cpassword:
        flash("Password and confirm password didn't match!")
        return render_template('signup_login.html', signup_checked = True)

    # print(email, username, password, cpassword, flush=True)

    user = User.query.filter_by(email=email).first()

    # print(user, user.email, user.password, user.username, flush=True)

    if user:
        flash('Email address already exists')
        return redirect(url_for('userr.login'))
    
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), username=username)

    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.email)
    confirm_url = url_for("userr.confirm_email", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(new_user.email, subject, html)

    login_user(new_user)

    flash("A confirmation email has been sent via email.", "success")
    # return redirect(url_for("accounts.inactive"))

    return redirect(url_for('userr.inactive'))

@userr.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    # print(email, password, flush=True)
    user = User.query.filter_by(email=email).first()
    # print(user, flush=True)
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('userr.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('toddo.todo'))


@userr.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('userr.login'))


@userr.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_verified:
        flash("Account already confirmed.", "success")
        return redirect(url_for("toddo.todo"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_verified = True
        user.verified_on = datetime.now()
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
        return redirect(url_for("toddo.todo"))
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for('userr.inactive'))


@userr.route("/inactive")
@login_required
def inactive():
    if current_user.is_verified:
        return redirect(url_for("toddo.todo"))
    return render_template("inactive.html")


@userr.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_verified:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("toddo.todo"))
    token = generate_token(current_user.email)
    confirm_url = url_for("userr.confirm_email", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("userr.inactive"))

@userr.route("/forgot-password", methods=["GET"])
def forgot_password():
    return render_template('forgot-password.html')

@userr.route("/forgot-password", methods=["POST"])
def verify_and_send_passlink():
    email = request.form.get("email")
    user = User.query.filter_by(email = email).first()
    if not user: 
        flash("Invalid email or email not found.", "danger")
        return redirect(url_for('userr.forgot_password'))
    
    token = generate_token(user.email)
    password_reset_url = url_for("userr.password_reset_pre", token=token, _external=True)
    html = render_template("password-reset-email.html", reset_url=password_reset_url)
    subject = "Password reset email"
    send_email(user.email, subject, html)

    flash("Password reset email is sent.", "success")
    return redirect(url_for("userr.forgot_password"))


@userr.route("/password-reset/<token>", methods=["GET"])
def password_reset_pre(token):
    email = confirm_token(token)
    user = User.query.filter_by(email = email).first()
    if not user: 
        flash("404 Not Found.")
        return render_template("404-not-found.html")
    
    return render_template("password-reset.html")


@userr.route("/password-reset/<token>", methods=["POST"])
def password_reset_post(token):
    email = confirm_token(token)
    user = User.query.filter_by(email = email).first()
    password = request.form.get('new_password')
    cpassword = request.form.get('confirm_password')
    if password != cpassword:
        flash("Password and confirm password didn't match.")
        return render_template('password-reset.html')
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    flash("Password reset successful.")
    return redirect(url_for('userr.login'))
