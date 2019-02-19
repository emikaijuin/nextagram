from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw
from config import BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY, SENDGRID_PRIVATE_KEY
import braintree
import sendgrid
import os
from sendgrid.helpers.mail import *

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    braintree.Environment.Sandbox,
    merchant_id = BRAINTREE_MERCHANT_ID,
    public_key = BRAINTREE_PUBLIC_KEY,
    private_key = BRAINTREE_PRIVATE_KEY
  )
)

class Donation(BaseModel):
  amount = pw.DecimalField()
  donor = pw.ForeignKeyField(User, backref="received_donations")
  image = pw.ForeignKeyField(Image, backref="donations")
  message = pw.CharField()
  recipient = pw.ForeignKeyField(User, backref="submitted_donations")

  @classmethod
  def submit_to_braintree(cls, nonce_from_the_client, amount):
    nonce_from_the_client = nonce_from_the_client
    result = gateway.transaction.sale({
      "amount":amount,
      "payment_method_nonce": nonce_from_the_client,
      "options": {
        "submit_for_settlement": True
      }
    })

    return result

  def notify_recipient(self, donor_name, amount, message):
    print("!!!!!!!!!!!!!!!!!!!!!!!!")
    print(SENDGRID_PRIVATE_KEY)
    sg = sendgrid.SendGridAPIClient(apikey= SENDGRID_PRIVATE_KEY)
    from_email = Email("test@example.com")
    to_email = Email("emikaijuin@gmail.com")
    subject = "You received a donation!"
    content = Content("text/plain", f"You received ${amount} from {donor_name}! They said: {message}")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())