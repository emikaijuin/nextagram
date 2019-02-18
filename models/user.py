from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from werkzeug.utils import secure_filename
from helpers import *
class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True, index=True)
    password_digest = pw.CharField(unique=False)
    avatar = pw.CharField(null=True)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append("Email is already taken, please login with existing email.")
        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append("Username is already taken, please try creating another.")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True
    
    def get_id(self):
        return str(self.id)

    def upload_file(self, request):
      if "user_file" not in request.files:
        return [False, "No user_file key in request.files"]
      file = request.files["user_file"]

      if file.filename == "":
        return [False, "Please select a file"]

      if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        self.avatar = output
        self.save()
        return [True, str(output)]

      else:
        return [False, "Avatar could not be uploaded to Amazon."]

    @hybrid_property
    def profile_image_url(self):
      if self.avatar:
        return S3_LOCATION + self.avatar
      else:
        return ""
        