from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.image import *
from models.user import *

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder="templates/images")

@images_blueprint.route("/new", methods=["GET"])
def new():
  return render_template("images/new.html")

@images_blueprint.route("/", methods=["POST"])
def create():
  return "YOU DIDN'T UPLOAD ME!"