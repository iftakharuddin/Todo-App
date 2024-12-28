from extensions import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    complete = db.Column(db.Boolean)
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    priority_level = db.Column(db.String(10), default='medium', nullable=False)  # Use Enum for priority
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key for use
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    tags = db.relationship('Tag', secondary='todotag', backref='todo', lazy=True)


    def __init__(self, title, priority_level = 'medium', user_id = 0):
        self.title = title
        self.complete = False
        self.priority_level = priority_level
        self.user_id = user_id