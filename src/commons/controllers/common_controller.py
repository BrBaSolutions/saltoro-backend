from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.factory.client_factory import ClientFactory
from src.commons.factory.service_factory import ServiceFactory
from src.commons.utils.api_response import Response

router = APIRouter()


@router.get(
    path="/test",
    summary="Test-API",
    response_model=Response,
    tags=["COMMON"]
)
def test_api(
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="Test-API",
        data=ClientFactory.get_ses_client().send_templated_email(
            receivers=["geetansh2k1@gmail.com"],
            template_data={'userName': 'Geetansh Sharma', 'userEmail': 'geetansh2k1@gmail.com', 'userPhone': '+1234567890', 'userCompany': 'ABC Company', 'service': 'Customer Support', 'query': 'I have a question regarding your product.'}
        )
    )
