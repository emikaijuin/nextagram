from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw
from config import BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY
import braintree

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
  user = pw.ForeignKeyField(User, backref="donations")
  image = pw.ForeignKeyField(Image, backref="donations")
  message = pw.CharField()

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