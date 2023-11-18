import enum
import os

from dotenv import load_dotenv

load_dotenv()


class ErrorEnum(enum.Enum):
    USER_NOT_FOUND = "User not found"
    INCORRECT_PASSWORD = "Incorrect password"
    INVALID_INPUT_DATA = "Invalid input data"
    EMAIL_ALREADY_EXIST = "Email already in use"
    LOGIN_ALREADY_EXIST = "Login already in use"
    INVALID_TOKEN = "Invalid token"
    PERMISSION_ERROR = "Your permission level is insufficient to access this resource."


class PersonTypeEnum(enum.Enum):
    REGULAR = "regular"
    MODERATOR = "moderator"
    ADMIN = "admin"


class TokenEnum(enum.Enum):
    TOKEN_KEY = "jwt_token"

class SMTPCredsEnum(enum.Enum):
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME = os.getenv("MAIN_FROM_NAME")


class LetterNameEnum(enum.Enum):
    ACCOUNT_CREATED = "templates/email/account_created.html"
    ACCOUNT_BLOCKED = "templates/email/account_blocked.html"


class SubjectMailEnum(enum.Enum):
    ACCOUNT_CREATED = "Account Successfully created!"
    ACCOUNT_BLOCKED = "Your account has been Blocked."


class EndpointPath(enum.Enum):
    REGISTER = "/register"
    LOGIN = "/login"
    GET_ALL_USERS = "/get_all_users"
    GET_USER = "/get_user/{user_id}"
    GET_ACTIVE_USERS = "/get_active_users"
    DEACTIVATE_USER = "/deactivate_user/{user_id}"
    CHANGE_PERSON_TYPE = "/change_person_type"


