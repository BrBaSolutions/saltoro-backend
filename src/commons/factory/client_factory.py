from src.commons.client.aws.s3_client import S3Client
from src.commons.client.aws.ses_client import SESClient


class ClientFactory:
    @staticmethod
    def get_s3_client():
        return S3Client()

    @staticmethod
    def get_ses_client():
        return SESClient()
