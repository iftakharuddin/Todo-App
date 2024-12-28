from extensions import db
from flask import render_template, Blueprint
from models.todo import Todo
from flask_login import login_user, login_required, logout_user, current_user

archive = Blueprint('archive', __name__)

@archive.route("/history")
def history():
    todos = Todo.query.filter_by(user_id=current_user.id, deleted=True).all()
    for todo in todos: 
        todo.created_datetime = todo.created_datetime.strftime("%B %d, %Y %I:%M %p")
    return render_template("history.html", todo_list = todos)