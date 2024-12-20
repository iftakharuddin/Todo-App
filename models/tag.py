from app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Todotag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)    
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)    

    def __init__(self, todo_id, tag_id):
        self.todo_id = todo_id
        self.tag_id = tag_id
