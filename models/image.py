from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
from werkzeug.utils import secure_filename
from helpers import *

class Image(BaseModel):
  url = pw.CharField()
  user = pw.ForeignKeyField(User, backref="images")

  def upload(self, request):
    self.errors = []
    self.validate_file(request)
  

    if len(self.errors) == 0: # validate file attachment before uploading to S3
      response = upload_file_to_s3(request.files['image_file'], S3_BUCKET)
      self.validate_upload(response)
      if len(self.errors) == 0: # validate Amazon upload was successful
        return response
    return 0

  def validate_file(self, request):
    if "image_file" not in request.files:
      self.errors.append("No image_file key in request.files")
    if request.files["image_file"].filename == "":
      self.errors.append("Please select a file")

  def validate_upload(self, response):
    if self.url not in response: # Need to confirm none of the Amazon failure messages do not include filename.
      self.errors.append(response)

  @hybrid_property
  def remote_url(self):
    if self.url:
      return S3_LOCATION + self.url
    else:
      return ""