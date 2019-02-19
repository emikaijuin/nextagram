from flask import(
  Blueprint, flask, redirect, render_template, url_for
)
from models.payment import *
from flask_login import current_user

payments_blueprint = Blueprint(
  'payments',
  __name__,
  template_folder='templates'
)