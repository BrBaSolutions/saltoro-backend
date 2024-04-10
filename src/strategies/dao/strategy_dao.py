from typing import Type, Union

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.strategies.entities.strategy import Strategy


class StrategyDao:
    def __init__(self, db: Session):
        self.db = db

    def add_strategy(
            self,
            strategy: Strategy,
            user_id: str
    ) -> Strategy:
        try:
            strategy.save(self.db, user_id)
            return strategy
        except Exception as e:
            handle_db_error(
                "strategy -> strategy_dao -> add_strategy",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_strategies(
            self
    ) -> list[Type[Strategy]]:
        try:
            return (
                self.db.query(Strategy)
                .order_by(Strategy.name)
                .filter(
                    Strategy.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "strategy -> strategy_dao -> get_strategies",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_count_of_strategies(
            self
    ) -> int:
        try:
            return (
                self.db.query(func.count(Strategy.id))
                .filter(
                    Strategy.is_active.__eq__(True),
                )
                .scalar()
            )
        except Exception as e:
            handle_db_error(
                "strategy -> strategy_dao -> get_count_of_strategies",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_strategy_by_id(
            self,
            strategy_id: str
    ) -> Union[Strategy, None]:
        try:
            return (
                self.db.query(Strategy)
                .filter(
                    and_(
                        Strategy.id.__eq__(strategy_id),
                        Strategy.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "strategy -> strategy_dao -> get_strategy_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_strategy(
            self,
            strategy: Strategy,
            user_id: str
    ) -> Strategy:
        try:
            strategy.save(self.db, user_id)
            return strategy
        except Exception as e:
            handle_db_error(
                "strategy -> strategy_dao -> update_strategy",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
