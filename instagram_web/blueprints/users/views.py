from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from models.user import *
from flask_login import current_user, login_required

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
    if False in user.upload_file(request):
      flash("There was an issue uploading your profile picture, please try again.")
    session['user_id'] = user.id
    flash("Welcome to NEXTagram!")
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
  user = User.get(username= username)
  return render_template(
    "show.html",
    username = username,
    profile_image_url = user.profile_image_url,
    user_images = user.images
  )


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if id == User.get_id(current_user):
        user = User.get_by_id(id)
        return render_template(
            'edit.html',
            username = user.username,
            email = user.email,
            id = id
        )
    else:
        return "You can't go there"


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(str(current_user))
    if request.form['username']: user.username = request.form['username']
    if request.form['password']: user.password = request.form['password']
    if request.form['user_file']: user.upload_file(request)
    
    if user.save():
        return redirect(url_for(".show", username = user.username))
    else:
        return render_template(
            "edit.html",
            errors = user.errors,
            username = user.username,
            email = user.email
        )