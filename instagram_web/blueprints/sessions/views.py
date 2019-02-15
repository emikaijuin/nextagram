# import functools
from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash
from models.user import *

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
    session["user_id"] = user.id
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
  session.clear()
  flash(f"You signed out.")
  return redirect(url_for('home'))
