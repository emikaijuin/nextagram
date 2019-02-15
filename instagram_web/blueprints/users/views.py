from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from models.user import *

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
  user = User(
    email = request.form['email'],
    username = request.form['username'],
    password_digest = generate_password_hash(request.form['password'])
  )

  if user.save():
    session['user_id'] = user.id
    return redirect(url_for('users.show', username=user.username))
  else:
    return render_template(
      'new.html', 
      errors=user.errors,
      username=user.username,
      email=user.email
    )

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return f"{username}'s profile"


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
