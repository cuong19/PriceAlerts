import uuid

from src.common.database import Database
from src.common.utils import Utils
from src.models.alerts.alert import Alert
from src.models.users.errors import UserNotExistError, IncorrectPasswordError, \
    UserAlreadyRegisteredError, InvalidEmailError


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one('users', {'email': email})
        if user_data is None:
            raise UserNotExistError("No user with this email is found.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise IncorrectPasswordError("The password you entered is incorrect.")

        return True

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one('users', {'email': email})
        if user_data is not None:
            raise UserAlreadyRegisteredError("The email you used has already been used.")
        if not Utils.email_is_valid(email):
            raise InvalidEmailError("The email does not have the right format.")

        User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    def save_to_mongo(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one('users', {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
