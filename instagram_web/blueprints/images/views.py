from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.image import *
from models.user import *
from flask_login import current_user

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder="templates")

@images_blueprint.route("/new", methods=["GET"])
def new():
  return render_template("images/new.html")

@images_blueprint.route("/", methods=["POST"])
def create():
  image = Image(
    url = request.files['image_file'].filename,
    user = current_user.id
  )
  if image.upload(request) and image.save():
    return redirect(url_for('.show', id=image.id))
  else:
    return render_template(
      "images/new.html",
      image_file = request.files["image_file"]
    )

@images_blueprint.route("/<id>", methods=["GET"])
def show(id):
  image = Image.get(id=id)
  return render_template(
    "images/show.html",
    image_url = image.remote_url
  )
