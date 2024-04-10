from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.utils.api_response import Response
from src.strategies.constants.endpoints import Endpoints
from src.strategies.dto.request.strategy import StrategyCreate, StrategyUpdate
from src.strategies.dto.response.strategy import StrategiesResponse
from src.strategies.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.STRATEGY,
    summary="Create a new strategy",
    response_model=Response,
    tags=["STRATEGY"]
)
def create_strategy(
        strategy_create: Annotated[StrategyCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="STRATEGY SUCCESSFULLY CREATED",
        data=ServiceFactory.get_strategies_service(db=db).add_strategy(
            user_id=current_user.id,
            strategy_create=strategy_create
        )
    )


@router.get(
    path=Endpoints.STRATEGIES,
    summary="Fetch all the strategies",
    response_model=StrategiesResponse,
    tags=["STRATEGY"]
)
def get_strategies(
        db: Session = Depends(get_db)
) -> StrategiesResponse:
    return StrategiesResponse(
        status_code=status.HTTP_200_OK,
        message="STRATEGIES SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_strategies_service(db=db).get_strategies()
    )


@router.put(
    path=Endpoints.STRATEGY,
    summary="Update existing strategy",
    response_model=Response,
    tags=["STRATEGY"]
)
def update_strategy(
        strategy_id: str,
        strategy_update: Annotated[StrategyUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="STRATEGY SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_strategies_service(db=db).update_strategy(
            user_id=current_user.id,
            strategy_id=strategy_id,
            strategy_update=strategy_update
        )
    )


@router.delete(
    path=Endpoints.STRATEGY,
    summary="Delete existing strategy",
    response_model=Response,
    tags=["STRATEGY"]
)
def delete_strategy(
        strategy_id: str,
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="STRATEGY SUCCESSFULLY DELETED",
        data=ServiceFactory.get_strategies_service(db=db).delete_strategy(
            user_id=current_user.id,
            strategy_id=strategy_id
        )
    )
