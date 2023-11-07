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
