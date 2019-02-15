from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True, index=True)
    password_digest = pw.CharField(unique=False)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_email:
            self.errors.append("Email is already taken, please login with existing email.")
        if duplicate_username:
            self.errors.append("Username is already taken, please try creating another.")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True
    
    def get_id(self):
        return str(self.id)