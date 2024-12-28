from models.tag import Tag
from extensions import db
from flask import Flask, redirect, url_for, render_template, request, jsonify, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from src.utils.decorators import check_is_confirmed

tagg = Blueprint('tagg', __name__)

@tagg.route("/tags")
@login_required
@check_is_confirmed
def tags():
    tags = Tag.query.filter_by(user_id=current_user.id, deleted=False)
    return render_template("tags.html", tag_list=tags)

@tagg.route('/tag/add', methods=['POST'])
@login_required
def add_tagg():
    name = request.form.get('name')
    tag = Tag(name, current_user.id)
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('tags'))

@tagg.route('/tag/edit/<int:id>')
@login_required
def edit_tag(id):
    tag = Tag.query.filter_by(id=id).first()
    return render_template('edit_tag.html', tag=tag)

@tagg.route('/tag/save/<int:id>', methods=['POST'])
@login_required
def save_tag(id):
    tag = Tag.query.filter_by(id=id).first()
    if tag: 
        tag.name = request.form.get('name')
        db.session.commit()
    return redirect(url_for('tags'))

@tagg.route('/tag/delete/<int:id>')
@login_required
def delete_tag(id = -1):
    tag = Tag.query.filter_by(id = id).first()
    todo.deleted = True
    db.session.commit()
    return redirect(url_for('tags'))