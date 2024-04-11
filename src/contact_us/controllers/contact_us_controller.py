from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.contact_us.constants.endpoints import Endpoints
from src.contact_us.dto.request.contact_us import ContactUsCreate
from src.contact_us.dto.response.contact_us import ContactUsListResponse, ContactUsResponse
from src.contact_us.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.CONTACT_US,
    summary="Submit a contact-us form",
    response_model=ContactUsResponse,
    tags=["CONTACT US"]
)
def create_contact_us(
        contact_us_create: Annotated[ContactUsCreate, Body()],
        db: Session = Depends(get_db)
):
    return ContactUsResponse(
        status_code=status.HTTP_201_CREATED,
        message="CONTACT US FORM SUCCESSFULLY SUBMITTED",
        data=ServiceFactory.get_contact_us_service(db=db).add_contact_us(
            contact_us_create=contact_us_create
        )
    )


@router.get(
    path=Endpoints.CONTACT_US,
    summary="Fetch all the submitted contact us forms",
    response_model=ContactUsListResponse,
    tags=["CONTACT US"]
)
def get_all_contact_us(
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
) -> ContactUsListResponse:
    return ContactUsListResponse(
        status_code=status.HTTP_200_OK,
        message="SUBMITTED CONTACT US FORMS SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_contact_us_service(db=db).get_all_contact_us()
    )
