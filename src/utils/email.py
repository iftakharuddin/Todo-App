from flask_mail import Message
from flask import current_app
from extensions import mail


def send_email(to, subject, template):
    if to == "iftakhar5129@gmail.com":
        return False
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)
    return True
