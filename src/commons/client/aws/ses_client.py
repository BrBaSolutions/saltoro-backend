import json

import boto3
from pydantic import EmailStr
from starlette import status

from src.commons.client.aws.constants.config import EmailTemplates
from src.commons.client.config_client import ConfigClient
from src.commons.constants.error_codes import ErrorCodes
from src.commons.constants.error_messages import ErrorMessages
from src.commons.exceptions.client_exception import ClientException


class SESClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SESClient, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = boto3.client('ses')
        return cls._instance

    def send_templated_email(
            self,
            receivers: list[EmailStr],
            template_data: dict,
            email_template: EmailTemplates = EmailTemplates.QUERY_NOTIFICATION_TEMPLATE,
            sender: EmailStr = ConfigClient.get_property(section='AWS', name='SENDER_EMAIL')
    ):
        try:
            response = self.client.send_templated_email(
                Source=sender,
                Destination={
                    'ToAddresses': receivers
                },
                Template=email_template.value,
                TemplateData=json.dumps(template_data)
            )
            return response
        except Exception as e:
            raise ClientException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.ERROR_SENDING_EMAIL,
                error_message=ErrorMessages.ERROR_SENDING_EMAIL.format(receivers=receivers),
                error=e
            )
