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
    private = pw.BooleanField(default=False)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.profile_image_url,
            "private": self.private 
        }

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append("Email is already taken, please login with existing email.")
        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append("Username is already taken, please try creating another.")

    # Flask Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True
    
    def get_id(self):
        return str(self.id)

    # S3 Image Upload 

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
        return s3_url(self.avatar)
      else:
        return ""

    # Following

    def follow(self, followee):
      follow = Relationship(
          follower = self.id,
          following = followee.id
      )

      follow.save()

    def followers(self):
      return (User
              .select()
              .join(Relationship, on=(Relationship.follower_id == User.id))
              .where(Relationship.following == self.id)
            )

    def following(self):
        return (User
                .select()
                .join(Relationship, on=(Relationship.following_id == User.id))
                .where(Relationship.follower == self.id)
            )

    def follow(self, username):
        user = User.get(username = username)
        relationship = Relationship(
            follower_id = self.id,
            following_id = user.id
        )
        relationship.save()

    def unfollow(self, username):
        user = User.get(username = username)
        relationship = Relationship.delete().where(
            Relationship.follower_id == self.id,
            Relationship.following_id == user.id
        )
        relationship.execute()

    def is_following(self, username):
        user = User.get(username = username)
        return Relationship.get_or_none(
            follower_id = self.id,
            following_id = user.id,
            approved = True
        )

    def can_view(self, username):
        user = User.get(username = username)
        if self == user:
            return True
        if not user.private:
            return True
        if self.is_authenticated and self.is_following(username):
            return True
        return False

    def has_pending_request_to(self, username):
      user = User.get(username = username)
      relationship = Relationship.get_or_none(
        follower_id = self.id, 
        following_id = user.id
      )
      if relationship and relationship.approved == False:
        return True
      else:
        return False

class Relationship(BaseModel):
  follower = pw.ForeignKeyField(User)
  following = pw.ForeignKeyField(User)
  approved = pw.BooleanField(default=False)

  def approve(self):
      self.approved = True
      self.save()

  @classmethod
  def unapproved_requests(cls, user):
      return Relationship.select().where(
          Relationship.following_id == user.id,
          Relationship.approved == False
      )