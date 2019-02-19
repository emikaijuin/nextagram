from flask import(
  Blueprint, Flask, redirect, render_template, url_for, request, flash
)
from models.donation import gateway, Donation
from models.image import Image
from models.user import User
from flask_login import current_user

donations_blueprint = Blueprint(
  'donations',
  __name__,
  template_folder='templates'
)

@donations_blueprint.route("/new", methods=["GET"])
def new(image_id):
  client_token =  gateway.client_token.generate() # does not currently support remembering returning braintree clients
  return render_template(
    "donations/new.html",
    client_token = client_token,
    image_id = image_id
  )

@donations_blueprint.route("/checkout", methods=["POST"])
def checkout(image_id):
  nonce_from_the_client = request.form['payment_method_nonce']
  amount = request.form['amount']
  result = Donation.submit_to_braintree(nonce_from_the_client, amount)
  if result.is_success:
    recipient = User.get(id = Image.get(id=image_id).user_id)
    donation = Donation(
      amount = amount,
      donor = current_user.id,
      image = image_id,
      message = request.form['message'],
      recipient = recipient.id
    )
    donation.save()
    flash(f"You donated {amount} dollars to {current_user.username}!")
    return redirect(url_for("users.show", username = recipient.username))
  else:
    flash("There were issues with your payment, please fix and try again.")
    for error in result.errors.deep_errors:
      flash(error.message)
    return redirect(f"/images/{image_id}/donations/new")