import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User, Relationship
from models.image import Image
from models.donation import Donation
import logging

# Configure app logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Initialize and configure app
web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

# Require CSRF tokens on post requests
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(id=user_id)
