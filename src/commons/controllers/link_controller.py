from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.dto.request.link import LinkCreate, LinkUpdate
from src.commons.dto.response.link import LinksResponse
from src.commons.utils.api_response import Response
from src.commons.constants.endpoints import Endpoints
from src.commons.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.LINK,
    summary="Create a new link",
    response_model=Response,
    tags=["LINK"]
)
def create_link(
        link_create: Annotated[LinkCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="LINK SUCCESSFULLY CREATED",
        data=ServiceFactory.get_link_service(db=db).add_link(
            user_id=current_user.id,
            link_create=link_create
        )
    )


@router.get(
    path=Endpoints.LINKS,
    summary="Fetch all the links",
    response_model=LinksResponse,
    tags=["LINK"]
)
def get_links(
        db: Session = Depends(get_db)
) -> LinksResponse:
    return LinksResponse(
        status_code=status.HTTP_200_OK,
        message="LINK SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_link_service(db=db).get_links()
    )


@router.put(
    path=Endpoints.LINK,
    summary="Update existing link",
    response_model=Response,
    tags=["LINK"]
)
def update_link(
        link_id: str,
        link_update: Annotated[LinkUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="LINK SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_link_service(db=db).update_link(
            user_id=current_user.id,
            link_id=link_id,
            link_update=link_update
        )
    )


@router.delete(
    path=Endpoints.LINK,
    summary="Delete existing link",
    response_model=Response,
    tags=["LINK"]
)
def delete_link(
        link_id: str,
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="LINK SUCCESSFULLY DELETED",
        data=ServiceFactory.get_link_service(db=db).delete_link(
            user_id=current_user.id,
            link_id=link_id
        )
    )
