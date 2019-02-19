from flask import(
  Blueprint, Flask, redirect, render_template, url_for, request
)
from models.donation import gateway, Donation
from flask_login import current_user

donations_blueprint = Blueprint(
  'donations',
  __name__,
  template_folder='templates'
)

@donations_blueprint.route("/new", methods=["GET"])
def new():
  client_token =  gateway.client_token.generate() # does not currently support remembering returning braintree clients
  return render_template(
    "donations/new.html",
    client_token = client_token
  )

@donations_blueprint.route("/checkout", methods=["POST"])
def checkout():
  nonce_from_the_client = request.form["payment_method_nonce"]

  result = gateway.transaction.sale({
    "amount": "10.00",
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
  })

@donations_blueprint.route("/<id>", methods=["GET"])
def show(id):
  return render_template("donations/show.html", )