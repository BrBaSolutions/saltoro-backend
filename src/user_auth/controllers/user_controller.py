from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.user_auth.constants.endpoints import Endpoints
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.authentication import UserLogin, RefreshToken
from src.user_auth.dto.request.user import UserCreate, UserDetails
from src.user_auth.dto.response.token import TokenResponse
from src.user_auth.dto.response.user import UserResponse
from src.user_auth.factory.service_factory import ServiceFactory

router = APIRouter()


@router.post(
    path=Endpoints.User.USER,
    summary="Create a new user",
    response_model=UserResponse,
    tags=["USER"]
)
def create_user(
        user: Annotated[UserCreate, Body()],
        db: Session = Depends(get_db)
):
    return UserResponse(
        status_code=status.HTTP_201_CREATED,
        message="USER SUCCESSFULLY CREATED",
        data=ServiceFactory.get_user_service(db).create_user(
            user=user
        )
    )


@router.post(
    path=Endpoints.Authentication.LOGIN,
    summary="Login the user",
    response_model=TokenResponse,
    tags=["AUTH"]
)
def login(
        login_request: Annotated[UserLogin, Body()],
        db: Session = Depends(get_db)
) -> TokenResponse:
    return TokenResponse(
        status_code=status.HTTP_200_OK,
        message="USER SUCCESSFULLY LOGGED IN",
        data=ServiceFactory.get_user_service(db).user_login(login_request)
    )


@router.post(
    path=Endpoints.Authentication.REFRESH,
    summary="Refreshes access tokens for user",
    response_model=TokenResponse,
    tags=["AUTH"]
)
def refresh_token(
        refresh_token_request: Annotated[RefreshToken, Body()],
        db: Session = Depends(get_db)
) -> TokenResponse:
    return TokenResponse(
        status_code=status.HTTP_200_OK,
        message="YOUR NEW ACCESS TOKEN",
        data=ServiceFactory.get_user_service(db)
        .refresh_token(refresh_token=refresh_token_request.refresh_token)
    )


@router.get(
    path=Endpoints.User.USER,
    response_model=UserResponse,
    tags=["USER"],
    summary="Get details about authenticated user"
)
def get_user(
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ]
) -> UserResponse:
    return UserResponse(
        status_code=status.HTTP_200_OK,
        message="USER DETAILS SUCCESSFULLY FETCHED",
        data=current_user
    )
