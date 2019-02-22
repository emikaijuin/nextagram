from flask import Flask, request, jsonify, Blueprint
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from flask_login import login_user

sessions_api_blueprint = Blueprint("sessions_api",
                                __name__,
                                url_prefix="/api/v1/sessions")
# Request JWT
@sessions_api_blueprint.route("/new", methods=["POST"])
def new():
  if not request.is_json:
    return jsonify({"msg": "Missing JSON in request"}), 400
  email = request.json.get('email', None)
  password = request.json.get('password', None)
  if not email:
    return jsonify({"msg": "Missing email parameter"}), 400
  if not password:
    return jsonify({"msg": "Missing password parameter"}), 400

  user = User.get_or_none(email=email)
  if user and check_password_hash(user.password_digest, password):
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, current_user = user.username), 200
  else:
    return jsonify({"msg": "Bad email or password"}), 401
