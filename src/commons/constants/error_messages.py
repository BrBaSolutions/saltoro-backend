from enum import Enum


class ErrorMessages(str, Enum):
    # DB Errors
    DB_EXECUTION_ERROR = ("An unexpected error occurred on the server. Please try again later or contact support if "
                          "the problem persists.")

    # S3 Errors
    ERROR_WHILE_GENERATING_UPLOAD_URL = "Error occurred while generating upload url."
    ERROR_WHILE_GENERATING_DOWNLOAD_URL = "Error occurred while generating download url."

    # SES Errors
    ERROR_SENDING_EMAIL = "Failed to send email to {receivers}"

    # SALTORO
    SALTORO_DETAILS_NOT_FOUND = "No company details added"
    ADD_SALTORO_FAILED = "Only one entry can be made for company details"

    # LINKS
    LINK_NOT_FOUND = "Link not found"
