import boto3
from botocore.config import Config
from starlette import status

from src.commons.client.config_client import ConfigClient
from src.commons.constants.error_codes import ErrorCodes
from src.commons.constants.error_messages import ErrorMessages
from src.commons.exceptions.client_exception import ClientException


class S3Client:
    _instance = None

    BUCKET = ConfigClient.get_property(section='AWS', name='BUCKET_NAME')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(S3Client, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = boto3.client(
                's3',
                config=Config(signature_version='s3v4')
            )
        return cls._instance

    @staticmethod
    def _get_params(
            file_key: str
    ) -> dict:
        return {
            "Bucket": S3Client.BUCKET,
            "Key": file_key
        }

    def get_upload_pre_signed_url(
            self,
            file_key: str,
            expiration: int = 600
    ):
        try:
            url = self.client.generate_presigned_url(
                'put_object',
                Params=self._get_params(
                    file_key=file_key
                ),
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            raise ClientException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.ERROR_WHILE_GENERATING_UPLOAD_URL,
                error_message=ErrorMessages.ERROR_WHILE_GENERATING_UPLOAD_URL,
                error=e
            )

    def get_download_pre_signed_url(
            self,
            file_key: str,
            expiration: int = 86400  # 24 hours
    ) -> str:
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params=self._get_params(
                    file_key=file_key
                ),
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            raise ClientException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.ERROR_WHILE_GENERATING_DOWNLOAD_URL,
                error_message=ErrorMessages.ERROR_WHILE_GENERATING_DOWNLOAD_URL,
                error=e
            )

    def check_file_exists(
            self,
            file_key: str
    ) -> bool:
        try:
            self.client.head_object(
                Bucket=S3Client.BUCKET,
                Key=file_key
            )
            return True
        except self.client.exceptions.NoSuchKey:
            return False
