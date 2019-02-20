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
from instagram_web.helpers.google_oauth import oauth

@sessions_blueprint.route("/new_oauth/<provider>", methods=["GET"])
def new_oauth(provider):
  redirect_uri = url_for("sessions.authorize", provider=provider, _external = True)
  return oauth.google.authorize_redirect(redirect_uri)

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

@sessions_blueprint.route('/authorize/<provider>', methods=["GET"])
def authorize(provider):
  if provider == "google":
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
  
  try:
    user = User.get(email = email)
    login_user(user)
    flash(f"Welcome, {user.username}.")
    return redirect(url_for('users.show', username = user.username))
  except:
    flash("Sorry, we weren't able to find a user with that email.")
    return redirect("/")

  
