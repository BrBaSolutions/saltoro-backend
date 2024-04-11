from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.dto.request.saltoro import SaltoroCreate, SaltoroUpdate
from src.commons.dto.response.saltoro import SaltoroResponse
from src.commons.utils.api_response import Response
from src.commons.constants.endpoints import Endpoints
from src.commons.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.SALTORO,
    summary="Create an entry for company details",
    response_model=Response,
    tags=["SALTORO"]
)
def create_saltoro(
        saltoro_create: Annotated[SaltoroCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="SALTORO SUCCESSFULLY CREATED",
        data=ServiceFactory.get_saltoro_service(db=db).add_saltoro(
            user_id=current_user.id,
            saltoro_create=saltoro_create
        )
    )


@router.get(
    path=Endpoints.SALTORO,
    summary="get the company details",
    response_model=SaltoroResponse,
    tags=["SALTORO"]
)
def get_saltoro(
        db: Session = Depends(get_db)
) -> SaltoroResponse:
    return SaltoroResponse(
        status_code=status.HTTP_200_OK,
        message="SALTORO DETAILS SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_saltoro_service(db=db).get_saltoro()
    )


@router.put(
    path=Endpoints.SALTORO,
    summary="Update existing saltoro",
    response_model=Response,
    tags=["SALTORO"]
)
def update_saltoro(
        saltoro_update: Annotated[SaltoroUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="SALTORO SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_saltoro_service(db=db).update_saltoro(
            user_id=current_user.id,
            saltoro_update=saltoro_update
        )
    )
