
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_login import LoginManager
from extensions import db, mail

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
# app.config.from_object('config.DevelopmentConfig')

db.init_app(app)
cache = Cache(app)
migrate = Migrate(app, db)
mail.init_app(app)

from routes.todo import toddo
from routes.user import userr
from routes.tag import tagg
from routes.history import archive
from routes.profile import proffile
from models.todo import Todo
from models.user import User

app.register_blueprint(toddo)
app.register_blueprint(userr)
app.register_blueprint(tagg)
app.register_blueprint(archive)
app.register_blueprint(proffile)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/')
def index(name=None):
    return redirect(url_for("userr.login"))

@app.route('/home')
def home():
    print("I am from Home.")
    return redirect(url_for('index'))

@app.route('/user/<name>')
def user(name):
    return "This is a user " + name


@app.route('/cache/<country>/<capital>')
def cache_set(country, capital):
    cache.set(country,{'country':capital})
    return 'Done'

@app.route('/cache/<country>')
def cache_get(country):
    resp = cache.get(country)
    print(resp)
    if resp is not None:
        return cache.get(country)
    else:
        return 'None'

if __name__=="__main__":
    app.run()

