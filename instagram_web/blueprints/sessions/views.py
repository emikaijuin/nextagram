# import functools
from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash
from models.user import *
from flask_login import login_user, current_user, logout_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route("/new", methods=["GET"])
def new():
  return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=["POST"])
def create():
  user = User.get(email= request.form['email'])
  if check_password_hash(user.password_digest, request.form['password']):
    login_user(user)
    flash(f"Welcome, {user.username}")
    return redirect(url_for('home'))
  else:
    return render_template(
      'sessions/new.html',
      errors = user.errors,
      email = user.email
    )

@sessions_blueprint.route('/destroy', methods=["POST"])
def destroy():
  user = User.get_by_id(User.get_id(current_user))
  logout_user()
  flash(f"You signed out.")
  return redirect(url_for('home'))
