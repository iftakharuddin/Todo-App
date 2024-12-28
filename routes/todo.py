from models.todo import Todo
from models.tag import Tag, Todotag
from extensions import db
from flask import Flask, redirect, url_for, render_template, request, jsonify, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from src.utils.decorators import check_is_confirmed

toddo = Blueprint('toddo', __name__)

@toddo.route('/todo')
@login_required
@check_is_confirmed
def todo():
    todos = Todo.query.filter_by(user_id=current_user.id, deleted=False).all()
    tags = Tag.query.filter_by(user_id=current_user.id, deleted=False).all()
    for todo in todos: 
        todo.created_datetime = todo.created_datetime.strftime("%B %d, %Y %I:%M %p")
    return render_template('todo.html', todo_list=todos, tag_list=tags)

@toddo.route('/todo/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')
    priority = request.form.get('priority')
    todo = Todo(title, priority, current_user.id)
    db.session.add(todo)
    db.session.flush()
    # print(todo.id, flush=True)
    tags = request.form.getlist('tag')
    for tag in tags:
        todotag = Todotag(todo.id, int(tag))
        db.session.add(todotag)
    db.session.commit();
    return redirect(url_for('todo'))

@toddo.route('/todo/update/<int:id>')
@login_required
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todo'))

@toddo.route('/todo/edit/<int:id>')
@login_required
def edit_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    tags = Tag.query.filter_by(user_id=current_user.id).all()
    return render_template('edit_todo.html', todo=todo, tags = tags)

@toddo.route('/todo/save/<int:id>', methods=['POST'])
@login_required
def save_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo: 
        todo.title = request.form.get('title')
        todo.priority_level = request.form.get('priority')
        db.session.commit()
    return redirect(url_for('todo'))

@toddo.route('/todo/delete/<int:id>')
@login_required
def delete_todo(id = -1):
    todo = Todo.query.filter_by(id = id).first()
    todo.deleted = True
    db.session.commit()
    return redirect(url_for('todo'))

@toddo.route('/todo/bulkadd')
@login_required
def todo_bulkadd():
    for i in range(0,100):
        todo = Todo('test'+str(i))
        db.session.add(todo)
    db.session.commit()
    return 'Done'

# To query the database, edit the /search route next:
@toddo.route('/search', methods=['GET'])
def search():
   query = request.args.get('query')
   results = Todo.query.filter(Todo.title.ilike(f"%{query}%"), Todo.user_id == current_user.id).all()
   
   return jsonify([{"id": r.id,
    "title": r.title, 
    "complete": r.complete, 
    "created_datetime": r.created_datetime, 
    "priority_level": r.priority_level} 
    for r in results])