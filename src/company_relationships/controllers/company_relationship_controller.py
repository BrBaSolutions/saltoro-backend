from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.utils.api_response import Response
from src.company_relationships.constants.endpoints import Endpoints
from src.company_relationships.dto.request.company_relationship import CompanyRelationshipCreate, \
    CompanyRelationshipUpdate
from src.company_relationships.dto.response.company_realtionship import CompanyRelationshipsResponse
from src.company_relationships.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.COMPANY_RELATIONSHIP,
    summary="Create a new company relationship",
    response_model=Response,
    tags=["COMPANY RELATIONSHIP"]
)
def create_company_relationship(
        company_relationship_create: Annotated[CompanyRelationshipCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="COMPANY RELATIONSHIP SUCCESSFULLY CREATED",
        data=ServiceFactory.get_company_relationship_service(db=db).add_company_relationship(
            user_id=current_user.id,
            company_relationship_create=company_relationship_create
        )
    )


@router.get(
    path=Endpoints.COMPANY_RELATIONSHIPS,
    summary="Fetch all the company relationships",
    response_model=CompanyRelationshipsResponse,
    tags=["COMPANY RELATIONSHIP"]
)
def get_company_relationships(
        db: Session = Depends(get_db)
) -> CompanyRelationshipsResponse:
    return CompanyRelationshipsResponse(
        status_code=status.HTTP_200_OK,
        message="COMPANY RELATIONSHIP SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_company_relationship_service(db=db).get_company_relationships()
    )


@router.put(
    path=Endpoints.COMPANY_RELATIONSHIP,
    summary="Update existing company relationship",
    response_model=Response,
    tags=["COMPANY RELATIONSHIP"]
)
def update_company_relationship(
        company_relationship_id: str,
        company_relationship_update: Annotated[CompanyRelationshipUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="COMPANY RELATIONSHIP SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_company_relationship_service(db=db).update_company_relationship(
            user_id=current_user.id,
            company_relationship_id=company_relationship_id,
            company_relationship_update=company_relationship_update
        )
    )


@router.delete(
    path=Endpoints.COMPANY_RELATIONSHIP,
    summary="Delete existing company relationship",
    response_model=Response,
    tags=["COMPANY RELATIONSHIP"]
)
def delete_company_relationship(
        company_relationship_id: str,
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="COMPANY RELATIONSHIP SUCCESSFULLY DELETED",
        data=ServiceFactory.get_company_relationship_service(db=db).delete_company_relationship(
            user_id=current_user.id,
            company_relationship_id=company_relationship_id
        )
    )
