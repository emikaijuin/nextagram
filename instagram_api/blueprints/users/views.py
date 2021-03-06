from flask import Blueprint, jsonify
from models.user import User
from helpers import map_to_s3
from flask_login import current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route("/<username>", methods=['GET'])
@jwt_required
def show(username):
    current_user = User.get(email = get_jwt_identity())
    user = User.get(username = username)
    return jsonify(
        images = map_to_s3(user.images),
        profile_user = {
            **user.to_json(),
        },
        current_user = {**current_user.to_json()} if current_user.is_authenticated else False,
        current_user_is_following = True if current_user.is_authenticated and current_user.is_following(username) else False
    )
