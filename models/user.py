from extensions import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verified_on = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username