from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.utils.api_response import Response
from src.services.constants.endpoints import Endpoints
from src.services.dto.request.services import ServicesCreate, ServicesUpdate
from src.services.dto.response.services import ServicesResponse
from src.services.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.SERVICE,
    summary="Create a new service",
    response_model=Response,
    tags=["SERVICE"]
)
def create_service(
        services_create: Annotated[ServicesCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="SERVICE SUCCESSFULLY CREATED",
        data=ServiceFactory.get_services_service(db=db).add_service(
            user_id=current_user.id,
            service_create=services_create
        )
    )


@router.get(
    path=Endpoints.SERVICES,
    summary="Fetch all the services",
    response_model=ServicesResponse,
    tags=["SERVICE"]
)
def get_services(
        db: Session = Depends(get_db)
) -> ServicesResponse:
    return ServicesResponse(
        status_code=status.HTTP_200_OK,
        message="SERVICES SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_services_service(db=db).get_services()
    )


@router.put(
    path=Endpoints.SERVICE,
    summary="Update existing service",
    response_model=Response,
    tags=["SERVICE"]
)
def update_service(
        service_id: str,
        services_update: Annotated[ServicesUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="SERVICE SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_services_service(db=db).update_service(
            user_id=current_user.id,
            service_id=service_id,
            service_update=services_update
        )
    )


@router.delete(
    path=Endpoints.SERVICE,
    summary="Delete existing service",
    response_model=Response,
    tags=["SERVICE"]
)
def delete_service(
        service_id: str,
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="SERVICE SUCCESSFULLY DELETED",
        data=ServiceFactory.get_services_service(db=db).delete_service(
            user_id=current_user.id,
            service_id=service_id
        )
    )
