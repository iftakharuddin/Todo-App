from models.todo import Todo
from app import db, app
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from src.utils.decorators import check_is_confirmed

@app.route('/todo')
@login_required
@check_is_confirmed
def todo():
    todos = Todo.query.filter_by(user_id=current_user.id)
    return render_template('todo.html', todo_list=todos)

@app.route('/todo/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')
    priority = request.form.get('priority')
    todo = Todo(title, priority, current_user.id)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/todo/update/<int:id>')
@login_required
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/todo/edit/<int:id>')
@login_required
def edit_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('edit_todo.html', todo=todo)

@app.route('/todo/save/<int:id>', methods=['POST'])
@login_required
def save_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo: 
        todo.title = request.form.get('title')
        todo.priority_level = request.form.get('priority')
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/todo/delete/<int:id>')
@login_required
def delete_todo(id = -1):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/todo/bulkadd')
@login_required
def todo_bulkadd():
    for i in range(0,100):
        todo = Todo('test'+str(i))
        db.session.add(todo)
    db.session.commit()
    return 'Done'

# To query the database, edit the /search route next:
@app.route('/search', methods=['GET'])
def search():
   query = request.args.get('query')
   results = Todo.query.filter(Todo.title.ilike(f"%{query}%"), Todo.user_id == current_user.id).all()
   
   return jsonify([{"id": r.id,
    "title": r.title, 
    "complete": r.complete, 
    "created_datetime": r.created_datetime, 
    "priority_level": r.priority_level} 
    for r in results])