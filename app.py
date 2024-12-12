
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
cache = Cache(app)
migrate = Migrate(app, db)
mail = Mail(app)

from routes.todo import *
from routes.user import *
from routes.tag import *
from routes.history import *
from routes.profile import *
from models.todo import Todo
from models.user import User

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route('/')
def index(name=None):
    return render_template('index.html', myname=name)

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

