from enum import Enum


class ErrorMessages(str, Enum):
    # JWT token errors
    INVALID_TOKEN = "The requested token is not a valid JWT token."
    EXPIRED_TOKEN = "The requested token has expired."

    # Login/Signup errors
    INCORRECT_PASSWORD = "Password mismatch."
    PASSWORD_CONFIRM_PASSWORD_MISMATCH = "New Password & Confirm Password doesn't have same values."
    USER_ALREADY_EXISTS = "A user with the email/phone number already exists."
    USER_NOT_FOUND = "User with email: {user_id} does not exist."
