from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.enum.file_type import FileType
from src.commons.factory.client_factory import ClientFactory
from src.commons.utils.helpers import get_file_key
from src.strategies.constants.error_codes import ErrorCodes
from src.strategies.constants.error_messages import ErrorMessages
from src.strategies.dao.strategy_dao import StrategyDao
from src.strategies.dto.request.strategy import StrategyDetails, StrategyCreate, StrategyUpdate
from src.strategies.entities.strategy import Strategy
from src.strategies.exceptions.strategy_exception import StrategyException
from src.strategies.mapper.strategy_mapper import StrategyMapper


class StrategiesService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(StrategiesService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.strategy_dao = StrategyDao(db=db)
        self.strategy_mapper = StrategyMapper()
        self.s3_client = ClientFactory.get_s3_client()

    def _convert_strategy_entity_to_dto(
            self,
            strategy: Strategy
    ) -> StrategyDetails:
        asset_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=strategy.asset_key
        )

        return self.strategy_mapper.strategy_entity_to_dto(
            strategy=strategy,
            asset_url=asset_url
        )

    def _create_strategy(
            self,
            user_id: str,
            strategy_create: StrategyCreate
    ) -> Strategy:
        strategy: Strategy = self.strategy_mapper.strategy_dto_to_entity(
            strategy=strategy_create
        )

        strategy.asset_key = get_file_key(
            file_type=FileType.STRATEGIES,
            entity_id=strategy.id,
            file_name=strategy_create.file_name
        )

        strategy: Strategy = self.strategy_dao.add_strategy(
            strategy=strategy,
            user_id=user_id
        )

        return strategy

    def add_strategy(
            self,
            user_id: str,
            strategy_create: StrategyCreate
    ) -> str:
        if self.strategy_dao.get_count_of_strategies() >= 4:
            raise StrategyException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.ADD_STRATEGY_FAILED,
                error_message=ErrorMessages.ADD_STRATEGY_FAILED
            )

        strategy: Strategy = self._create_strategy(
            strategy_create=strategy_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=strategy.asset_key
        )

    def _get_strategy_by_id(
            self,
            strategy_id: str
    ) -> Strategy:
        strategy: Strategy = self.strategy_dao.get_strategy_by_id(
            strategy_id=strategy_id
        )

        if strategy is None:
            raise StrategyException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.STRATEGY_NOT_FOUND,
                error_message=ErrorMessages.STRATEGY_NOT_FOUND
            )

        return strategy

    def get_strategies(
            self
    ) -> list[StrategyDetails]:
        strategies: list[Strategy] = self.strategy_dao.get_strategies()

        return [
            self._convert_strategy_entity_to_dto(strategy=strategy)
            for strategy in strategies
        ]

    def _update_strategy(
            self,
            user_id: str,
            strategy: Strategy
    ) -> Strategy:
        strategy: Strategy = self.strategy_dao.update_strategy(
            strategy=strategy,
            user_id=user_id
        )

        return strategy

    def update_strategy(
            self,
            user_id: str,
            strategy_id: str,
            strategy_update: StrategyUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_strategy: Strategy = self._get_strategy_by_id(
            strategy_id=strategy_id
        )

        for field, value in strategy_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_strategy.asset_key = get_file_key(
                        file_type=FileType.STRATEGIES,
                        entity_id=existing_strategy.id,
                        file_name=strategy_update.file_name
                    )
                else:
                    setattr(existing_strategy, field, value)

        existing_strategy: Strategy = self._update_strategy(
            strategy=existing_strategy,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_strategy.asset_key
        ) if file_updated else None

    def delete_strategy(
            self,
            user_id: str,
            strategy_id: str
    ) -> str:
        existing_strategy: Strategy = self._get_strategy_by_id(
            strategy_id=strategy_id
        )

        existing_strategy.is_active = False

        existing_strategy: Strategy = self._update_strategy(
            user_id=user_id,
            strategy=existing_strategy
        )

        return existing_strategy.id
