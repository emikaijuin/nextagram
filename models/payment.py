from models.base_model import BaseModel
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

# class Payment(BaseModel):
#   pass