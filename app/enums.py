import enum


class ErrorEnum(enum.Enum):
    USER_NOT_FOUND = "User not found"
    INCORRECT_PASSWORD = "Incorrect password"
    INVALID_INPUT_DATA = "Invalid input data"
    EMAIL_ALREADY_EXIST = "Email already in use"
    LOGIN_ALREADY_EXIST = "Login already in use"
    INVALID_TOKEN = "Invalid token"


class PersonTypeEnum(enum.Enum):
    REGULAR = "regular"
    MODERATOR = "moderator"
    ADMIN = "admin"
